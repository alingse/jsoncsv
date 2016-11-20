# coding=utf-8
# author@alingse
# 2016.05.27

from copy import deepcopy
from itertools import groupby
from operator import itemgetter

from utils import encode_safe_key
from utils import decode_safe_key


__all__ = [
    'expand',
    'restore',
    'gen_leaf',
    'from_leaf',
]


def gen_leaf(root, path=None):
    if path is None:
        path = []

    # the leaf
    if not isinstance(root, (dict, list)) or not root:
        leaf = (path, root)
        yield leaf
    else:
        if isinstance(root, dict):
            items = root.iteritems()
        else:
            items = enumerate(root)

        for key, value in items:
            _path = deepcopy(path)
            _path.append(key)
            for leaf in gen_leaf(value, _path):
                yield leaf


int_digit = lambda x: isinstance(x, int)
str_digit = lambda x: x.isdigit()


def from_leaf(leafs):
    # (path,value),(path, value)
    leafs = list(leafs)
    # leaf
    if len(leafs) == 1:
        path, value = leafs[0]
        if path == []:
            return value

    heads = [leaf[0].pop(0) for leaf in leafs]

    zlist = zip(heads, leafs)
    glist = groupby(sorted(zlist, key=itemgetter(0)), key=itemgetter(0))

    child = []
    for g in glist:
        head, _zlist = g
        _leafs = map(itemgetter(1), _zlist)
        _child = from_leaf(_leafs)
        child.append((head, _child))

    if all(map(int_digit, heads)) or all(map(str_digit, heads)):
        child.sort(key=lambda x: int(x[0]))
        return map(itemgetter(1), child)
    else:
        return dict(child)


def expand(origin, separator='.', safe=False):
    root = origin
    leafs = gen_leaf(root)

    expobj = {}
    for path, value in leafs:
        path = map(str, path)
        if safe:
            key = encode_safe_key(path, separator)
        else:
            key = separator.join(path)
        expobj[key] = value

    return expobj


def restore(expobj, separator='.', safe=False):
    leafs = []

    for key, value in expobj.iteritems():
        if safe:
            path = decode_safe_key(key, separator)
        else:
            path = key.split(separator)

        # separator.join(path)
        if key == '':
            path = []

        leafs.append((path, value))

    origin = from_leaf(leafs)
    return origin
