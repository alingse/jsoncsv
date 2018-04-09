# coding=utf-8
# author@alingse
# 2018.03.29

import unittest

from jsoncsv.dumptool import dumpexcel


class Testdumptool(unittest.TestCase):

    def test_dumpexcel_csv(self):
        fin = open('./fixture/expand.json', 'r')
        fout = open('./fixture/output2.csv', 'w')

        dumpexcel(fin, fout, 'csv')
        fin.close()
        fout.close()

        output = open('./fixture/output.csv', 'r')
        fout = open('./fixture/output2.csv', 'r')

        self.assertEqual(output.read(), fout.read())

        output.close()
        fout.close()

    def test_dumpexcel_csv_with_sort(self):
        fin = open('./fixture/expand.json', 'r')
        fout = open('./fixture/tmp.csv', 'w')

        dumpexcel(fin, fout, 'csv', sort_type=True)
        fin.close()
        fout.close()

        output = open('./fixture/output.sort.csv', 'r')
        fout = open('./fixture/tmp.csv', 'r')

        self.assertEqual(output.read(), fout.read())

        output.close()
        fout.close()
