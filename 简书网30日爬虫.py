# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import sys
import pymongo
from multiprocessing import Pool

reload(sys)
sys.setdefaultencoding('utf-8')

urls = ['https://www.jianshu.com/trending/monthly?page={}'.format(i) for i in range(1,18)]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

client = pymongo.MongoClient('localhost', 27017)
JianShuDB = client['JianShuDB']
fpg = JianShuDB['fpg']


def mulFunc(url):
    print("New Page Started.")
    html = requests.get(url, headers=headers)
    band = etree.HTML(html.text)
    contents = band.xpath('//div[@class="content"]')
    for c in contents:
        try:
            author = c.xpath('div[@class="author"]/div/a/text()')[0]
            title = c.xpath('a/text()')[0]
            abstract = c.xpath('p/text()')[0].strip()
            # type = c.xpath('div[@class="meta"]/a[1]/text()')[0]
            view = c.xpath('div[@class="meta"]/a[1]/text()')[1].strip()
            comment = c.xpath('div[@class="meta"]/a[2]/text()')[1]
            like = c.xpath('div[@class="meta"]/span/text()')[0]
            colTime = c.xpath('div[1]/div[1]/span/@data-shared-at')[0]
            date = colTime.split("T")[0]
            time = colTime.split("T")[1].split("+")[0]
            when = date + " " + time
            data = {
                'author': author,
                'title': title,
                'time': when,
                'abstract': abstract,
                # 'type': type,
                'view': view,
                'comment': comment,
                'like': like
            }
            fpg.insert_one(data)
        except IndexError:
            pass


if __name__ == '__main__':
    pool = Pool(processes=8)
    pool.map(mulFunc,urls)


