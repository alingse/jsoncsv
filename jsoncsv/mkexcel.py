#!/usr/bin/python
#coding=utf-8
#author@shibin
#2015.10.09

import StringIO
import xlwt
import json
import sys


def filter_none(one_list):
    for i in range(len(one_list)):
        if one_list[i] == None:
            one_list[i] = ""
    return one_list


each_encode = lambda x: [i.encode('utf-8') for i in x]


def make_xls_file(header_list, data_list):
    headers = each_encode(filter_none(header_list))
    datas = [each_encode(filter_none(row)) for row in data_list]

    mem_file = StringIO.StringIO()
    wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
    ws = wb.add_sheet('Sheet1')
    r = 0
    c = 0
    for header in headers:
        ws.write(r, c, header)
        c += 1

    for data in datas:
        r += 1
        c = 0
        for datai in data:
            ws.write(r, c, datai)
            c += 1
    wb.save(mem_file)
    mem_file.flush()
    return mem_file


def chg_doc(doc):
    newdoc = {}
    for k in doc:
        newdoc[k] = doc[k]

    for k in newdoc:
        v = newdoc[k]
        if v == None:
            newdoc[k] = ""
        elif type(v) != unicode:
            newdoc[k] = str(v)
    return newdoc


def readfile(fin):
    header_list = []
    data_list = []
    for line in fin:
        doc = json.loads(line)
        doc = chg_doc(doc)
        if header_list == []:
            header_list = doc.keys()
        data = []
        for k in header_list:
            data.append(doc[k])
        data_list.append(data)
    return header_list, data_list


def writefile(mem_file, fout):
    fout.write(mem_file.getvalue())
    fout.close()


def main(fin, fout):
    header_list, data_list = readfile(fin)
    mem_file = make_xls_file(header_list, data_list)
    writefile(mem_file, fout)


if __name__ == '__main__':
    fin = sys.stdin
    fout = sys.stdout
    if len(sys.argv) == 2:
        fin = open(sys.argv[1], 'r')
    if len(sys.argv) == 3:
        fin = open(sys.argv[1], 'r')
        fout = open(sys.argv[2], 'w')
    main(fin, fout)
