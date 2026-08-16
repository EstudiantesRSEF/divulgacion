# _plugins/visitas.rb
#
# Lee _data/visitas.yml (generado por scripts/actualizar_visitas.py) y
# asigna el número de visitas a cada post como post.views, para que
# _layouts/post.html y las páginas de listado puedan mostrarlo/ordenar por él.

module Visitas
  class Generator < Jekyll::Generator
    priority :low

    def generate(site)
      visitas = site.data['visitas'] || {}

      site.posts.docs.each do |post|
        # post.url ya incluye el permalink completo definido en _config.yml
        # (/blog/:year/:month/:day/:title/), que es el mismo formato que
        # guarda actualizar_visitas.py en _data/visitas.yml
        post.data['views'] = visitas[post.url] || 0
      end
    end
  end
end
 
