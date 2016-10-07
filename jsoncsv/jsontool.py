#!/usr/bin/env python2.7
#coding=utf-8
#author@alingse
#2016.05.27

from itertools import groupby
from operator import itemgetter
import argparse
import json
import sys


def expand(origin,separator='.'):
    def gen_child(obj, head=None):
        exp = {}
        _type = type(obj)
        #the break
        if _type not in [dict,list]:
            key = head
            value = obj
            if head == None:
                key = ''

            _exp = {key:value}
            exp.update(_exp)

        else:
            if _type == dict:
                items = iter(obj.items())
            if _type == list:
                items = enumerate(obj)

            for key,value in items:
                if head == None:
                    _head = '{}'.format(key)
                else:
                    _head = '{}{}{}'.format(head, separator, key)

                _exp = gen_child(value, head = _head)
                exp.update(_exp)

        return exp

    expobj = gen_child(origin)
    return expobj


def restore(expobj,separator='.'):
    def from_child(res_list):
        keys_list, values = zip(*res_list)

        count = len(keys_list)
        #the break
        #the leaf point
        if count == 1:
            #for last value
            if keys_list[0] == []:
                return values[0]
            #for single string obj
            elif keys_list[0][0] == '':
                return values[0]
            #else this is object or array

        key_list = [keys.pop(0) for keys in keys_list]

        zlist = zip(key_list, keys_list, values)
        sort_zlist = sorted(zlist, key=itemgetter(0))
        glist = groupby(sort_zlist, itemgetter(0))

        #check for digit
        key_isdigit = map(lambda key:key.isdigit(),key_list)
        #this is an array
        if all(key_isdigit):
            doc = []
        #this is an object
        elif not any(key_isdigit):
            doc = {}
        else:
            raise Exception('number can not be a key')
        
        for g in glist:
            key, _zlist = g
            #机智,我真是太机智了
            _res_list = map(itemgetter(1, 2), _zlist)
            _doc = from_child(_res_list)

            if type(doc) == list:
                doc.append((int(key), _doc))
            elif type(doc) == dict:
                doc[key] = _doc

        if type(doc) == list:
            #sort by index(the key)
            sort_doc = sorted(doc, key=itemgetter(0))
            #get list doc
            doc = map(itemgetter(1), sort_doc)

        return doc

    res_list = []
    for key, value in expobj.items():
        keys = key.split(separator)
        res_list.append((keys, value))

    origin = from_child(res_list)
    return origin


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e',
                        '--expand',
                        action='store_true',
                        help='choose `expand` a json')
    parser.add_argument('-r',
                        '--restore',
                        action='store_true',
                        help='choose `contract` a ｀expanded` json')
    parser.add_argument('-o',
                        '--output',
                        help='file for output, default is stdout')
    parser.add_argument('input',
                        nargs='?',
                        help='input file, default is stdin')
    args = parser.parse_args()

    if args.expand == args.restore:
        print('can not choose both or choose none, "-e" or "-r"')
        exit()

    if args.input != None:
        fin = open(args.input, 'r')
    else:
        fin = sys.stdin
    if args.output != None:
        fout = open(args.output, 'w')
    else:
        fout = sys.stdout

    if args.expand:
        func = expand
    if args.restore:
        func = restore

    for line in fin:
        obj = json.loads(line)
        new = func(obj)
        out = json.dumps(new, ensure_ascii=False).encode('utf-8')
        fout.write(out)
        fout.write('\n')
