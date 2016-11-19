# coding=utf-8
# author@alingse
# 2016.05.27

from itertools import groupby
from collections import Iterable
from operator import itemgetter
from copy import deepcopy


def gen_leaf(root, path=None):
    if path == None:
        path = []

    # the leaf
    if not isinstance(root, Iterable):
        leaf = (path, root)
        yield leaf
    else:
        if type(root) == dict:
            items = root.iteritems()
        else:
            items = enumerate(root)
        
        for key, value in items:
            _path = deepcopy(path)
            _path.append(key)
            for leaf in gen_leaf(value, _path):
                yield leaf


def from_leaf(leafs):    
    pass

def expand(origin, separator='.'):

    root = origin
    leafs = gen_leaf(root)

    expobj = {}
    for path, value in leafs:
        path = map(str, path)
        key = separator.join(path)
        expobj[key] = value

    return expobj


def restore(expobj, separator='.'):
    def from_child(res_list):
        keys_list, values = zip(*res_list)

        if len(keys_list) == 1:
            # break at the leaf point
            # last value
            if keys_list[0] == []:
                return values[0]
            # or single string obj
            elif keys_list[0][0] == '':
                return values[0]

        key_list = [keys.pop(0) for keys in keys_list]

        zlist = zip(key_list, keys_list, values)
        sort_zlist = sorted(zlist, key=itemgetter(0))
        glist = groupby(sort_zlist, itemgetter(0))

        if all(map(str.isdigit, key_list)):
            # this is an array
            _type = list
            doc = []
        else:
            # this is an object
            _type = dict
            doc = {}

        for g in glist:
            key, _zlist = g
            _res_list = map(itemgetter(1, 2), _zlist)
            _doc = from_child(_res_list)

            if _type == list:
                doc.append((int(key), _doc))
            elif _type == dict:
                doc[key] = _doc

        if _type == list:
            # sort by index
            sort_doc = sorted(doc, key=itemgetter(0))
            doc = map(itemgetter(1), sort_doc)

        return doc

    res_list = []
    for key, value in expobj.items():
        keys = key.split(separator)
        res_list.append((keys, value))

    origin = from_child(res_list)
    return origin
