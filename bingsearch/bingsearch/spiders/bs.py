# -*- coding: utf-8 -*-
import scrapy


class BsSpider(scrapy.Spider):
    name = 'bs'
    allowed_domains = ['cn.bing.com']
    start_urls = ['http://cn.bing.com/search?q=袁洪岗']

    def parse(self, response):
        with open('123456.html', 'wb') as f:
            f.write(response.body)
        print('All is done')
