# coding=utf-8
# author@alingse
# 2015.10.09

import json
import xlwt

from jsoncsv import PY3


class Dump(object):

    def __init__(self, fin, fout, **kwargs):
        self.fin = fin
        self.fout = fout
        self.initialize(**kwargs)

    def initialize(self, **kwargs):
        pass

    def patch(self, value):
        if value is None:
            return ''

        if value == {} or value == []:
            return ''

        return value

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
            read_row = 1

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
        headers, datas = self.load_headers(self.fin, self._read_row, self._sort_type)
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

        self._separator = kwargs.get('separator', ',')

    def write_headers(self):
        header = self._separator.join(self._headers)
        if PY3:
            self.fout.write(header)
        else:
            self.fout.write(header.encode('utf-8'))
        self.fout.write('\n')

    def patch(self, value):
        value = super(DumpCSV, self).patch(value)
        if PY3:
            return str(value)
        else:
            return unicode(value)  # noqa

    def write_obj(self, obj):
        values = [
            self.patch(obj.get(head))
            for head in self._headers
        ]
        content = self._separator.join(values)
        if PY3:
            self.fout.write(content)
        else:
            self.fout.write(content.encode('utf-8'))
        self.fout.write('\n')


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
            value = self.patch(obj.get(head))
            self.ws.write(self.row, self.cloumn, value)
            self.cloumn += 1

        self.row += 1

    def on_finish(self):
        self.wb.save(self.fout)


def dumpexcel(fin, fout, type_, **kwargs):
    if type_ == 'csv':
        DumpKlass = DumpCSV
    elif type_ == 'xls':
        DumpKlass = DumpXLS

    dump = DumpKlass(fin, fout, **kwargs)
    dump.dump()
