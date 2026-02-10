# author@alingse
# 2016.05.27

import io
import json
from copy import deepcopy
from itertools import groupby
from operator import itemgetter
from typing import Callable, Iterable, Iterator, List, Optional, Union

from jsoncsv.utils import DecodedPathType, JsonType, LeafInputType, LeafType, PathType, decode_safe_key, encode_safe_key

__all__ = [
    'convert_json',
    'expand',
    'restore',
]

# Type alias for the func parameter in convert_json
# Use ... to indicate additional keyword arguments are accepted
ConvertFunc = Union[
    Callable[..., dict[str, JsonType]],  # expand signature
    Callable[..., JsonType],             # restore signature
]


def gen_leaf(root: JsonType, path: Optional[PathType] = None) -> Iterator[LeafType]:
    if path is None:
        path = []

    if not isinstance(root, (dict, list)) or not root:
        leaf: LeafType = (path, root)
        yield leaf
    else:
        items = root.items() if isinstance(root, dict) else enumerate(root)

        for key, value in items:
            _path = deepcopy(path)
            _path.append(key)
            for leaf in gen_leaf(value, _path):
                yield leaf


def is_array_index(keys: Iterable[Union[int, str]], enable_str: bool = True) -> bool:
    keys = list(deepcopy(keys))
    # 不强调有序
    key_map = dict.fromkeys(keys, True)
    int_keys = range(len(keys))

    if all(key in key_map for key in int_keys):
        return True

    return bool(enable_str and all(str(key) in key_map for key in int_keys))


def from_leaf(leafs: Iterable[LeafInputType]) -> JsonType:
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

    child: list[tuple[Union[int, str], JsonType]] = []
    for g in glist:
        head, _zlist = g
        _leafs = map(_get_leaf, _zlist)
        _child = from_leaf(_leafs)
        child.append((head, _child))

    child_keys = map(_get_head, child)
    if is_array_index(child_keys):
        child.sort(key=lambda x: int(x[0]))
        return list(map(_get_leaf, child))

    return dict(child)  # type: ignore[arg-type]


def expand(origin: JsonType, separator: str = '.', safe: bool = False) -> dict[str, JsonType]:
    root = origin
    leafs = gen_leaf(root)

    expobj: dict[str, JsonType] = {}
    for path, value in leafs:
        # Convert path elements to strings
        str_path: List[str] = [str(p) for p in path]

        key = encode_safe_key(str_path, separator) if safe else separator.join(str_path)
        expobj[key] = value

    return expobj


def restore(expobj: dict[str, JsonType], separator: str = '.', safe: bool = False) -> JsonType:
    leafs: list[tuple[DecodedPathType, JsonType]] = []

    items = expobj.items()

    for key, value in items:
        path: DecodedPathType = decode_safe_key(key, separator) if safe else key.split(separator)

        if key == '':
            path = []

        leafs.append((path, value))

    origin = from_leaf(leafs)
    return origin


def convert_json(
    fin: io.TextIOBase,
    fout: io.TextIOBase,
    func: ConvertFunc,
    separator: str = '.',
    safe: bool = False,
    json_array: bool = False,
) -> None:
    '''
    ensure fin/fout is TextIO
    '''

    if func not in [expand, restore]:
        raise ValueError("unknow convert_json type")

    # default: read json objects from each line
    def gen_objs() -> Iterator[JsonType]:
        for line in fin:
            obj = json.loads(line)
            yield obj

    objs = gen_objs()

    if json_array:
        # read all input as json array
        def gen_objs_from_array() -> Iterator[JsonType]:
            objs = json.load(fin)
            assert isinstance(objs, list)
            yield from objs

        objs = gen_objs_from_array()

    for obj in objs:
        new = func(obj, separator=separator, safe=safe)
        content = json.dumps(new, ensure_ascii=False)
        fout.write(content)
        fout.write('\n')
