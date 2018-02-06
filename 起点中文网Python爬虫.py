# -*- coding: UTF-8 -*-
from lxml import etree
import requests
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
urls = ['https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubfl' \
        'ag=0&hiddenField=0&page={}'.format(i)for i in range(1,20)]

f = open('C://Users/Li Zhenhan/Desktop/QiDian.csv','wb')
writer = csv.writer(f)
writer.writerow(("小说名","作者","分类","状态","简介"))

i = 1
for url in urls:
    html = requests.get(url,headers = headers)
    selector = etree.HTML(html.text)
    infos = selector.xpath('//li[@data-rid]/div[@class="book-mid-info"]')
    print("i = %s"%i)
    i = i + 1
    for a in infos:
        name = a.xpath('h4/a/text()')[0]
        author = a.xpath('p[@class="author"]/a[1]/text()')[0]
        classification1 = a.xpath('p[@class="author"]/a[2]/text()')[0]
        classification2 = a.xpath('p[@class="author"]/a[3]/text()')[0]
        combinedclass = classification1 + "*" + classification2
        status = a.xpath('p[@class="author"]/span/text()')[0]
        intro = a.xpath('p[@class="intro"]/text()')[0].strip()
        writer.writerow((name,author,combinedclass,status,intro))
f.close()