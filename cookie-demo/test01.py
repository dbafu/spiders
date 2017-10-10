# coding:utf-8
import urllib2
import string

def tieba(url, begin_page, end_page):
    for i in range(begin_page, end_page + 1):
        sName = string.zfill(i, 5) + '.html'
        print '正在下载第' + str(i) + '个网页，并将其存储为 ： ' + sName + '......'
        with open(sName, 'w') as f:
            url += str(i)
            res = urllib2.urlopen(url).read()
            f.write(res)

url = 'https://tieba.baidu.com/p/4251714048?pn='
tieba(url, 1, 8)





