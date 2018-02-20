# -*- coding: UTF-8 -*-
import re
import requests
import json
import pymongo
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')

urls = ['https://m.weibo.cn/api/container/getIndex?containerid=102803&since_id={}'.format(i) for i in range(1,52)]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
           'Cookie': 'SCF=AvZ-aQesp6qSkS2x9KTXxKBcVt9JvaLqqNez5fEKEPDr-139Ip6co9sKUctDgom1bhiibDfx56nzNtD41oQbPPE.; '
                     'SUB=_2A253j7WwDeRhGeNP7FAV8yfLyTuIHXVVc9v4rDV6PUJbktBeLVTjkW1NTnhnKCsD2MnwPjMyV74NOe42EB-Rkbfk; '
                     'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWz5hFzFGi.ihmYC00vnBBz5JpX5oz75NHD95QfeKMEShe4S0zNWs4Dqcj'
                     '6i--Xi-i2i-27i--NiKLhiKyFi--NiKLhiKyFi--Ri-isiK.4i--Xi-zRi-8Wi--Ni-2EiK.Ni--fiK.fiKyW; SUHB=0z1wG'
                     '0e2fKgrfl; SSOLoginState=1519109600; ALF=1521701600; _T_WM=68494ca8537ffa18aa51fdbd4ce24d50; H5_I'
                     'NDEX=2; H5_INDEX_TITLE=%E4%BD%A0%E7%9C%8B%E7%9C%8B%E8%BF%99%E4%B8%AA%E7%A2%97%E5%95%8A; WEIBOCN_FR'
                     'OM=1110006030; M_WEIBOCN_PARAMS=featurecode%3D20000320%26luicode%3D20000174%26lfid%3Dhotword%26fid'
                     '%3D102803%26uicode%3D10000011'}

f = open('C:/Users/Li Zhenhan/Desktop/weibo.txt','wb')

client = pymongo.MongoClient('localhost',27017)
WeiBo = client['WeiBo']
data = WeiBo['dataf']
i = 0


for url in urls:
    time.sleep(1)
    print("Page %d finished. "%i)
    i = i + 1
    try:
        html = requests.get(url, headers=headers)
        json_data = json.loads(html.text)
        cards = json_data['data']['cards']
        for card in cards:
            text = card['mblog']['text']
            string = "" + text
            #这一步是用于除去非中文字段
            string = string.decode("utf-8")
            filtrate = re.compile(u'[^\u4E00-\u9FA5]')  # 非中文
            filtered_str = filtrate.sub(r' ', string)  # replace
            infos = {'text': filtered_str}
            data.insert_one(infos)
            # print filtered_str
    except KeyError:
        print("Error")
        pass
