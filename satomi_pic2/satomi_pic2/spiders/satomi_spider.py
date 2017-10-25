# -*- coding: utf-8 -*-
# import scrapy


# class SatomiSpiderSpider(scrapy.Spider):
#     name = 'satomi_spider'
#     allowed_domains = ['']
#     start_urls = ['http:///']

#     def parse(self, response):
#         pass


from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from satomi_pic2.items import SatomiPic2Item

class SatomiSpider(CrawlSpider):
    name="satomi_pic_spider"

    download_delay=5

    allowed_domains=[]

    start_urls=[
        'http://movie.douban.com/celebrity/1016930/photo/1253599819/'
    ]

    rules=(
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/celebrity/1016930/photo/\d+')),callback='parse_item',follow=True),

    )

    def parse_item(self,response):
        print response

        sel=Selector(response)

        item=SatomiPic2Item()

        item['image_urls']=sel.xpath('//div[@class="photo-show"]/div[@class="photo-wp"]/a/img/@src').extract()

        yield item

    # def parse(self,response):
    #     print response

    #     sel=Selector(response)

    #     item=SatomiPic2Item()

    #     item['image_urls']=sel.xpath('//div[@class="photo-show"]/div[@class="photo-wp"]/a/img/@src').extract()

    #     yield item
