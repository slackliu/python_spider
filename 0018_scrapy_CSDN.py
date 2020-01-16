# items相关代码:
name = scrapy.Field()
href = scrapy.Field()
students = scrapy.Field()
contents = scrapy.Field()


# csdn相关代码
import scrapy
from scdnedu import items
import requests
from lxml import etree

class ScdnSpider(scrapy.Spider):
    name = 'scdn'
    allowed_domains = ['edu.csdn.net']
    start_urls = ['https://edu.csdn.net/lecturer']

    def __init__(self):
        super().__init__()
        self.offset = 1
        self.lastpage = self.get_page(self.start_urls[0])

    def get_page(self, url):
        response = requests.get(url).text
        response = etree.HTML(response)
        page = response.xpath('//span[@class="page-nav"]/a[6]/text()')[0]
        page = int(page)
        return page

    def parse(self, response):
        scdneduItem = items. ScdneduItem()
        html = response.xpath('//dl[@class="lector_list"]')
        for item in html:
            href = item.xpath('./dt/a/@href').extract()
            name = item.xpath('./dd/ul/li[1]/a/text()').extract()
            students = item.xpath('./dd/ul/li[3]/span/text()').extract()
            contents = item.xpath('./dd/p/text()').extract()
            scdneduItem['name'] = name
            scdneduItem['href'] = href
            scdneduItem['students'] = students
            scdneduItem['contents'] = contents
            yield scdneduItem

        if self.offset < self.lastpage:
            self.offset += 1
            new_url = 'https://edu.csdn.net/lecturer?page=' + str(self.offset)
            yield scrapy.Request(new_url, self.parse)




# pipeline相关代码：
class ScdneduPipeline(object):
    def __init__(self):
        self.file = open("t.txt", "w")

    def __del__(self):
        self.file.close()

    def process_item(self, item, spider):
        text = str(item) + '\t\n'
        self.file.write(text)
        self.file.flush()
        return item


