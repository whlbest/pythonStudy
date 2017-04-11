# -*- coding: utf-8 -*-
__author__ = 'wanghaolong'

import threading
import urllib2
import Queue
import re

thread_lock = threading.RLock()

#下载页面的一个函数，header中没有任何内容也可以顺利的下载，就省去了
def download_page(html_url):
    try:
        req = urllib2.Request(html_url)
        response = urllib2.urlopen(req)
        page = response.read()
        return page
    except Exception:
        print 'download %s failed' % html_url
        return None

#下载图片的一个方法，和上面的函数很像，只不过添加了一个文件头
#因为在测试的过程中发现天涯对于没有如下文件头的图片链接是不会返回正确的图片的
def download_image(image_url, referer):
    try:
        req = urllib2.Request(image_url)
        req.add_header('Host', 'img3.laibafile.cn')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0')
        req.add_header('Accept', 'image/png,image/*;q=0.8,*/*;q=0.5')
        req.add_header('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3')
        req.add_header('Referer', referer)
        req.add_header('Origin', 'http://bbs.tianya.cn')
        req.add_header('Connection', 'keep-alive')
        response = urllib2.urlopen(req)
        image = response.read()
        return image
    except Exception:
        print 'download %s failed' % image_url
        return None

#下载和解析一个页面的线程类
class download_html_page(threading.Thread):
    #name:线程的名字
    #page_range:用户输入的页面范围
    #page_contents:解析之后楼主的内容
    #img_urls:解析之后楼主贴的图的链接
    #html_url:输入的页面url
    #first_page：第一次已经下载好的页面，主要是考虑效率，不重复下载
    def __init__(self, name, page_range, page_contents, img_urls, html_url, first_page):
        threading.Thread.__init__(self)
        self.name = name
        self.page_range = page_range
        self.page_contents = page_contents
        self.img_urls = img_urls

        self.html_url = html_url
        self.first_page = first_page

    #判断是不是楼主的内容
    def is_louzhu(self, s):
        result = re.search(r'<!-- <div class="host-ico">(.*?)</div> -->', s, re.S)
        return (result is not None)

    #获得页面里属于楼主图片的url
    def get_img_url(self, s, page_url):
        #判断是不是楼主给其他用户的评论，如果是的话，直接过滤掉（本人从不看评论）
        is_louzhu_answer = re.search(r'-{15,}<br>', s, re.S)
        if is_louzhu_answer is None:
            imgurl = re.findall(r'<img.*?original="(?P<imgurl>.*?)".*?/><br>', s, flags = re.S)

            url_path = []
            for one_url in imgurl:
                self.img_urls.put(one_url + '|' + page_url)
                path = re.search('\w+\.jpg', one_url).group(0)
                url_path.append('img/' + path)

            segments = re.split(r'<img .*?/><br>', s.strip())
            content = segments[0].strip()
            for i in range(len(url_path)):
                content += '\n<img src = "' + url_path[i] + '" />\n<br>'
                content += segments[i+1].strip()
            return content

    #解析夜歌页面
    def parse_page(self, html_page, page_url):
        html_page.decode('utf-8')
        Items = re.findall(r'<div class="atl-content">(?P<islouzhu>.+?)<div class="bbs-content.*?">(?P<content>.+?)</div>', html_page, re.S)
        page_content = ''

        for item in Items:
            if self.is_louzhu(item[0]):
                one_div = self.get_img_url(item[1], page_url)
                if one_div is not None:
                    page_content += one_div
        return page_content

    def run(self):
        while self.page_range.qsize() > 0:
            page_number = self.page_range.get()
            page_url = re.sub('-(\d+?)\.shtml', '-' + str(page_number) + '.shtml', self.html_url)

            page_content = ''
            print 'thread %s is downloading %s' % (self.name, page_url)
            if page_url == self.html_url:
                page_content = self.parse_page(self.first_page, page_url)
            else:
                page = download_page(page_url)
                if page is not None:
                    page_content = self.parse_page(page, page_url)
            #thread_lock.acquire()
            #self.page_contents[page_number] = page_content
            #thread_lock.release()
            self.page_contents.put(page_content, page_number)
        self.img_urls.put('finished')

#下载图片的线程
class fetch_img(threading.Thread):
    def __init__(self, name, img_urls, download_img):
        threading.Thread.__init__(self)
        self.name = name
        self.img_urls = img_urls
        self.download_img = download_img

    def run(self):
        while True:
            message = self.img_urls.get().split('|')
            img_url = message[0]
            if img_url == 'finished':
                self.img_urls.put('finished')
                break
            else:
                thread_lock.acquire()
                if img_url in self.download_img:
                    thread_lock.release()
                    continue
                else:
                    thread_lock.release()
                    print 'fetching image %s' % img_url
                    referer = message[1]
                    image = download_image(img_url, referer)

                    image_name = re.search('\w+\.jpg', img_url).group(0)
                    with open(r'img\%s' % image_name, 'wb') as img:
                        img.write(image)
                    thread_lock.acquire()
                    self.download_img.add(img_url)
                    thread_lock.release()

#定义了一个线程池
class thread_pool:
    def __init__(self, page_range, page_contents, html_url, first_page):
        self.page_range = page_range
        self.page_contents = page_contents
        self.img_urls = Queue.Queue()
        self.html_url = html_url
        self.first_page = first_page
        self.download_img = set()

        self.page_thread_pool = []
        self.image_thread_pool = []

    def build_thread(self, page, image):
        for i in range(page):
            t = download_html_page('page thread%d' % i, self.page_range, self.page_contents,
                                    self.img_urls, self.html_url, self.first_page)
            self.page_thread_pool.append(t)
        for i in range(image):
            t = fetch_img('image thread%d' % i, self.img_urls, self.download_img)
            self.image_thread_pool.append(t)

    def all_start(self):
        for t in self.page_thread_pool:
            t.start()
        for t in self.image_thread_pool:
            t.start()

    def all_join(self):
        for t in self.page_thread_pool:
            t.join()
        for t in self.image_thread_pool:
            t.join()
