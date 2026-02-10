# author@alingse
# 2018.03.29
import io
import unittest

from jsoncsv.dumptool import DumpCSV, DumpXLS, dump_excel


class TestDumpTool(unittest.TestCase):

    # FIXME (使用虚拟文件)
    def test_dumpexcel_csv(self):
        with open('./fixture/files/expand.1.json', encoding='utf-8') as fin, \
                open('./fixture/files/tmp.output.1.csv', 'w', encoding='utf-8', newline='') as fout:
            dump_excel(fin, fout, DumpCSV)

        with open('./fixture/files/output.1.csv', encoding='utf-8') as output, \
                open('./fixture/files/tmp.output.1.csv', encoding='utf-8') as fout:
            self.assertEqual(output.read(), fout.read())

    def test_dumpexcel_csv_with_sort(self):
        with open('./fixture/files/expand.1.json', encoding='utf-8') as fin, \
                open('./fixture/files/tmp.output.1.sort.csv', 'w', encoding='utf-8', newline='') as fout:
            dump_excel(fin, fout, DumpCSV, sort_type=True)

        with open('./fixture/files/output.1.sort.csv', encoding='utf-8') as output, \
                open('./fixture/files/tmp.output.1.sort.csv', encoding='utf-8') as fout:
            self.assertEqual(output.read(), fout.read())

    def test_dumpcexcel_xls(self):
        with open('./fixture/files/expand.1.json', encoding='utf-8') as fin, \
                open('./fixture/files/tmp.output.1.xls', 'wb') as fout:
            dump_excel(fin, fout, DumpXLS)

    def test_dump_csv_with_non_ascii(self):
        with open('./fixture/files/expand.2.json', encoding='utf-8') as fin, \
                open('./fixture/files/tmp.output.2.csv', 'w', encoding='utf-8', newline='') as fout:
            dump_excel(fin, fout, DumpCSV)

    def test_dump_xls_with_non_ascii(self):
        with open('./fixture/files/expand.2.json', encoding='utf-8') as fin, \
                open('./fixture/files/tmp.output.2.xls', 'wb') as fout:
            dump_excel(fin, fout, DumpXLS)

    def test_dump_xls_with_dict(self):
        fin = io.StringIO('{"a": {}}\n')
        fout = io.BytesIO()

        dump_excel(fin, fout, DumpXLS)

        fin.close()
        fout.close()

    def test_dump_excel_with_error(self):
        with self.assertRaises(ValueError):
            dump_excel(None, None, None)
