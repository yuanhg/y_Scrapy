# -*- coding: utf-8 -*-

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class Xrk8Pipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for imgUrl in item['image_urls']:
            yield scrapy.Request(imgUrl)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        item['image_paths'] = image_path
        return item

    '''
    def parse_image(self, response):
        # 定义图片名字
        name = "0000.png"
        # 图片保存路径
        img_save_path = "D:/wallpapers/" + name
        with open(img_save_path,"wb") as fw:
            fw.write(response.body)
    
    '''