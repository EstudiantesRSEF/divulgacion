"""
Descarga el número de visitas de cada página del blog desde Google Analytics
(GA4) y las guarda en _data/visitas.yml, para que Jekyll las use al generar
la web (ver _plugins/visitas.rb).

Se ejecuta automáticamente cada noche mediante
.github/workflows/actualizar-visitas.yml, pero también puedes lanzarlo
a mano en local:

    pip install google-analytics-data pyyaml
    export GA_PROPERTY_ID="properties/123456789"
    export GOOGLE_APPLICATION_CREDENTIALS="ga-credentials.json"
    python scripts/actualizar_visitas.py
"""

import os
import yaml
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

PROPERTY_ID = os.environ["GA_PROPERTY_ID"]          # p. ej. "properties/123456789"
SALIDA = os.path.join(os.path.dirname(__file__), "..", "_data", "visitas.yml")

# Prefijo bajo el que se sirve el sitio (p. ej. https://estudiantes.rsef.es/divulgacion/...).
# GA4 registra la ruta completa tal como la ve el navegador, incluyendo este prefijo,
# pero Jekyll calcula post.url SIN él (no hay "baseurl" configurado en _config.yml).
# Por eso lo recortamos aquí, para que las claves de visitas.yml coincidan exactamente
# con post.url (ver _plugins/visitas.rb).
PREFIJO_SITIO = "/divulgacion"


def obtener_visitas():
    client = BetaAnalyticsDataClient()  # usa GOOGLE_APPLICATION_CREDENTIALS

    request = RunReportRequest(
        property=PROPERTY_ID,
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[DateRange(start_date="2020-01-01", end_date="today")],
        limit=5000,
    )
    response = client.run_report(request)

    visitas = {}
    for row in response.rows:
        ruta = row.dimension_values[0].value
        vistas = int(row.metric_values[0].value)

        # Quitamos el prefijo del sitio si está presente
        if ruta.startswith(PREFIJO_SITIO):
            ruta = ruta[len(PREFIJO_SITIO):]

        # Normalizamos posibles dobles barras o falta de barra inicial
        if not ruta.startswith("/"):
            ruta = "/" + ruta

        # Solo nos interesan las entradas del blog
        if ruta.startswith("/blog/"):
            visitas[ruta] = visitas.get(ruta, 0) + vistas

    return visitas


def main():
    visitas = obtener_visitas()
    with open(SALIDA, "w", encoding="utf-8") as f:
        f.write(
            "# Este archivo se actualiza automáticamente cada noche mediante\n"
            "# .github/workflows/actualizar-visitas.yml — no lo edites a mano.\n"
        )
        yaml.dump(visitas, f, allow_unicode=True, sort_keys=True)

    print(f"Guardadas {len(visitas)} rutas con visitas en {SALIDA}")


if __name__ == "__main__":
    main()