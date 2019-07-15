# coding=utf-8
# author@alingse
# 2018.03.29

import unittest

from jsoncsv.dumptool import DumpCSV
from jsoncsv.dumptool import DumpXLS
from jsoncsv.dumptool import dump_excel


class TestDumpTool(unittest.TestCase):

    # FIXME (使用虚拟文件)
    def test_dumpexcel_csv(self):
        fin = open('./fixture/files/expand.1.json', 'r')
        fout = open('./fixture/files/tmp.output.1.csv', 'wb')

        dump_excel(fin, fout, DumpCSV)
        fin.close()
        fout.close()

        output = open('./fixture/files/output.1.csv', 'r')
        fout = open('./fixture/files/tmp.output.1.csv', 'r')

        self.assertEqual(output.read(), fout.read())

        output.close()
        fout.close()

    def test_dumpexcel_csv_with_sort(self):
        fin = open('./fixture/files/expand.1.json', 'r')
        fout = open('./fixture/files/tmp.output.1.sort.csv', 'wb')

        dump_excel(fin, fout, DumpCSV, sort_type=True)
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

        dump_excel(fin, fout, DumpXLS)

        fin.close()
        fout.close()

    def test_dump_csv_with_non_ascii(self):
        fin = open('./fixture/files/expand.2.json', 'r')
        fout = open('./fixture/files/tmp.output.2.csv', 'wb')

        dump_excel(fin, fout, DumpCSV)

        fin.close()
        fout.close()

    def test_dump_xls_with_non_ascii(self):
        fin = open('./fixture/files/expand.2.json', 'r')
        fout = open('./fixture/files/tmp.output.2.xls', 'wb')

        dump_excel(fin, fout, DumpXLS)

        fin.close()
        fout.close()
