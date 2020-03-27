# coding=utf-8
# author@alingse
# 2015.10.09

import json

import unicodecsv as csv
import xlwt


class Dump(object):
    def __init__(self, fin, fout, **kwargs):
        self.fin = fin
        self.fout = fout
        self.initialize(**kwargs)

    def initialize(self, **kwargs):
        pass

    def prepare(self):
        pass

    def dump_file(self, obj):
        raise NotImplementedError

    def on_finish(self):
        pass

    def dump(self):
        self.prepare()
        self.dump_file()
        self.on_finish()


class ReadHeadersMixin(object):
    @staticmethod
    def load_headers(fin, read_row=None, sort_type=None):
        headers = set()
        datas = []

        # read
        if not read_row or read_row < 1:
            read_row = -1

        for line in fin:
            obj = json.loads(line)
            headers.update(obj.keys())
            datas.append(obj)

            read_row -= 1
            if not read_row:
                break
        # TODO: add some sort_type here
        headers = sorted(list(headers))

        return (list(headers), datas)


class DumpExcel(Dump, ReadHeadersMixin):
    def initialize(self, **kwargs):
        super(DumpExcel, self).initialize(**kwargs)
        self._read_row = kwargs.get('read_row')
        self._sort_type = kwargs.get('sort_type')

    def prepare(self):
        headers, datas = self.load_headers(self.fin, self._read_row,
                                           self._sort_type)
        self._headers = headers
        self._datas = datas

    def write_headers(self):
        raise NotImplementedError

    def write_obj(self):
        raise NotImplementedError

    def dump_file(self):
        self.write_headers()

        for obj in self._datas:
            self.write_obj(obj)

        for line in self.fin:
            obj = json.loads(line)
            self.write_obj(obj)


class DumpCSV(DumpExcel):
    def initialize(self, **kwargs):
        super(DumpCSV, self).initialize(**kwargs)
        self.csv_writer = None

    def write_headers(self):
        self.csv_writer = csv.DictWriter(self.fout, self._headers)
        self.csv_writer.writeheader()

    def write_obj(self, obj):
        patched_obj = {
            key: self.patch_value(value)
            for key, value in obj.items()
        }
        self.csv_writer.writerow(patched_obj)

    def patch_value(self, value):
        if value in (None, {}, []):
            return ""
        return value


class DumpXLS(DumpExcel):
    def initialize(self, **kwargs):
        super(DumpXLS, self).initialize(**kwargs)

        self.sheet = kwargs.get('sheet', 'Sheet1')
        self.wb = xlwt.Workbook(encoding='utf-8')
        self.ws = self.wb.add_sheet(self.sheet)
        self.row = 0
        self.cloumn = 0

    def write_headers(self):
        for head in self._headers:
            self.ws.write(self.row, self.cloumn, head)
            self.cloumn += 1
        self.row += 1

    def write_obj(self, obj):
        self.cloumn = 0

        for head in self._headers:
            value = obj.get(head)
            # patch
            if value in ({},):
                value = "{}"
            self.ws.write(self.row, self.cloumn, value)
            self.cloumn += 1

        self.row += 1

    def on_finish(self):
        self.wb.save(self.fout)


def dump_excel(fin, fout, klass, **kwargs):
    if not isinstance(klass, type) or not issubclass(klass, DumpExcel):
        raise ValueError("unknow dumpexcel type")

    dump = klass(fin, fout, **kwargs)
    dump.dump()
