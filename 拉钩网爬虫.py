import requests
import json
import pymongo
import time

url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false&isSchoolJob=0'

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
           'Cookie': 'JSESSIONID=ABAAABAAAIAACBI3AB0C3F59B10F66D078B4F5E4A09A94A; _ga=GA1.2.1430593343.1519094020; '
                     '_gid=GA1.2.64420250.1519094020; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1519094020; user_trace_'
                     'token=20180220103341-76b7725e-15e6-11e8-8bee-525400f775ce; LGSID=20180220103341-76b773c3-15e6-11e8'
                     '-8bee-525400f775ce; LGUID=20180220103341-76b77696-15e6-11e8-8bee-525400f775ce; index_location_city'
                     '=%E5%8C%97%E4%BA%AC; _qddaz=QD.w1jd11.3q49jy.jdv1sb7o; X_HTTP_TOKEN=575b8945f60f6114bab0e6948e343416;'
                     ' TG-TRACK-CODE=search_code; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1519096728; LGRID=20180220112806-'
                     '1104e7a5-15ee-11e8-b074-5254005c3644; '
                     'SEARCH_ID=5f3081935a1147ccb3333f910d2b7f01',
           'Connection':'keep-alive',
           'Referer': 'https://www.lagou.com/jobs/list_java?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput='
}

#初始化MongoDB参数
client = pymongo.MongoClient('localhost',27017)
LaGou = client['LaGou']
infos = LaGou['infos']

#提取最大页数
params = {
    'first': 'true',
    'pn':1,
    'kd':'python'
}
html = requests.post(url,data = params,headers = headers)
json_data = json.loads(html.text)
items =  json_data['content']['positionResult']['totalCount']
totalPages = int(items/15) if (items/15) < 30 else 30 		#限制页数：若总页数>30，取30， 否则取最大页数。除以15是因为每页显示15个

#构造post的params参数
def loadPage():
    for i in range(1,totalPages):
        list = {
            'first': 'true',
            'pn': i,
            'kd': 'python'
        }
        getInfo(list)
        print("Page %d finished. "%i)
	time.sleep(1) 				#暂停1s，防止因过快访问被ban IP
		
#从返回的response的json data中提取关键信息，存入MongoDB
def getInfo(params):
    html = requests.post(url, data=params, headers=headers)
    json_data = json.loads(html.text)
    collections = json_data['content']['positionResult']['result']
    for col in collections:
        comment = ""
        for i in col['companyLabelList']:
            comment = comment + " " + i
        aggregation = {
            'city': col['city'],
            'shortName': col['companyShortName'],
            'fullName': col['companyFullName'],
            'companySize': col['companySize'],
            'education': col['education'],
            'industryField': col['industryField'],
            'jobNature': col['jobNature'],
            'address': col['linestaion'],
            'positionAdvantage': col['positionAdvantage'],
            'positionName': col['positionName'],
            'salary': col['salary'],
            'workYear': col['workYear'],
            'formatCreateTime': col['formatCreateTime'],
            'description': comment
        }
        infos.insert_one(aggregation)
	
#程序入口
if __name__ == '__main__':
    loadPage()
