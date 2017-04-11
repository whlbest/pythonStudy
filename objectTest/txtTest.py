# -*- coding: utf-8 -*-
import codecs
import re
from bs4 import BeautifulSoup
import requests

__author__ = 'wanghaolong'

def open_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content.decode('utf-8'),'html.parser')
    contxt=soup.find(attrs={"id":"content"})
    return str(contxt.text)

if __name__=='__main__':
    url_dict={}
    url_index='http://www.biquge.tw/0_819/'

    r = requests.get(url_index)
    d=re.findall('<dd> <a style=\"\" href="(.*?)">(.*?)</a></dd>',r.text)
    start=len(d)-10
    end=len(d)
    with codecs.open("ccc.txt",'w',encoding='utf-8') as f:
        for a in d[start:end]:
            url_c='http://www.biquge.tw'+str(a[0])
            # print (url_c)

            print (a[1])
            f.write(str(a[1]))
            f.write('\n')
            f.write('-------------------------------------------')
            f.write('\n')

            cc=open_url(url_c)
            # cc=c.getUrl(url_c)cc
            # contxt=cc.find(attrs={"id":"content"})
            f.write(cc.strip())
            f.write('\n')
    f.close()
