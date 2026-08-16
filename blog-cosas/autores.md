---
title: "Todos los autores del Blog"
layout: null
permalink: /blog/autores/
---
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Autores | El Blog del GdeE</title>
    <link rel="icon" type="image/png" href="/divulgacion/img/logos/logo-fondo-cuadrado.png">
    <link rel="shortcut icon" type="image/png" href="/divulgacion/img/logos/logo-fondo-cuadrado.png">
    <link rel="apple-touch-icon" href="/divulgacion/img/logos/logo-fondo-cuadrado.png">
    {% include blog-styles.html %}
    {% include analytics.html %}
</head>
<body>

{% include blog-header.html %}

<div class="blog-layout" style="grid-template-columns: 1fr;">
    <div class="blog-main">
        <h2 class="blog-heading">Todos los autores</h2>
        {% include autores-destacados.html %}
        <div class="autores-lista-grid">
            {% for entrada in ranking_final %}
                {% assign partes = entrada | split: "||" %}
                {% assign autor_numero = partes[0] | plus: 0 %}
                {% assign autor_nombre = partes[1] %}
                {% assign autor_info = site.data.autores[autor_nombre] %}
                {% assign autor_slug = autor_nombre | slugify %}
                <a href="{{ site.baseurl }}/autores/{{ autor_slug }}/" class="autor-destacado">
                    <img src="{{ autor_info.image | default: '/divulgacion/Divulgacion-cosas/avatar-default.svg' }}" alt="Foto de {{ autor_nombre }}" onerror="this.onerror=null;this.src='/divulgacion/Divulgacion-cosas/avatar-default.svg';">
                    <div>
                        <div class="nombre">{{ autor_nombre }}</div>
                        <div class="conteo">{{ autor_numero }} entrada{% unless autor_numero == 1 %}s{% endunless %}</div>
                    </div>
                </a>
            {% endfor %}
        </div>
    </div>
</div>

{% include blog-footer.html %}
</body>
</html>