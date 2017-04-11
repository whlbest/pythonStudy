# -*- coding: utf-8 -*-
__author__ = 'wanghaolong'




characters=[]
stat={}
with open("xi.txt") as fr:


    for line in fr:
        # 去掉每一行两边的空白
        line = line.strip()

        # 如果为空行则跳过该轮循环
        if len(line) == 0:
            continue

        # 将文本转为unicode，便于处理汉字
        # line = unicode(line)

        # 遍历该行的每一个字
        for x in xrange(0, len(line)):
            # 去掉标点符号和空白符
            if line[x] in [' ', '\t', '\n', '。', '，', '(', ')', '（', '）', '：', '□', '？', '！', '《', '》', '、', '；', '“', '”', '……']:
                continue

            # 尚未记录在characters中
            if not line[x] in characters:
                characters.append(line[x])

            # 尚未记录在stat中
            if not stat.has_key(line[x]):
                stat[line[x]] = 0
            # 汉字出现次数加1
            stat[line[x]] += 1

    print characters
    print len(stat)