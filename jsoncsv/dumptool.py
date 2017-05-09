# coding=utf-8
# author@alingse
# 2015.10.09

import json
import xlwt


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

        if isinstance(value, basestring):
            return value.encode('utf-8')

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

    def load_headers(fin, read_row=None):
        headers = set()
        datas = []

        if not read_row or read_row < 1:
            read_row = 1

        for line in fin:
            obj = json.loads(line)

            headers.update(obj.iterkeys())
            datas.append(obj)

            read_row -= 1
            if not read_row:
                break

        return (headers, datas)


class DumpExcel(Dump, ReadHeadersMixin):

    def initialize(self, **kwargs):
        super(DumpExcel, self).initialize(**kwargs)
        self.read_row = kwargs.get('read_row')

    def prepare(self):
        headers, datas = self.load_headers(self.fin, self.read_row)
        self.headers = headers
        self.datas = datas

    def write_headers(self):
        raise NotImplementedError

    def write_obj(self):
        raise NotImplementedError

    def dump_file(self):
        self.write_headers()

        for obj in self.datas:
            self.write_obj(obj)

        for line in self.fin:
            obj = json.loads(line)
            self.write_obj(obj)


class DumpCSV(DumpExcel):

    def initialize(self, **kwargs):
        super(DumpCSV, self).initialize(**kwargs)

        self.separator = kwargs.get('separator', ',')

    def write_headers(self):
        content = self.separator.join(list(self.headers))
        self.fout.write(content)
        self.fout.write('\n')

    def patch(self, value):
        value = super(DumpCSV, self).patch(value)
        return str(value)

    def write_obj(self, obj):
        values = [
            self.patch(obj.get(head))
            for head in self.headers
        ]
        content = self.separator.join(values)
        self.fout.write(content)
        self.fout.write('\n')


class DumpXLS(DumpExcel):

    def initialize(self, **kwargs):
        super(DumpCSV, self).initialize(**kwargs)

        self.sheet = kwargs.get('sheet', 'Sheet1')
        self.wb = xlwt.Workbook(encoding='utf-8')
        self.ws = self.wb.add_sheet(self.sheet)
        self.row = 0
        self.cloumn = 0

    def write_headers(self):
        for head in self.headers:
            self.ws.write(self.row, self.cloumn, head)
            self.cloumn += 1
        self.row += 1

    def write_obj(self, obj):
        values = [
            self.patch(obj.get(head))
            for head in self.headers
        ]

        self.cloumn = 0
        for value in values:
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
