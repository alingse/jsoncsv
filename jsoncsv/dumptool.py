# coding=utf-8
# author@alingse
# 2015.10.09

import json
import xlwt


def patch(value):
    if value is None:
        return ''
    if isinstance(value, basestring):
        return value.encode('utf-8')
    if value == {} or value == []:
        return ''
    return value


def dump_csv(fin, headers, fout, datas=None):
    headers = list(headers)
 
    fout.write(','.join(headers))
    fout.write('\n')

    def write_obj(obj):
        values = [obj.get(head) for head in headers]
        values = map(patch, values)
        values = map(str, values)


        fout.write(','.join(values))
        fout.write('\n')

    if datas:
        map(write_obj, datas)

    for line in fin:
        obj = json.loads(line)
        write_obj(obj)


def dump_xls(fin, headers, fout, datas=None):
    headers = list(headers)

    wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
    ws = wb.add_sheet('Sheet1')

    self = {}
    self['row'] = 0
    self['cloumn'] = 0
    row = 0
    cloumn = 0

    for head in headers:
        ws.write(self['row'], self['cloumn'], head)
        self['cloumn'] += 1

    def write_obj(obj):

        values = [obj.get(head) for head in headers]
        values = map(patch, values)

        self['row'] += 1
        self['cloumn'] = 0
        for value in values:
            ws.write(self['row'], self['cloumn'], value)
            self['cloumn'] += 1

    if datas:
        map(write_obj, datas)

    for line in fin:
        obj = json.loads(line)
        write_obj(obj)

    wb.save(fout)


def load_headers(fin, read_row=None):
    headers = set()
    datas = []
    i = 0
    for line in fin:
        obj = json.loads(line)
        map(headers.add, obj.iterkeys())
        datas.append(obj)
        if read_row is not None and i >= read_row:
            break

    return headers, datas


def dumpfile(fin, type_, fout, read_row=None):
    headers, datas = load_headers(fin, read_row)
    if type_ == 'csv':
        func = dump_csv
    elif type_ == 'xls':
        func = dump_xls

    func(fin, headers, fout, datas=datas)
