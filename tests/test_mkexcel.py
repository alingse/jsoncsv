# coding=utf-8
# author@alingse
# 2018.03.29

import unittest

from jsoncsv.dumptool import dumpexcel


class Testdumptool(unittest.TestCase):

    # FIXME (使用虚拟文件)
    def test_dumpexcel_csv(self):
        fin = open('./fixture/files/expand.1.json', 'r')
        fout = open('./fixture/files/tmp.output.1.csv', 'w')

        dumpexcel(fin, fout, 'csv')
        fin.close()
        fout.close()

        output = open('./fixture/files/output.1.csv', 'r')
        fout = open('./fixture/files/tmp.output.1.csv', 'r')

        self.assertEqual(output.read(), fout.read())

        output.close()
        fout.close()

    def test_dumpexcel_csv_with_sort(self):
        fin = open('./fixture/files/expand.1.json', 'r')
        fout = open('./fixture/files/tmp.output.1.sort.csv', 'w')

        dumpexcel(fin, fout, 'csv', sort_type=True)
        fin.close()
        fout.close()

        output = open('./fixture/files/output.1.sort.csv', 'r')
        fout = open('./fixture/files/tmp.output.1.sort.csv', 'r')

        self.assertEqual(output.read(), fout.read())

        output.close()
        fout.close()

    def test_dumpcexcel_xls(self):
        fin = open('./fixture/files/expand.1.json', 'r')
        fout = open('./fixture/files/tmp.output.1.xls', 'wb')

        dumpexcel(fin, fout, 'xls')

        fin.close()
        fout.close()
