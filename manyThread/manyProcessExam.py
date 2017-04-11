# -*- coding: utf-8 -*-
import multiprocessing


import os
import time
from multiprocessing import Pool

def getFile(path) :
  #获取目录下的文件list
  fileList = []
  for root, dirs, files in list(os.walk(path)) :
    for i in files :
      if i.endswith('.txt') or i.endswith('.10w') :
        fileList.append(root + "\\" + i)
  return fileList

def operFile(filePath) :
  #统计每个文件中行数和字符数，并返回
  filePath = filePath
  fp = open(filePath)
  content = fp.readlines()
  fp.close()
  lines = len(content)
  alphaNum = 0
  for i in content :
    alphaNum += len(i.strip('\n'))
  return lines,alphaNum,filePath

def out(list1, writeFilePath) :
  #将统计结果写入结果文件中
  fileLines = 0
  charNum = 0
  fp = open(writeFilePath,'a')
  for i in list1 :
    fp.write(i[2] + " 行数："+ str(i[0]) + " 字符数："+str(i[1]) + "\n")
    fileLines += i[0]
    charNum += i[1]
  fp.close()
  print fileLines, charNum

if __name__ == "__main__":
  #创建多个进程去统计目录中所有文件的行数和字符数
  filePathdata="D:\\txt"
  writeFilePath="D:\\txt\\result.txt"

  startTime = time.time()
  filePath = filePathdata
  fileList = getFile(filePath)
  pool =multiprocessing.Pool(processes=5)
  resultList =pool.map(operFile, fileList)
  pool.close()
  pool.join()


  writeFilePath =writeFilePath
  print resultList
  out(resultList, writeFilePath)
  endTime = time.time()
  print "used time is ", endTime - startTime