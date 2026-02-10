# author@alingse
# 2016.08.09

import io
import unittest

from jsoncsv.jsontool import convert_json, expand, is_array_index, restore


class TestJSONTool(unittest.TestCase):

    def test_string(self):
        s = "sss"
        exp = expand(s)
        _s = restore(exp)
        self.assertEqual(s, _s)

    def test_list(self):
        s = ["sss", "ttt", 1, 2, ["3"]]
        exp = expand(s)
        _s = restore(exp)

        self.assertListEqual(s, _s)

    def test_dict(self):
        s = {
            "s": 1,
            "w": 5,
            "t": {
                "m": 0,
                "x": {
                    "y": "z"
                },
            },
        }

        exp = expand(s)
        _s = restore(exp)

        self.assertDictEqual(s, _s)

    def test_complex(self):
        s = [
            {"s": 0},
            {"t": ["2", {"x": "z"}]},
            0,
            "w",
            ["x", "g", 1]
        ]
        exp = expand(s)
        _s = restore(exp)

        self.assertDictEqual(s[0], _s[0])
        self.assertDictEqual(s[1], _s[1])

        self.assertEqual(s[2], _s[2])
        self.assertEqual(s[3], _s[3])

        self.assertListEqual(s[4], _s[4])

    def test_is_array_index(self):
        self.assertTrue(is_array_index([0, 1, 2, 3]))
        self.assertTrue(is_array_index(['0', '1', '2', '3']))
        # string order
        self.assertTrue(is_array_index(['0', '1', '10', '2', '3', '4', '5', '6', '7', '8', '9']))
        self.assertFalse(is_array_index([1, 2, 3]))
        self.assertFalse(is_array_index(['0', 1, 2]))

    def test_unicode(self):
        data = [
            {"河流名字": "长江", "河流长度": "6000千米"},
            {"河流名字": "黄河", "河流长度": "5000千米"}
        ]

        expobj = expand(data)
        assert expobj

    def test_expand_with_safe(self):
        data = {
            "www.a.com": {"qps": 100, "p95": 20},
            "api.a.com": {"qps": 100, "p95": 20, "p99": 100},
        }
        expobj = expand(data, safe=True)
        self.assertEqual(expobj['api.a.com\\.p95'], 20)
        self.assertEqual(expobj['api.a.com\\.p99'], 100)

        origin = restore(expobj, safe=True)
        self.assertEqual(origin, data)

    def test_expand_and_restore(self):
        data = ["a", "ab", "b"] * 4
        expobj = expand(data)
        self.assertEqual(expobj["0"], "a")
        self.assertEqual(expobj["1"], "ab")

        origin = restore(expobj)
        self.assertEqual(data, origin)


class TestConvertJSON(unittest.TestCase):

    def test_convert_expand(self):
        fin = io.StringIO('{"a":{"b":3}}\n{"a":{"c":4}}\n')
        fout = io.StringIO()

        convert_json(fin, fout, expand)

        self.assertEqual('{"a.b": 3}\n{"a.c": 4}\n', fout.getvalue())

        fin.close()
        fout.close()

    def test_convert_with_unicode(self):
        fin = io.StringIO('{"河流":{"长度":3}}\n{"河流":{"名字":"长江"}}\n')
        fout = io.StringIO()

        convert_json(fin, fout, expand)

        self.assertEqual('{"河流.长度": 3}\n{"河流.名字": "长江"}\n', fout.getvalue())

        fin.close()
        fout.close()

    def test_convert_restore(self):
        fin = io.StringIO('{"a.b": 3}\n{"a.c": 4}\n')
        fout = io.StringIO()

        convert_json(fin, fout, restore)

        self.assertEqual('{"a": {"b": 3}}\n{"a": {"c": 4}}\n', fout.getvalue())

        fin.close()
        fout.close()

    def test_convert_expand_json_array(self):
        fin = io.StringIO('[{"a":{"b":3}},{"a":{"c":4}}]')
        fout = io.StringIO()

        convert_json(fin, fout, expand, json_array=True)

        self.assertEqual('{"a.b": 3}\n{"a.c": 4}\n', fout.getvalue())

        fin.close()
        fout.close()
