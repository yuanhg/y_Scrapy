# -*- coding: utf-8 -*-

import scrapy

class Xrk8Item(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
    #从跟踪网页请求中获得的两个参数
    data = scrapy.Field()
    file = scrapy.Field()
