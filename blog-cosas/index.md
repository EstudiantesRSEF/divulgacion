---
title: "El Blog del Grupo de Estudiantes de la RSEF"
layout: null
permalink: "/blog/"
---
<!-- <!DOCTYPE html> -->
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ page.title }}</title>
    <link rel="icon" type="image/png" href="/divulgacion/img/logos/logo-fondo-cuadrado.png">
    <link rel="shortcut icon" type="image/png" href="/divulgacion/img/logos/logo-fondo-cuadrado.png">
    <link rel="apple-touch-icon" href="/divulgacion/img/logos/logo-fondo-cuadrado.png">
    {% include blog-styles.html %}
    {% include analytics.html %}
</head>
<body>

{% include blog-header.html %}

<!-- CARRUSEL DE SECCIONES -->
<div class="secciones-carousel" id="seccionesCarousel">
    {% for item in site.data.secciones %}
        {% assign car_slug = item[0] %}
        {% assign car_seccion = item[1] %}
        <a href="{{ site.baseurl }}/secciones/{{ car_slug }}/" class="seccion-slide" style="background-image: url('{{ car_seccion.imagen | relative_url }}');">
            <div class="seccion-slide-overlay"></div>
            <div class="seccion-slide-content">
                <h2>{{ car_seccion.titulo }}</h2>
                <p>{{ car_seccion.descripcion }}</p>
                <span class="btn btn-small">Ver sección</span>
            </div>
        </a>
    {% endfor %}
    <button class="carousel-arrow prev" onclick="moverSecciones(-1)"><i class="fas fa-chevron-left"></i></button>
    <button class="carousel-arrow next" onclick="moverSecciones(1)"><i class="fas fa-chevron-right"></i></button>
    <div class="carousel-dots" id="carouselDots"></div>
</div>

<div class="blog-layout">

    <div class="blog-main">
        <h2 class="blog-heading">Todas las entradas</h2>

        <div class="filtros-categorias">
            <button class="chip_button active" id="All" onclick="filterUsingCategory('All')">Todas las entradas</button>
            {% assign categories = site.categories | sort %}
            {% for category in categories %}
                {% assign cat = category | first %}
                {% if cat == 'blog' or cat == 'blog-cosas'%}
                {% else %}
                    <button class="chip_button" id="{{ cat }}" onclick="filterUsingCategory(this.id)">{{ cat }}</button>
                {% endif %}
            {% endfor %}
        </div>

        <div class="post-card-grid">
            {% assign id = 0 %}
            {% for post in site.posts %}
                {% if post.hidden != true and post.categories contains 'blog' %}
                    {% assign id = id | plus: 1 %}
                    <div id="{{ id }}">
                        {% include blog-post-card.html post=post %}
                    </div>
                {% endif %}
            {% endfor %}
        </div>
    </div>

    <aside class="blog-sidebar">

        <div class="sidebar-widget">
            <h3>Autores destacados</h3>
            {% for autor in site.data.autores_ranking limit: 5 %}
                {% assign autor_info = site.data.autores[autor.nombre] %}
                <div class="autor-destacado">
                    <img src="{{ autor_info.image | default: '/divulgacion/Divulgacion-cosas/avatar-default.svg' }}" alt="Foto de {{ autor.nombre }}" onerror="this.onerror=null;this.src='/divulgacion/Divulgacion-cosas/avatar-default.svg';">
                    <div>
                        <div class="nombre">{{ autor.nombre }}</div>
                        <div class="conteo">{{ autor.numero }} entrada{% unless autor.numero == 1 %}s{% endunless %}</div>
                    </div>
                </div>
            {% endfor %}
        </div>

        <div class="sidebar-widget">
            <h3>Entradas más visitadas</h3>
            {% assign posts_por_visitas = site.posts | where_exp: "p", "p.categories contains 'blog'" | sort: "views" | reverse %}
            {% for post in posts_por_visitas limit: 10 %}
                <a href="{{ post.url | prepend: site.baseurl }}" class="entrada-destacada">
                    <span class="num">{{ forloop.index }}</span>
                    <div>
                        <div class="titulo">{{ post.title }}</div>
                        <div class="visitas">{{ post.views | default: 0 }} visitas</div>
                    </div>
                </a>
            {% endfor %}
        </div>

    </aside>

</div>

{% include blog-footer.html %}

<script>
    // Carrusel de secciones
    const seccionesCarousel = document.getElementById('seccionesCarousel');
    const totalSlides = {{ site.data.secciones | size }};
    const dotsContainer = document.getElementById('carouselDots');
    for (let i = 0; i < totalSlides; i++) {
        const dot = document.createElement('button');
        if (i === 0) dot.classList.add('active');
        dot.onclick = () => irASeccion(i);
        dotsContainer.appendChild(dot);
    }
    function actualizarDots() {
        const index = Math.round(seccionesCarousel.scrollLeft / seccionesCarousel.offsetWidth);
        document.querySelectorAll('.carousel-dots button').forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
    }
    function irASeccion(i) {
        seccionesCarousel.scrollTo({ left: i * seccionesCarousel.offsetWidth, behavior: 'smooth' });
    }
    function moverSecciones(direccion) {
        seccionesCarousel.scrollBy({ left: direccion * seccionesCarousel.offsetWidth, behavior: 'smooth' });
    }
    seccionesCarousel.addEventListener('scroll', () => {
        clearTimeout(window._scrollDebounce);
        window._scrollDebounce = setTimeout(actualizarDots, 100);
    });

    // Filtro de categorías (misma lógica que ya teníamos)
    function filterUsingCategory(selectedCategory) {
        var id = 0;
        document.querySelectorAll('.chip_button').forEach(function (btn) {
            btn.classList.toggle('active', btn.id === selectedCategory);
        });
        {% for post in site.posts %}
            {% if post.categories contains 'blog' and post.hidden != true %}
                var cats = {{ post.categories | jsonify }};
                var postDiv = document.getElementById(++id);
                postDiv.style.display =
                    (selectedCategory == 'All' || cats.includes(selectedCategory))
                        ? 'unset'
                        : 'none';
            {% endif %}
        {% endfor %}
    }
</script>
</body>
</html>
