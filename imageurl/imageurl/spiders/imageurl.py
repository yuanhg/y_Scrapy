

import scrapy
from ..items import ImageurlItem


class ImageurlSpider(scrapy.Spider):
    name = 'imageurl'

    def start_requests(self):
        item = ImageurlItem()
        file_path = 'D:\\data_files\\urls_123.txt'
        urls = []
        with open(file_path, 'r') as f:
            for url in f:
                urls.append(url[:-1])
        item['image_urls'] = urls
        print(item['image_urls'])
        yield item

