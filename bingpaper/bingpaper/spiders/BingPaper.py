# -*- coding: utf-8 -*-
import scrapy
import os


class BingpaperSpider(scrapy.Spider):
    name = 'BingPaper'
    allowed_domains = ['cn.bing.com']
    start_urls = ['http://cn.bing.com/?mkt=zh-CN']

    def parse(self, response):
        imgurl = "http://cn.bing.com" + response.xpath("//link[@rel='preload']//@href").extract_first()
        yield scrapy.Request(url=imgurl, callback=self.parse_url)

    '''此函数根据图片链接下载，并判断是否存在该图片，若不存在则下载并存储在磁盘中'''
    def parse_url(self, response):
        # 确定存储文件夹，若不存在则创建
        bp_savepath = 'd:\\bingpapers'
        if os.path.exists(bp_savepath) == False:
            os.mkdir(p_savepath)
        # 读取目录下的文件名，并将前10个字符存储在一个list中，用于后面判断是否重复
        bp_name_list = []
        bp_names = os.listdir(bp_savepath)
        for bp_name in bp_names:
            bp_name_list.append(bp_name[:10])

        # 直接从链接中提取图片文件名
        filename = response.url.split("/")[-1]
        if filename[:10] not in bp_name_list:
            with open(bp_savepath + "\\" + filename, 'wb') as f:  # python文件操作
                f.write(response.body)  # 刚才下载的图片去哪里了？response.body就代表了刚才下载的图片！
            self.log('保存文件: %s' % filename)  # 打个日志
        else:
            print("图片已经存在")
