# coding=utf-8
# author@alingse
# 2015.10.09

import json
import xlwt


class Dump(object):

    def __init__(self, fin, fout, **kwargs):
        self.fin = fin
        self.fout = fout
        self.datas = []
        self.headers = set()

        self.initialize(**kwargs)

    def initialize(self, **kwargs):
        pass

    def patch(self, value):
        if value is None:
            return ''

        if isinstance(value, basestring):
            return value.encode('utf-8')

        if value == {} or value == []:
            return ''

        return value

    def load_headers(self, read_row=None):
        i = 0
        for line in self.fin:
            obj = json.loads(line)
            map(self.headers.add, obj.iterkeys())
            self.datas.append(obj)
            if read_row is not None and i >= read_row:
                break

    def write_headers(self):
        raise NotImplementedError

    def write_obj(self, obj):
        raise NotImplementedError

    def on_finish(self):
        pass

    def dump_file(self):
        if self.datas:
            map(self.write_obj, self.datas)

        for line in self.fin:
            obj = json.loads(line)
            self.write_obj(obj)

    def dump(self):
        self.write_headers()
        self.dump_file()
        self.on_finish()


class DumpCSV(Dump):

    def initialize(self, separator=','):
        self.separator = separator

    def write_headers(self):
        self.headers = list(self.headers)
        content = self.separator.join(self.headers)
        self.fout.write(content)
        self.fout.write('\n')

    def patch(self, value):
        value = super(DumpCSV, self).patch(value)
        return str(value)

    def write_obj(self, obj):
        values = [obj.get(head) for head in self.headers]
        values = map(self.patch, values)
        content = self.separator.join(values)
        self.fout.write(content)
        self.fout.write('\n')


class DumpExcel(Dump):

    def initialize(self, **kwargs):
        self.wb = xlwt.Workbook(encoding='utf-8')
        self.ws = self.wb.add_sheet('Sheet1')
        self.row = 0
        self.cloumn = 0

    def write_headers(self):
        self.headers = list(self.headers)

        for head in self.headers:
            self.ws.write(self.row, self.cloumn, head)
            self.cloumn += 1

    def write_obj(self, obj):
        values = [obj.get(head) for head in self.headers]
        values = map(self.patch, values)

        self.row += 1
        self.cloumn = 0
        for value in values:
            self.ws.write(self.row, self.cloumn, value)
            self.cloumn += 1

    def on_finish(self):
        self.wb.save(self.fout)


def dumpfile(fin, fout, type_, read_row=None):
    if type_ == 'csv':
        DumpKlass = DumpCSV
    elif type_ == 'xls':
        DumpKlass = DumpExcel

    dump = DumpKlass(fin, fout)
    dump.load_headers(read_row)
    dump.dump()
