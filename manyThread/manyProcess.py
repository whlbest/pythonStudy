# -*- coding: utf-8 -*-
from datetime import datetime
import time
from multiprocessing import Process
import multiprocessing

import multiprocessing
import time

def func(msg):
    print "msg:", msg
    time.sleep(3)
    print "end"
    return "done" + msg


def foo(i,a):
    print 'say hi',i,a




def do(msg):
    maps={}
    name=multiprocessing.current_process().name
    print name,'start',msg
    # time.sleep(2)
    print name,'end'
    maps[msg]='message'+str(msg)
    return maps


def manyProce():
    pool=multiprocessing.Pool(processes = 2)
    liststr=[]
    for i in xrange(100):
        msg = "hello %d" %(i)
        #将结果存储到列表中,非阻塞调用
        liststr.append(pool.apply_async(do, (msg,)))
    pool.close()
    pool.join()
    #遍历列表
    for a in liststr:
        temp=a.get()
        for key in temp.keys():
            print key
    # print liststr
def manyProcMap():
    pool=multiprocessing.Pool(processes = 4)
    msgList=xrange(1,100)
    pool.map(do,msgList)

def manyProceResust():
    pool = multiprocessing.Pool(processes=4)
    result = []
    for i in xrange(3):
        msg = "hello %d" %(i)
        result.append(pool.apply_async(func, (msg, )))
    pool.close()
    pool.join()
    for res in result:
        print ":::", res.get()
    print "Sub-process(es) done."

if __name__=='__main__':
##################################################################################

###################################################################################

    for i in range(10):
        p = Process(target=foo,args=(i,i,))
        p.start()
    # manyProceResust()
    # # manyProce()
    # starttime=time.time()
    # # manyProcMap()
    # manyProce()
    # endtime=time.time()
    # print  '------------------------------',endtime-starttime