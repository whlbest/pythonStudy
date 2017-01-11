# -*- coding: utf-8 -*-
import multiprocessing
import random
import time
from multiprocessing import Queue

__author__ = 'wanghaolong'

def write(q):
    with open('test.txt') as f:
        for line in f:
    # for value in ['A', 'B', 'C']:
    #         print 'Put %s to queue...' % line
            q.put(line)
        # time.sleep(random.random())
# 读数据进程执行的代码:
def read(q):
    with open('b.txt','a+') as f:
        while True:
            if not q.empty():
                value = q.get(False)
                f.write(value)
                print 'Get %s from queue.' % value
                # time.sleep(random.random())
            else:
                break
            # print 'Get %s from queue.' % value
if __name__=='__main__':
    # 父进程创建Queue，并传给各个子进程：
    manager = multiprocessing.Manager()
    # 父进程创建Queue，并传给各个子进程：
    q = manager.Queue()
    # p = multiprocessing.Pool()
    p = multiprocessing.Pool(processes = 4)
    pw = p.apply_async(write,args=(q,))
    time.sleep(0.5)
    pr = p.apply_async(read,args=(q,))
    p.close()
    p.join()

    print '所有数据都写入并且读完'