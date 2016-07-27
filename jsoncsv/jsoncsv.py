#!/usr/bin/env python2.7
#coding=utf-8
#author@alingse
#2016.05.27

from __future__ import print_function
import json
import argparse
import sys


def expand_json(json_obj, head = None):
    exp_obj = {}
    if type(json_obj) == dict:
        for key in json_obj:
            if head == None:
                k_head = key
            else:
                k_head = '{}.{}'.format(head,key)

            k_obj = json_obj[key]
            k_exp_obj = expand_json(k_obj,head = k_head)
            exp_obj.update(k_exp_obj)

    elif type(json_obj) == list:
        for i in range(len(json_obj)):
            if head == None:
                i_head = str(i)
            else:
                i_head = '{}.{}'.format(head,i)

            i_obj = json_obj[i]
            i_exp_obj = expand_json(i_obj,head = i_head)
            exp_obj.update(i_exp_obj)

    else:
        if head == None:
            head = ''

        value = json_obj
        exp_obj[head] = value

    return exp_obj
   



def contract_json(exp_obj):
    return exp_obj

'''
    #[(['s','t'],1),...]
    def from_keys():
        pass


    class Empty(object):
        pass

    def new(keys,value):
        if len(keys) == 0:
            return value
        key = keys[0]
        _doc = newone(keys[1:],value)
        if key == '':
            doc = _doc
        #means list
        if key.isdigit():
            doc = [(int(key),_doc)]
        else:
            doc = {
                key:_doc
            }
        return doc
    
    #is this key in this doc
    def find(key,doc):
        if doc == None:
            return False,None
        if key.isdigit():
            if type(doc) != list:
                raise Exception('number key must use for list')
            for idoc in doc:
                if int(key) == idoc[0]:
                    return True,idoc[1]
            return False,None
        else:
            if type(doc) != dict:
                raise Exception('string key only find in doc')
            if key in doc:
                return True,doc[key]
            return False,None


    def update(keys,value,doc):

    origin_obj = Empty()

    for key in exp_obj:
        keys = key.split('.')
        for _key in keys:
            status,obj = find(_key,origin_obj)
            if status:

        key = 

'''
'''
    json_obj = {}
    for key in exp_obj:
        value = exp_obj[key]
        keys = key.split('.')
        this = json_obj
        for ikey in keys:
            if ikey.isdigit():
                pass
'''
'''
    return exp_obj

'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e','--expand',action='store_true',help='choose `expand` a json')
    parser.add_argument('-c','--contract',action='store_true',help='choose `contract` a ｀expanded` json')    
    parser.add_argument('-o','--output',help='file for output, default is stdout')
    parser.add_argument('input', nargs='?', help='input file, default is stdin')
    args = parser.parse_args()


    if args.expand == args.contract:
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
        func = expand_json
    if args.contract:
        func = contract_json
    for line in fin:
        obj = json.loads(line)
        new = func(obj)
        out = json.dumps(new,ensure_ascii=False).encode('utf-8')
        fout.write(out)
        fout.write('\n')