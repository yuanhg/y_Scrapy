import scrapy

class BingpaperSpider(scrapy.Spider):
    name = 'imageurldownload'

    def start_requests(self):
        file_path = 'D:\\data_files\\urls_sexy.txt'
        with open(file_path, 'r') as f:
            for url in f:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = response.url.split("/")[-1]
        #filenames = filename.split(".")

        pathname = "d:\\raw_data\\" + filename        #s[0] + .jpg"
        with open(pathname, 'wb') as f:
            f.write(response.body)
