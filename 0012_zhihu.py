import requests

import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()
from lxml import etree
import time


def get_page(url):
    driver.get(url)
    text = driver.page_source
    html = etree.HTML(text)

    list_item = html.xpath('//div[@class="List-item"]')
    user_list=[]
    user_info = {}
    for item in list_item:
        user_info['name'] = item.xpath('.//div[@class="Popover"]//a/text()')[0]

        user_info['user_href'] = item.xpath('.//div[@class="Popover"]//a/@href')[1].split('//')[1]
        user_info['info'] = item.xpath('.//span[@class="ContentItem-statusItem"]/text()')
        user_list.append(user_info)
    print(user_list)


def main():

    id = "%s"  #个人id
    url = "https://www.zhihu.com/people/%s/following" % id
    get_page(url)
    time.sleep(5)
    driver.close()

main()
