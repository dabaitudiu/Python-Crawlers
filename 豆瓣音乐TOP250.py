import requests
from lxml import etree
import sys
import xlwt

reload(sys)
sys.setdefaultencoding('utf-8')

urls = ['https://music.douban.com/top250?start={}'.format(i) for i in range(0,250,25)]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
book = xlwt.Workbook(encoding = 'utf-8')
sheet = book.add_sheet('Sheet1')
i = 0
p = 1
for url in urls:
    print("Page %s:"%p)
    p = p + 1
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    content = selector.xpath('//tr[@class="item"]')
    for a in content:
        print("%d/%d completed. " % (i % 25 + 1,25))
        j = 0
        infos = a.xpath('td[2]/div/p/text()')[0].strip()
        _title = a.xpath('td[2]/div/a/text()')[0].strip()
        _name = infos.split("/")[0]
        _date = infos.split("/")[1]
        _type = infos.split("/")[2]
        _perf = infos.split("/")[-1]
        coll = [_title, _name, _date, _type, _perf]
        for b in coll:
            sheet.write(i,j,b)
            j = j + 1
        i = i + 1

book.save('C://Users/Li Zhenhan/Desktop/Movies.csv')
