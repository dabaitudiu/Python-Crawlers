# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import sys
import csv
import xlwt
import json
import time

reload(sys)
sys.setdefaultencoding('utf-8')

#先通过百科段子页爬到用户分页，再通过分页爬用户的地理信息。得到信息后，通过百度地图API返回经纬度信息，存入EXCEL中。


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

urls = ['https://www.qiushibaike.com/8hr/page/{}/'.format(i) for i in range(1,10)]
basicURL = 'https://www.qiushibaike.com'
f = open('C://Users/Li Zhenhan/Desktop/GEO1.csv','w')

mapURL = 'http://restapi.amap.com/v3/geocode/geo'

writer = csv.writer(f)
book = xlwt.Workbook(encoding = 'utf-8')
sheet = book.add_sheet('Sheet1')


global m
m = 0

def get_user_info(url):
    html = requests.get(url, headers=headers)
    content = etree.HTML(html.text)
    selector = content.xpath('//div[@class="user-col-left"]')
    if len(selector) == 0:
        pass
    else:
        data = selector[0].xpath('div[2]/ul/li[4]/text()')
        if len(data) == 0:
            pass
        else:
            info = data[0].split("·")[0].strip()
            if info == "未知" or info == "国外":
                pass
            else:
                global m
                lat,alt = getLocation(info)
                infos = [info,lat,alt]
                a = 0
                for i in infos:
                    sheet.write(m,a,infos[a])
                    a = a + 1
                m += 1

def differenttypes(selector):
    for a in selector:
        user = a.xpath('div[1]/a[1]/@href')
        if len(user) != 0:
            path = basicURL + user[0]
            get_user_info(path)
        else:
            pass


def getLocation(info):
    par = {'address': info, 'key': 'cb649a25c1f81c1451adbeca73623251'}
    res = requests.get(mapURL, par)
    raw = json.loads(res.text)
    try:
        locations = raw['geocodes'][0]['location']
        latitude = locations.split(",")[0]
        altitude = locations.split(",")[1]
    except 'geocodes':
        locations = "NA"
        latitude = "NA"
        altitude = "NA"
    return latitude,altitude


if __name__ == '__main__':
    i = 1
    for url in urls:
        print("当前循环：%s " % i)
        i = i + 1
        html = requests.get(url, headers=headers)
        content = etree.HTML(html.text)
        selector1 = content.xpath('//div[@class="article block untagged mb15 typs_recent"]')
        selector2 = content.xpath('//div[@class="article block untagged mb15 typs_hot"]')
        selector3 = content.xpath('//div[@class="article block untagged mb15 typs_old"]')
        differenttypes(selector1)
        print("s1 finished.")
        differenttypes(selector2)
        print("s2 finished.")
        differenttypes(selector3)
        print("s3 finished.")
        time.sleep(2)

    book.save('C://Users/Li Zhenhan/Desktop/infoss.csv')
