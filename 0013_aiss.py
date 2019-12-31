# -*- coding: utf-8 -*-
import os
import json
import requests
import time
from multiprocessing import Process, Queue, Pool

class downloadinfo:
    def download_info(self):
        """ 下载列表页（包含对所有图片的描述信息），并存储到data/info.txt文件中 """
        page = 1
        while True:
            page_json = self.download_page(page)
            if not page_json['data']['list']:
                break
            self.save_page(page_json)
            page += 1

    def download_page(self, page):
        """ 下载某页面的信息 """
        url = 'http://api.pmkoo.cn/aiss/suite/suiteList.do'
        params = {
            'page': page,
            'userId': 153044
        }
        rsp = requests.post(url, data=params, timeout=100)
        print(rsp.text)
        return rsp.json()
    def save_page(self, page_json):
        """ 保存某页面的信息 """
        txt = json.dumps(page_json)
        with open('data/info.txt', 'a') as f:
            f.write(txt)
            f.write('\n')


class download_pic:
    def get_info(self):
        res=[]
        with open('data/info.txt', 'r') as f:
            for line in f:
                data = json.loads(line)
                res.extend(data['data']['list'])  # list.extend  在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
        return res

    def get_info_imgs(self, info):
        """ 获取要下载的所有图片url、目录名、要存储的名字 """
        res = []
        for item in info:
            nickname = item["author"]["nickname"]
            catalog = item["source"]["catalog"]
            name = item["source"]["name"]
            issue = item["issue"]
            pictureCount = item["pictureCount"]
            for pic_idx in range(pictureCount):
                # url = "http://aiss-1254233499.costj.myqcloud.com/picture/%s/%s/%s.jpg" % (catalog, issue, pic_idx)
                url = "http://tuigirl-1254818389.cosbj.myqcloud.com/picture/%s/%s/%s.jpg" % (catalog, issue, pic_idx)
                directory = os.path.join("data", name, "%s-%s" % (issue, nickname))
                filepath = os.path.join(directory, "%s.jpg" % pic_idx)
                # 每张图片一组，包含 图片url，所在目录，存储路径
                res.append((
                    url, directory, filepath
                ))
        return res

    def setup_download_dir(self, directory):
        """ 设置文件夹，文件夹名为传入的 directory 参数，若不存在会自动创建 """
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except Exception as e:
                pass
        return True
    def download_one(self, img):
        """ 下载一张图片 """
        url, directory, filepath = img
        # 如果文件已经存在，放弃下载
        if os.path.exists(filepath):
            print('exists:', filepath)
            return

        self.setup_download_dir(directory)
        rsp = requests.get(url, timeout=100)
        print('start download', url)
        with open(filepath, 'wb') as f:
            f.write(rsp.content)
            print('end download', url)
    def download(self, imgs, processes=10):
        """ 并发下载所有图片 """
        start_time = time.time()
        pool = Pool(processes)
        for img in imgs:
            pool.apply_async(self.download_one, (img,))
        pool.close()
        pool.join()
        end_time = time.time()
        print('下载完毕,用时:%s秒' % (end_time - start_time))



if __name__ == "__main__":
    info = downloadinfo()
    info.download_info()
    time.sleep(2)
    img = download_pic()
    imgs = img.get_info()
    info = img.get_info_imgs(imgs)
    img.download(info, processes=10)

