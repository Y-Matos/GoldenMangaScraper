import scrapy
from os import makedirs


class MangaspyderSpider(scrapy.Spider):
    name = 'mangaSpyder'
    allowed_domains = ['goldenmangas.top']
    #https://goldenmangas.top/mangabr/one-punch-man-gm

    def start_requests(self):
        yield scrapy.Request(f'{self.manga_url}')

    def parse(self, response):
        nome = response.css('div.col-sm-8 > h2::text').get()
        genero = response.css('div.col-sm-8 > h5 > a.label.label-warning::text').getall()
        autor = response.css('div.col-sm-8 > h5 > strong + a::text')[0].get()
        artista = response.css('div.col-sm-8 > h5 > strong + a::text')[1].get()
        status = response.css('div.col-sm-8 > h5 > strong + a::text')[2].get()
        descricao = response.css('#manga_capitulo_descricao::text').get().strip()

        capitulos = response.css('li.row')
        
        for capitulo in capitulos[:10]:
            link_capitulo = capitulo.css('a::attr(href)').get()

            yield response.follow(link_capitulo, callback=self.parse_capitulos)
    
    def parse_capitulos(self, response):
        paginas = response.css('#capitulos_images img')
        dominio = response.request.url.split('/m')[0]

        nome_manga = paginas.css('img::attr(src)').get().split('/')[-3]
        num_capitulo = paginas.css('img::attr(src)').get().split('/')[-2]
        
        nova_pasta = f'imgs_temp\{nome_manga}\{num_capitulo}\\'
        try:
            makedirs(nova_pasta)
            print(f'Pasta {num_capitulo} criada com sucesso | Caminho: {nova_pasta}')
        except OSError as error:
            print(error)

        links_paginas = []

        for pagina in paginas:            
            links_paginas.append( dominio + pagina.css('img::attr(src)').get())
            
        yield {
            
            'image_urls' : links_paginas
        }