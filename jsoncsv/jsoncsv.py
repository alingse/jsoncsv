#!/usr/bin/env python2.7
#coding=utf-8
#author@alingse
#2016.05.27

from itertools import groupby
from operator import itemgetter
import json
import argparse
import sys


def expand(origin):
    #gen net obj keys
    def gen_next(obj,head=None):
        exp = {}
        if type(obj) == dict:
            for key in obj:
                if head == None:
                    k_head = key
                else:
                    k_head = '{}.{}'.format(head,key)

                k_obj = obj[key]
                k_exp = gen_next(k_obj, head=k_head)
                exp.update(k_exp)
        elif type(obj) == list:
            for i,i_obj in enumerate(obj):
                if head == None:
                    #this is important,so the json forbidden number key
                    i_head = str(i)
                else:
                    i_head = '{}.{}'.format(head,i)

                i_exp = gen_next(i_obj, head=i_head)
                exp.update(i_exp)
        else:
            if head == None:
                head = ''

            value = obj
            _exp = {head:value}

            exp.update(_exp)

        return exp

    expobj = gen_next(origin,head=None)
    return expobj
   

def restore(expobj):

    def from_child(res_list):
        keys_list,values=zip(*res_list)
        N = len(keys_list)
        #the break
        #this group only one
        if N == 1:
            if keys_list[0] == []:
                #return the value
                return values[0]
            #for single string obj
            elif keys_list[0][0] == '':
                return values[0]

        key_list = [keys.pop(0) for keys in keys_list]
        #应该还有其他的检查 assert 等。raise Exception

        zlist = zip(key_list,keys_list,values)
        sort_zlist = sorted(zlist,key=itemgetter(0))
        glist = groupby(sort_zlist,itemgetter(0))

        #check for digit
        digit_list = filter(lambda x:x.isdigit(),key_list)
        #this is an array
        if len(digit_list) == N:
            doc = []
        elif len(digit_list) == 0:
            doc = {}
        else:
            raise Exception('number can not be a key')

        for g in glist:
            key,_zlist = g
            #机智,我真是太机智了
            _res_list = map(itemgetter(1,2),_zlist)
            _doc = from_child(_res_list)
            if type(doc) == list:
                doc.append((int(key),_doc))
            elif type(doc) == dict:
                doc[key] = _doc

        if type(doc) == list:
            #sort by index(the key)
            sort_tmp = sorted(doc,key=itemgetter(0))
            #get list doc
            doc = map(itemgetter(1),sort_tmp)
        
        return doc

    res_list = []
    for key,value in expobj.items():
        keys = key.split('.')
        res_list.append((keys,value))

    origin = from_child(res_list)
    return origin


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e','--expand',action='store_true',help='choose `expand` a json')
    parser.add_argument('-r','--restore',action='store_true',help='choose `contract` a ｀expanded` json')    
    parser.add_argument('-o','--output',help='file for output, default is stdout')
    parser.add_argument('input', nargs='?', help='input file, default is stdin')
    args = parser.parse_args()

    if args.expand == args.restore:
        print('can not choose two or choose none')
        exit()

    if args.output != None:
        fout = open(args.output,'w')
    else:
        fout = sys.stdout
    if args.input != None:
        fin = open(args.input,'r')
    else:
        fin = sys.stdin
        

    if args.expand:
        func = expand
    if args.restore:
        func = restore

    for line in fin:
        obj = json.loads(line)
        new = func(obj)
        out = json.dumps(new,ensure_ascii=False).encode('utf-8')
        fout.write(out)
        fout.write('\n')