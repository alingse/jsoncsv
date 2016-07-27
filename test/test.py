
from __future__ import print_function

from jsoncsv.jsoncsv import expand,restore

import json

def log(obj):
    
    print(json.dumps(obj,ensure_ascii=False,indent=1))


def test_one(origin):
    print('the origin:')
    log(origin)

    expobj = expand(origin)
    print('the expobj:')
    log(expobj)

    _origin = restore(expobj)
    print('the restore:')
    log(_origin)

    return _origin


def test_string():
    s = "sss"
    print("test string :",s)
    _s = test_one(s)
    print('equal : ',_s==s)


def test_list():
    s = [1,2,3,4]
    print('test list',s)
    _s = test_one(s)
    print('equal',_s == s)


def test_dict():
    s = {"s":1}
    print('test dict',s)
    _s = test_one(s)
    print('Equal',_s.keys == ["s"] and _s["s"] == 1)

def test_complex():
    s = {"s":1,"t":[1,{"w":2}],"m":[{"w":[0,1,2]},{"m":"n"}]}
    print('test a complex one ',s)
    _s = test_one(s)

if __name__ == '__main__':
    test_string()
    test_list()
    test_dict()
    test_complex()






