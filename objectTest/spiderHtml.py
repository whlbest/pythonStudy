# -*- coding: utf-8 -*-
import codecs
import os

import zlib
from bs4 import BeautifulSoup
import requests

__author__ = 'wanghaolong'


# from urllib import request
class sHtml(object):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch, br'}

    # 打开页面获取到定位的内容返回str

	def getUrltext(self,url, coding='utf-8'):
		req = requests.get(url)
		# data = zlib.decompress(req.text, 16 + zlib.MAX_WBITS)
		return BeautifulSoup(req.content.decode(coding), 'html.parser')

	# 保存文本内容到本地
	def saveText(self, filename, content, mode='w'):
		# self._checkPath(filename)
		with codecs.open(filename, encoding='utf-8', mode=mode) as f:
			f.write(content)

        # #保存图片
        # def saveImg(self, imgUrl, imgName):
        # 	data=request.urlopen(imgUrl).read()
        # 	self._checkPath(imgName)
        # 	with open(imgName,'wb') as f:
        # 		f.write(data)

        # 创建目录
	def _checkPath(self, path):
		dirname = os.path.dirname(path.strip())
		if not os.path.exists(dirname):
			os.makedirs(dirname)
