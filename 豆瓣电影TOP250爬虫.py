# -*- coding: UTF-8 -*-
from lxml import etree
import requests
import sys
import csv

reload(sys)
sys.setdefaultencoding('utf-8')


urls = ['https://movie.douban.com/top250?start={}&filter='.format(i) for i in range(0,250,25)]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

f = open('C://Users/Li Zhenhan/Desktop/MovieTop250_1.csv','w')
writer = csv.writer(f)
writer.writerow(("片名","导演演员信息","发行日期","国家/地区","评分","评论"))
i = 1
for url in urls:
    html = requests.get(url, headers = headers)
    selector = etree.HTML(html.text)
    mods = selector.xpath('//div[@class="info"]')
    print("Page:%s"%i)
    i= i + 1
    for a in mods:
        name = a.xpath('div[@class="hd"]/a/span[@class="title"]/text()')[0]
        infos = a.xpath('div[@class="bd"]/p[1]/text()')
        dirandactor = infos[0].strip().replace(" ","")
        date = infos[1].strip().split("/")[0]
        country = infos[1].strip().split("/")[1]
        rate = a.xpath('div[@class="bd"]/div/span[2]/text()')[0]
        comments = a.xpath('div[@class="bd"]/p[@class="quote"]/span/text()')
        comment = comments[0] if len(comments) != 0 else "None"
        writer.writerow((name,dirandactor,date,country,rate,comment))
f.close()

