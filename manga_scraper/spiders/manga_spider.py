import scrapy


class MangaSpiderSpider(scrapy.Spider):
    name = 'manga_spider'
    allowed_domains = ['goldenmangas.top']
    #start_urls = ['http://goldenmangas.top/']

    def start_requests(self):
        yield scrapy.Request(f'{self.manga_url}')

    def parse(self, response):
        capitulos = response.css("li.row")
        
        for capitulo in capitulos[:5]:
            link_capitulo = capitulo.css("a::attr(href)").get()

            yield response.follow(link_capitulo, callback=self.parse_capitulos)
    
    def parse_capitulos(self, response):
        paginas = response.css("#capitulos_images img")
        dominio = response.request.url.split("/m")[0]

        links_paginas = []
        for pagina in paginas:
            links_paginas.append(dominio + pagina.css("img::attr(src)").get())
        
        yield{
            'image_urls': links_paginas
        }