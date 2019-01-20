# -*- coding: utf-8 -*-
# scrapy爬取全部知乎用户信息
# 1：是否遵守robbots_txt协议改为False
# 2: 加入爬取所需的headers: user-agent，authorazation
# 3：确定爬取任务：即想要得到的用户信息
# 4: 爬取思路解析
# 整体思路：从起始大v开始，获得其关注列表和粉丝列表；解析列表，可以得到每一个用户的详细信息地址，组成每一个用户的url；
# 从用户的url开始，解析用户详细信息，取到详细信息。同时又可以解析到每一个用户的关注列表和粉丝列表，循环请求。
# 分步骤如下：
# 4-1：找到起始大v，请求其页面，循环翻页获取其全部的关注列表，粉丝列表
# 4-2：列表步骤：解析关注列表，粉丝列表，从所有列表中取得用户的url_token，组成用户url，执行用户步骤4-3
# 4-3：用户步骤：解析用户url，该步骤可以获得1.该用户详细信息 2.该用户全部的关注列表与粉丝列表，返回列表步骤4-2
# 4-4：同步存储item到数据库mongodb，去重设计。
import json
import scrapy
from zhihu_s.items import Zhihu2Item

class ZhihuuserSpider(scrapy.Spider):
    name = 'zhihu_spider_user'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    start_user = 'excited-vczh'
    # 一：对用户关注列表的请求构造
    # 用户关注列表 start_user为起始大v，followees_include为请求参数，limit为每页显示用户数，默认20，offset为页码参数，首页为0
    followees_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    followees_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    # 二：对用户粉丝列表的请求构造
    # 用户关注列表 start_user为起始大v，followees_include为请求参数，limit为每页显示用户数，默认20，offset为页码参数，首页为0
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    # 三：对用户详细信息的请求构造
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_include = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
    def start_requests(self):
        # 分别举列表url和用户url示例，以验证是否能够爬取
        # 关注列表url示例
        # 返回401是请求验证用户的身份，知乎的首页是要求验证用户的身份才能进入，所以需要在settings里面设置authorization
        # url='https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=60&limit=20'
        # 用户详细url示例
        # url='https://www.zhihu.com/api/v4/members/lanfengxing?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
        # yield scrapy.Request(url, callback=self.parse)
        # 构造用户关注列表的请求 主要用到format方法

        yield scrapy.Request(url=self.followees_url.format(user=self.start_user, include=self.followees_include, offset=0, limit=20), callback=self.parse_followees)
        # 构造用户粉丝列表的请求 主要用到format方法
        yield scrapy.Request(url=self.followers_url.format(user=self.start_user, include=self.followers_include, offset=0, limit=20),callback=self.parse_followers)
        # 对用户详细信息的请求构造
        yield scrapy.Request(url=self.user_url.format(user=self.start_user, include=self.user_include),callback=self.parse_user)
    # 解析关注列表
    def parse_followees(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                # 解析关注列表，得到所关注人的url_token，构造解析详细信息请求
                yield scrapy.Request(url=self.user_url.format(user=result.get('url_token'), include=self.user_include),callback=self.parse_user)
        # 构造翻页请求
        if 'paging' in results.keys() and results.get('paging').get('is_end')==False:
            next = results.get('paging').get('next')
            yield scrapy.Request(url=next, callback=self.parse_followees)

    # 解析粉丝列表
    def parse_followers(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                # 解析关注列表，得到所关注人的url_token，构造解析详细信息请求
                yield scrapy.Request(url=self.user_url.format(user=result.get('url_token'), include=self.user_include),
                                     callback=self.parse_user)
        # 构造翻页请求
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next = results.get('paging').get('next')
            yield scrapy.Request(url=next, callback=self.parse_followers)

    # 解析用户详细信息,由于我们任务的目标是获取用户详细信息，因此在这一步要确定哪些信息是被使用，在items里面做相应设置
    def parse_user(self, response):
        item = Zhihu2Item()
        # 返回的response是json格式，因此需要解析json
        results = json.loads(response.text)
        # 遍历item数据结构的键名，item.field可以得到数据结构的所有键
        for field in item.fields:
            # 如果item的键名在网页里面，则遍历赋值
            if field in results.keys():
                item[field]=results.get(field)
        yield item

        # 提取用户的关注列表
        yield scrapy.Request(url=self.followees_url.format(user=results.get('url_token'),include = self.followees_include,offset=0, limit=20),callback=self.parse_followees)
        # 提取用户的粉丝列表
        yield scrapy.Request(url=self.followers_url.format(user=results.get('url_token'), include=self.followers_include, offset=0, limit=20),callback=self.parse_followers)