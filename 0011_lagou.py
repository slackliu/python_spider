import requests
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import  NoSuchElementException
import pymysql

# 获取网页信息

def get_page():
    url = "https://www.lagou.com/"
    browser = webdriver.Chrome()
    browser.get(url)
    quanguo = browser.find_element_by_id("cboxClose")
    quanguo.click()
    wait = WebDriverWait(browser, 30)
    # input = wait.until(EC.presence_of_all_elements_located((By.ID, 'search_input')))
    time.sleep(5)
    input = browser.find_element_by_id("search_input")
    # print(input)
    input.send_keys('Python')
    time.sleep(1)
    # button = wait.until(EC.presence_of_all_elements_located((By.ID, 'earch_button')))
    button = browser.find_element_by_id("search_button")
    button.click()
    source = browser.page_source
    html = etree.HTML(source)
    link = html.xpath('//a[@class="position_link"]/@href')
    url_list = []
    for position_url in link:
        url_list.append(position_url)
    browser.quit()
    return url_list

# 解析网页信息
def parse_page(position_url):
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='mysql')
    cursor = db.cursor()
    driver = webdriver.Chrome()
    driver.get(position_url)
    text = driver.page_source
    html = etree.HTML(text)
    job_info = {}
    name = html.xpath('//div[@class="position-content "]//span[@class="name"]/text()')[0]
    salary = html.xpath('//div[@class="position-content "]//span[@class="salary"]/text()')[0].strip()
    # job_request = html.xpath('//div[@class="position-content "]//dd[@class="job_request"]/p/span/text()')
    # print(job_request)
    drrs = html.xpath('//div[@class="position-content "]//dd[@class="job_request"]/p/span[2]/text()')[0].split('/')[1].strip()
    years = html.xpath('//div[@class="position-content "]//dd[@class="job_request"]/p/span[3]/text()')[0].split('/')[0].strip()
    jingyan = html.xpath('//div[@class="position-content "]//dd[@class="job_request"]/p/span[4]/text()')[0].split('/')[0].strip()
    zhiye = html.xpath('//div[@class="position-content "]//dd[@class="job_request"]/p/span[5]/text()')[0]
    company = html.xpath('//div[@class="job_company_content"]//em[@class="fl-cn"]/text()')[0].strip()
    infos = html.xpath('//div[@class="job-detail"]/p/text()')[:]
    infos = ''.join(infos)
    job_info['职位'] = name
    job_info['薪水'] = salary
    job_info['地址'] = drrs
    job_info['工作年限'] = years
    job_info['经验'] = jingyan
    job_info['是否全职'] = zhiye
    job_info['公司名称'] = company
    job_info['职位描述'] = infos
    sql = '''INSERT INTO func(names, salarys, drrss , yearss, jingyans, zhiyes, companys, infoss) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')'''\
          % (name, salary, drrs, years, jingyan, zhiye, company, infos)
    sql = sql.encode('utf-8')
    cursor.execute(sql)
    db.commit()
    db.close()
    print(job_info)
    driver.quit()


def main():
    url_list = get_page()
    for positioin_url in url_list:
        parse_page(positioin_url)



main()
