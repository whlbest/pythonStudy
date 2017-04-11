# -*- coding: utf-8 -*-
import threadpool
import time

__author__ = 'wanghaolong'

def func(msg):
    print "msg:", msg
    time.sleep(3)
    print "end"
    # return "done" + msg

if __name__=='__main__':

    data=range(1,10)
    print_result=[]
    pool = threadpool.ThreadPool(10) #建立线程池，控制线程数量为10
    reqs = threadpool.makeRequests(func, data) #构建请求，get_title为要运行的函数，data为要多线程执行函数的参数，最后这个print_result是可选的，是对前两个函数运行结果的操作
    [pool.putRequest(req) for req in reqs] #多线程一块执行
    pool.wait() #线程挂起，直到结束

    # print print_result