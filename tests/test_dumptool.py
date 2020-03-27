# coding=utf-8
# author@alingse
# 2018.03.29
import io
import unittest

from jsoncsv.dumptool import DumpCSV
from jsoncsv.dumptool import DumpXLS
from jsoncsv.dumptool import dump_excel


class TestDumpTool(unittest.TestCase):

    # FIXME (使用虚拟文件)
    def test_dumpexcel_csv(self):
        fin = io.open('./fixture/files/expand.1.json', 'r', encoding='utf-8')
        fout = io.open('./fixture/files/tmp.output.1.csv', 'wb')

        dump_excel(fin, fout, DumpCSV)
        fin.close()
        fout.close()

        output = io.open('./fixture/files/output.1.csv', 'r', encoding='utf-8')
        fout = io.open('./fixture/files/tmp.output.1.csv', 'r', encoding='utf-8')

        self.assertEqual(output.read(), fout.read())

        output.close()
        fout.close()

    def test_dumpexcel_csv_with_sort(self):
        fin = io.open('./fixture/files/expand.1.json', 'r', encoding='utf-8')
        fout = io.open('./fixture/files/tmp.output.1.sort.csv', 'wb')

        dump_excel(fin, fout, DumpCSV, sort_type=True)
        fin.close()
        fout.close()

        output = io.open('./fixture/files/output.1.sort.csv', 'r', encoding='utf-8')
        fout = io.open('./fixture/files/tmp.output.1.sort.csv', 'r', encoding='utf-8')

        self.assertEqual(output.read(), fout.read())

        output.close()
        fout.close()

    def test_dumpcexcel_xls(self):
        fin = io.open('./fixture/files/expand.1.json', 'r', encoding='utf-8')
        fout = io.open('./fixture/files/tmp.output.1.xls', 'wb')

        dump_excel(fin, fout, DumpXLS)

        fin.close()
        fout.close()

    def test_dump_csv_with_non_ascii(self):
        fin = io.open('./fixture/files/expand.2.json', 'r', encoding='utf-8')
        fout = io.open('./fixture/files/tmp.output.2.csv', 'wb')

        dump_excel(fin, fout, DumpCSV)

        fin.close()
        fout.close()

    def test_dump_xls_with_non_ascii(self):
        fin = io.open('./fixture/files/expand.2.json', 'r', encoding='utf-8')
        fout = io.open('./fixture/files/tmp.output.2.xls', 'wb')

        dump_excel(fin, fout, DumpXLS)

        fin.close()
        fout.close()

    def test_dump_xls_with_dict(self):
        fin = io.StringIO(u'{"a": {}}\n')
        fout = io.BytesIO()

        dump_excel(fin, fout, DumpXLS)

        fin.close()
        fout.close()

    def test_dump_excel_with_error(self):
        with self.assertRaises(ValueError):
            dump_excel(None, None, None)
