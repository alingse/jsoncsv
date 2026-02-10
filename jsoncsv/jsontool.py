# author@alingse
# 2016.05.27

import json
from copy import deepcopy
from itertools import groupby
from operator import itemgetter

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
        items = root.items() if isinstance(root, dict) else enumerate(root)

        for key, value in items:
            _path = deepcopy(path)
            _path.append(key)
            for leaf in gen_leaf(value, _path):
                yield leaf


def is_array_index(keys, enable_str=True):
    keys = list(deepcopy(keys))
    # 不强调有序
    key_map = dict.fromkeys(keys, True)
    int_keys = range(len(keys))

    if all(key in key_map for key in int_keys):
        return True

    return bool(enable_str and all(str(key) in key_map for key in int_keys))


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
        path = map(str, path)

        key = encode_safe_key(path, separator) if safe else separator.join(path)
        expobj[key] = value

    return expobj


def restore(expobj, separator='.', safe=False):
    leafs = []

    items = expobj.items()

    for key, value in items:
        path = decode_safe_key(key, separator) if safe else key.split(separator)

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
            yield from objs

        objs = gen_objs_from_array()

    for obj in objs:
        new = func(obj, separator=separator, safe=safe)
        content = json.dumps(new, ensure_ascii=False)
        fout.write(content)
        fout.write('\n')
