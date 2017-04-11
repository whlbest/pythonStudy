# -*- coding: utf-8 -*-



if __name__=='__main__':
    dictstr={}
    with open('erp_pin.txt') as f:
        for line in f:
            lines=line.split(',')
            dictstr[lines[0]]=lines[1]

    print len(dictstr.keys())
