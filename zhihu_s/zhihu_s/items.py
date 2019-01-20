# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 想要获取的用户信息设置
class Zhihu2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 姓名　
    name = scrapy.Field()
    # 性别
    gender = scrapy.Field()
    # 职业
    employments = scrapy.Field()
    # 级别
    badge = scrapy.Field()
    # 一句话介绍
    headline = scrapy.Field()
    # 粉丝数
    follower_count = scrapy.Field()
    # 回答问题数
    answer_count = scrapy.Field()
    # 撰写文章数
    articles_count = scrapy.Field()
    # 头像
    avatar_url = scrapy.Field()
    avatar_url_template = scrapy.Field()
    # id
    id = scrapy.Field()
    # 注册类型
    type = scrapy.Field()
    # 注册url
    url = scrapy.Field()
    # 主页地址，唯一识别码
    url_token = scrapy.Field()
    # 用户类型
    user_type = scrapy.Field()