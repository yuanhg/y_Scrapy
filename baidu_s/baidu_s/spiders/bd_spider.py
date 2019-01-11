import scrapy

# 需要继承scrapy.Spider类
class scrapy_baidu(scrapy.Spider):
    # 定义蜘蛛名
    name = "bd_spider"


    def start_requests(self):  # 由此方法通过下面链接爬取页面

        # 定义爬取的链接
        urls = [ 'http://cn.bing.com',    ]
        myHeaders = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            'Content-Length': '0',
            "Connection": "keep-alive",
        }

        for url in urls:
            # 爬取到的页面如何处理？提交给parse方法处理
            yield scrapy.Request(url=url, callback=self.parse, headers=myHeaders)

    def parse(self, response):
        #page = response.url.split("/")[-2]  # 根据上面的链接提取分页,如：/page/1/，提取到的就是：1
        #filename = 'baidu-%s.html' % page  # 拼接文件名，如果是第一页，最终文件名便是：mingyan-1.html
        filename = 'baidu-scrapy.html'
        with open(filename, 'wb') as f:  # python文件操作，不多说了；
            f.write(response.body)  # 刚才下载的页面去哪里了？response.body就代表了刚才下载的页面！
        self.log('保存文件: %s' % filename)  # 打个日志
