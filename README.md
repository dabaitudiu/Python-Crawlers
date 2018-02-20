# Python爬虫实践

利用**requests, BeautifulSoup, lxml**等库爬取豆瓣、糗事百科、知乎等网站信息.
+ 2018/2/9 新增豆瓣音乐TP250爬虫

+ 2018/2/11 新增简书网30日信息爬虫 以及bug文档

+ 2018/2/20 新增拉钩网爬虫。拉钩网用了Ajax技术，通过构造post参数来获得不同页面信息，将其储存在MongoDB数据库中。
  注意：headers信息要写全，如果不能获得信息或提示“请求过于频繁”可能是因为headers没有包含referer这个参数。
  
+ 2018/2/20 新增微博热门。白天巧合的构造出了url，晚上想重做一遍怎么都做不出来了。。代替方法是用在chrome中选择移动端，request get到response，从       response中提取文字。headers就是正常的user-agent和cookie. 微博反爬虫做的有点强，还是说我没领悟到？网页版基本热门爬不出来。。
```python
urls = ['https://m.weibo.cn/api/container/getIndex?containerid=102803&since_id={}'.format(i) for i in range(1,52)]
#记住这个地址。。
```
      

