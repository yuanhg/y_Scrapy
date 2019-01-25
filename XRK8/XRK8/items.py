# -*- coding: utf-8 -*-

import scrapy

class Xrk8Item(scrapy.Item):
    image_urls = scrapy.Field()
    image_names = scrapy.Field()
    pass
