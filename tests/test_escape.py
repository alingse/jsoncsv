# coding=utf-8
# author@alingse
# 2016.11.21

import unittest

from jsoncsv.utils import encode_safe_key, decode_safe_key


class Testescape(unittest.TestCase):

    def test_all(self):
        path = ['A', 'B', '..', '\.\\ww']

        for sep in 'AB.w':
            key = encode_safe_key(path, sep)
            _path = decode_safe_key(key, sep)

        self.assertListEqual(path, _path)

    def test_encode(self):
        path = ['A', 'B', 'C', 'www.xxx.com']
        sep = '.'
        key = encode_safe_key(path, sep)

        self.assertEqual(key, 'A\.B\.C\.www.xxx.com')

    def test_decode(self):
        key = 'A\.B\.C\.www.xxx.com'
        sep = '.'
        path = decode_safe_key(key, sep)

        self.assertEqual(path[0], 'A')
        self.assertEqual(path[1], 'B')
        self.assertEqual(path[2], 'C')
        self.assertEqual(path[3], 'www.xxx.com')
