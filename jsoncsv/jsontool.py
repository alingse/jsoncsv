# coding=utf-8
# author@alingse
# 2016.05.27

from itertools import groupby
from operator import itemgetter


def expand(origin, separator='.'):
    def gen_child(obj, head=None):
        exp = {}
        _type = type(obj)
        # the break
        if _type not in (dict, list):
            key = head
            value = obj
            if head is None:
                key = ''

            _exp = {key: value}
            exp.update(_exp)
        else:
            if _type == dict:
                items = iter(obj.items())
            if _type == list:
                items = enumerate(obj)

            for key, value in items:
                if head is None:
                    _head = '{}'.format(key)
                else:
                    _head = '{}{}{}'.format(head, separator, key)

                _exp = gen_child(value, head=_head)
                exp.update(_exp)

        return exp

    expobj = gen_child(origin)
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
