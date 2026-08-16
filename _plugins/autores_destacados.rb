# _plugins/autores_destacados.rb
#
# Calcula cuántas entradas ha escrito cada autor, contando también a los
# autores de entradas firmadas por varias personas. En el front matter de
# una entrada con varios autores, sepáralos con "&" y/o "," (puedes
# mezclar ambos), por ejemplo:
#
#   author: "Andrea Morras & Pablo Ruiz"
#   author: "Andrea Morras, Pablo Ruiz, Laura Gómez"
#   author: "Andrea Morras, Pablo Ruiz & Laura Gómez"
#
# Cada persona suma +1 a su propio contador (no cuenta como una sola
# entrada compartida), y el resultado queda disponible en las plantillas
# Liquid como `site.data.autores_ranking`, ya ordenado de mayor a menor
# número de entradas: una lista de {"nombre" => ..., "numero" => ...}.

module GdeE
  class AutoresDestacadosGenerator < Jekyll::Generator
    priority :low

    def generate(site)
      conteo = Hash.new(0)

      site.posts.docs.each do |post|
        next if post.data['hidden']
        next unless Array(post.data['categories']).include?('blog')

        autor_raw = post.data['author'].to_s
        autores = autor_raw.split(/[,&]/).map(&:strip).reject(&:empty?)

        autores.each { |autor| conteo[autor] += 1 }
      end

      ranking = conteo.map { |nombre, numero| { 'nombre' => nombre, 'numero' => numero } }
      ranking.sort_by! { |h| -h['numero'] }

      site.data['autores_ranking'] = ranking
    end
  end
end
