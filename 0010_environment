import requests
import bs4
import time
from lxml import etree
import os


def get_cities_url():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'aqi_query_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFRkkiJTZiZjQ1MWI5NjUzZWNiZDA0MzIzMzllMWUxMWRjYmZiBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUxuYkg4V0tMV2xMeXFBb2NFNDViMHRWTklPRE5lMUxEQ01OQmd2VXFELzg9BjsARg%3D%3D--a08f667c6f9b040442ae1daab0fc5c45641db6bf; __utma=162682429.909376057.1565782011.1565782011.1565782011.1; __utmc=162682429; __utmz=162682429.1565782011.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=162682429.1.10.1565782011',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    response = requests.get('http://www.pm25.in/', headers=headers).text
    reslut = {}
    soup = bs4.BeautifulSoup(response, 'lxml').find('div', attrs={'class': 'all'}).find_all('ul')
    for item in soup:
        cities = item.find_all('a')
        for item in cities:
            cities_name = item.get_text()
            url = item.get('href')
            cities_url = 'http://www.pm25.in/' + url
            reslut[cities_name] = cities_url
    return reslut


def get_time():
    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return time_now


def get_info(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '_utmz=162682429.1565771778.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _aqi_query_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFRkkiJWFlZjc0ZmU0NDUyY2MzNzM0ZTFmNWQ5NGY5OGEwM2EwBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMXNjYXhtV0tVZCtPdmFBOVVGS1RNQThieEJVZlM5aTdOWEtyYzU1MXJva1E9BjsARg%3D%3D--db4a6df8dce35e9592aeafb012e12df5e3111190; __utma=162682429.744598818.1565771778.1565771778.1565832496.2; __utmc=162682429',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    response = requests.get(url, headers=headers).text
    html = etree.HTML(response)
    heads = bs4.BeautifulSoup(response, 'lxml').find('table', attrs={'id': 'detail-data'}).find('thead').find_all('th')
    city_name = html.xpath('//div[@class="city_name"]/h2/text()')[0]
    data = html.xpath('//div[@class="live_data_time"]/p/text()')[0]
    print(data)
    sites = bs4.BeautifulSoup(response, 'lxml').find('table', attrs={'id': 'detail-data'}).find('tbody').find_all('tr')
    for item in sites:
        site = item.find('td').get_text()
        with open('result/' + str(city_name) + '/' + site + '.txt', 'w+', encoding='utf-8') as f:
            for line in heads:
                head = line.get_text()
                f.write(str(head) + '\t')
            f.write('\n')
            for item1 in sites:
                infos = item1.find_all('td')
                for fo in infos:
                    info = fo.get_text()
                    f.write(str(info) + '\t')
                f.write('\n')


if __name__ == '__main__':
    result = get_cities_url()
    try:
        os.mkdir('result')
    except:
        pass
    for cities_name in result:
        try:
            os.mkdir('result/' + cities_name)
        except:
            pass

        get_info(result[cities_name])



