# coding=utf-8
# author@alingse
# 2016.05.27
from __future__ import absolute_import, unicode_literals

import json
from copy import deepcopy
from itertools import groupby
from operator import itemgetter

from jsoncsv import PY2
from jsoncsv.utils import decode_safe_key, encode_safe_key

__all__ = [
    'convert_json',
    'expand',
    'restore',
]


def gen_leaf(root, path=None):
    if path is None:
        path = []

    if not isinstance(root, (dict, list)) or not root:
        leaf = (path, root)
        yield leaf
    else:
        if isinstance(root, dict):
            if PY2:
                items = root.iteritems()
            else:
                items = root.items()
        else:
            items = enumerate(root)

        for key, value in items:
            _path = deepcopy(path)
            _path.append(key)
            for leaf in gen_leaf(value, _path):
                yield leaf


def is_array_index(keys, enable_str=True):
    keys = list(deepcopy(keys))
    # 不强调有序
    key_map = {key: True for key in keys}
    int_keys = range(len(keys))

    if all(key in key_map for key in int_keys):
        return True

    if enable_str:
        if all(str(key) in key_map for key in int_keys):
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
    if is_array_index(child_keys):
        child.sort(key=lambda x: int(x[0]))
        return list(map(_get_leaf, child))

    return dict(child)


def expand(origin, separator='.', safe=False):
    root = origin
    leafs = gen_leaf(root)

    expobj = {}
    for path, value in leafs:
        if PY2:
            path = map(unicode, path)  # noqa
        else:
            path = map(str, path)

        if safe:
            key = encode_safe_key(path, separator)
        else:
            key = separator.join(path)
        expobj[key] = value

    return expobj


def restore(expobj, separator='.', safe=False):
    leafs = []

    if PY2:
        items = expobj.iteritems()
    else:
        items = expobj.items()

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


def convert_json(fin, fout, func, separator=".", safe=False, json_array=False):
    '''
    ensure fin/fout is TextIO
    '''

    if func not in [expand, restore]:
        raise ValueError("unknow convert_json type")

    # default: read json objects from each line
    def gen_objs():
        for line in fin:
            obj = json.loads(line)
            yield obj

    objs = gen_objs()

    if json_array:
        # read all input as json array
        def gen_objs_from_array():
            objs = json.load(fin)
            assert isinstance(objs, list)
            for obj in objs:
                yield obj

        objs = gen_objs_from_array()

    for obj in objs:
        new = func(obj, separator=separator, safe=safe)
        content = json.dumps(new, ensure_ascii=False)
        fout.write(content)
        fout.write('\n')
