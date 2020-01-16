from threading import Thread
import urllib.request
import bs4
import urllib.error
from queue import Queue
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}


class productor(Thread):
    def __init__(self, pageQueue, imgQueue):
        super(productor, self).__init__()
        self.pageQueue = pageQueue
        self.imgQueue = imgQueue

    def run(self):
        while True:
            if self.pageQueue.empty():
                break
            url = self.pageQueue.get()
            print(url)
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode("utf-8")
            soup = bs4.BeautifulSoup(html, "lxml")
            pic_lists = soup.find('ul', attrs={"class": "thumbnails"})
            pic_list = pic_lists.find_all('li')
            for pics in pic_list:
                pic_url = pics.find('img')['src']
                title = pics.find('img')['title']
                title = title.replace('.', '').replace('?', '').replace('*', '').replace('/', '').replace('\\', '').replace('。', '').replace('，', '')
                imgQueue.put((pic_url, title))


class consumor(Thread):
    def __init__(self, pageQueue, imgQueue):
        Thread.__init__(self)
        self.pageQueue = pageQueue
        self.imgQueue = imgQueue

    def run(self):
        while True:
            if self.pageQueue.empty() and self.imgQueue.empty():
                break
            pic_url, title = self.imgQueue.get()
            urllib.request.urlretrieve(pic_url, "D:\工作\python\spider\images\\" + title + ".jpg")
            print('下载成功！')


if __name__ == '__main__':
    pageQueue = Queue(50)
    for i in range(1, 51):
        url = "https://www.dbmeinv.com/?pager_offset=" + str(i)
        pageQueue.put(url)
    imgQueue = Queue(1000)
    for j in range(5):
        thread = productor(pageQueue, imgQueue)
        thread.start()
        thread.join()
    for j in range(5):
        thread = consumor(pageQueue, imgQueue)
        thread.start()
        thread.join()


