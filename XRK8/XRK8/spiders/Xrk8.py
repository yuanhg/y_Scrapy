# -*- coding: utf-8 -*-

import scrapy
from XRK8.items import Xrk8Item

class Xrk8Spider(scrapy.Spider):
    name = 'Xrk8'
    allowed_domains = ['himawari8.nict.go.jp']
    start_urls = ['http://himawari8.nict.go.jp/']

    # start_urls = ['http://himawari8.nict.go.jp/img/D531106/1d/550/2019/01/21/015000_0_0.png']

    def parse(self, response):
        item = Xrk8Item()
        imgUrl = response.xpath("//meta[@property='og:image']//@content").extract_first()
        item['image_urls'] = [imgUrl]
        yield item


