# coding=utf-8
# author@alingse
# 2016.05.27
from __future__ import absolute_import

from copy import deepcopy
from itertools import groupby
from operator import itemgetter

from jsoncsv import PY3
from jsoncsv.utils import encode_safe_key
from jsoncsv.utils import decode_safe_key


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
            if PY3:
                items = root.items()
            else:
                items = root.iteritems()
        else:
            items = enumerate(root)

        for key, value in items:
            _path = deepcopy(path)
            _path.append(key)
            for leaf in gen_leaf(value, _path):
                yield leaf


def is_array(keys, ensure_str=True):
    copy_keys = list(deepcopy(keys))
    int_keys = list(range(len(copy_keys)))
    if copy_keys == int_keys:
        return True
    if ensure_str:
        str_keys = list(map(str, int_keys))
        if copy_keys == str_keys:
            return True
    return False


def from_leaf(leafs):
    # [(path, value), (path, value)]
    leafs = list(leafs)

    if len(leafs) == 1:
        path, value = leafs[0]
        if path == []:
            return value

    heads = [leaf[0].pop(0) for leaf in leafs]

    _get_head = itemgetter(0)
    _get_leaf = itemgetter(1)

    zlist = list(zip(heads, leafs))
    glist = groupby(sorted(zlist, key=_get_head), key=_get_head)

    child = []
    for g in glist:
        head, _zlist = g
        _leafs = map(_get_leaf, _zlist)
        _child = from_leaf(_leafs)
        child.append((head, _child))

    child_keys = map(_get_head, child)
    if is_array(child_keys):
        child.sort(key=lambda x: int(x[0]))
        return list(map(_get_leaf, child))

    return dict(child)


def expand(origin, separator='.', safe=False):
    root = origin
    leafs = gen_leaf(root)

    expobj = {}
    for path, value in leafs:
        if PY3:
            path = map(str, path)
        else:
            path = map(unicode, path)  # noqa

        if safe:
            key = encode_safe_key(path, separator)
        else:
            key = separator.join(path)
        expobj[key] = value

    return expobj


def restore(expobj, separator='.', safe=False):
    leafs = []

    if PY3:
        items = expobj.items()
    else:
        items = expobj.iteritems()

    for key, value in items:
        if safe:
            path = decode_safe_key(key, separator)
        else:
            path = key.split(separator)

        if key == '':
            path = []

        leafs.append((path, value))

    origin = from_leaf(leafs)
    return origin
