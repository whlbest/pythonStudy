# -*- coding: utf-8 -*-
import multiprocessing
import random
import time

__author__ = 'wanghaolong'

def mycallback(x):
    with open('file.txt', 'a+') as f:
        f.writelines(str(x))
        f.write('\n')


def sayHi(num):

    time.sleep(random.randint(0, 5))

    return num

if __name__ == '__main__':


    # num = multiprocessing.Value('d', 0.0)
    # arr = multiprocessing.Array('i', range(10))
    #
    # print num.value
    # print arr[:]




    # e1 = time.time()
    # pool=multiprocessing.Pool(processes = 2)
    #
    # for i in range(10):
    #     pool.apply_async(sayHi, (i,), callback=mycallback)
    # pool.close()
    # pool.join()
    # e2 = time.time()
    # print float(e2 - e1)

