#coding=utf-8
#author@alingse
#2016.08.09

from __future__ import print_function
from jsoncsv import expand,restore

import unittest
import json

class TestJsoncsv(unittest.TestCase):

    def log(self,obj):
        print(json.dumps(obj,ensure_ascii=False,indent=1))

    def test_string(self):
        s = "sss"
        exp = expand(s)
        _s = restore(exp)
        self.assertEqual(s,_s)

    def test_list(self):
        s = ["sss","ttt",1,2,["3"]]
        exp = expand(s)
        _s = restore(exp)
        print('test-list')
        self.log(s)
        self.log(exp)
        self.log(_s)

        self.assertListEqual(s,_s)

    def test_dict(self):
        s = {"s":1,"w":5,"t":{"m":0,"x":{"y":"z"}}}
        exp = expand(s)
        _s = restore(exp)
        self.log(s)
        self.log(exp)
        self.log(_s)
        self.assertDictEqual(s,_s)

    def test_complex(self):
        s = [{"s":0},{"t":["2",{"x":"z"}]},0,"w",["x","g",1]]
        exp = expand(s)
        _s = restore(exp)
        self.log(s)
        self.log(exp)
        self.log(_s)
        
        self.assertDictEqual(s[0],_s[0])
        self.assertDictEqual(s[1],_s[1])

        self.assertEqual(s[2],_s[2])
        self.assertEqual(s[3],_s[3])

        self.assertListEqual(s[4],_s[4])

if __name__ == '__main__':
    unittest.main()
