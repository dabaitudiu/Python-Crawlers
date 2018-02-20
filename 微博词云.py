import jieba.analyse as m
import jieba
path = "C:\Users\Li Zhenhan\PycharmProjects\\try1\weibo_160.txt"
fp = open(path,'r')
content = fp.read()
jieba.load_userdict("C:\Users\Li Zhenhan\PycharmProjects\\try1\\addings.txt")
m.set_stop_words("C:\Users\Li Zhenhan\PycharmProjects\\try1\out.txt")
tags = m.extract_tags(content,topK = 80 , withWeight = True)
for item in tags:
    print(item[0] + '\t' + str(int(item[1]*1000)))
fp.close()
