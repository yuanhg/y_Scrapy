# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# 项目管道用来处理得到的item信息,这里设置存储到MongoDB的class
class MongoPipeline(object):

    #初始化变量, 这里需要传入mongo_uri,mongo_db两个参数,这两个参数可以从类方法里面获得
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # 定义类方法,获得mongo_uri,mongo_db
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
        mongo_uri = crawler.settings.get('MONGO_URI'),
        mongo_db = crawler.settings.get('MONGO_DB')
        )

    # 初始化mongodb的变量,client, 与db,爬虫启动时即开始初始化
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    # 存储主体进程,返回item或者DropItem,这里设置update方法设置去重, 如果有同名就更新,没有就重新建立
    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].update({'url_token':item['url_token']}, {'$set':item}, True)
        return item

    # 关闭mongodb
    def close_spider(self,spider):
        self.client.close()