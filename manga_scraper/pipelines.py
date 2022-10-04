# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline

class customMangaPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        nome_manga = request.url.split('/')[-3]
        num_capitulo = request.url.split('/')[-2]

        nova_pasta = f"{nome_manga}\{num_capitulo}\\"

        return nova_pasta + request.url.split('/')[-1]