#!/usr/bin/python
#coding=utf-8
#author@shibin
#2015.10.09

import xlwt
import json
import sys


def patch_none(row):
    for i in range(len(row)):
        if row[i] == None:
            row[i] = ""
    return row


patch_encode = lambda row: [ele.encode('utf-8') for ele in row]


def patch_str(row):
    for i in range(len(row)):
        if type(row[i]) != unicode:
            row[i] = str(row[i])
    return row


def patch_datas(datas):
    datas = map(patch_none,datas)
    datas = map(patch_str,datas)
    datas = map(patch_encode,datas)

    return datas


def load_files(fin):
    headers = set()
    objs = []
    for line in fin:
        obj = json.loads(line)
        for key in obj:
            headers.add(key)
        objs.append(obj)

    headers = list(headers)
    datas = []
    for obj in objs:
        row = []
        for head in headers:
            row.append(obj.get(head,''))
        datas.append(row)

    return (headers,datas)


def make_xls(headers,datas):
    wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
    ws = wb.add_sheet('Sheet1')

    r = 0
    c = 0
    for head in headers:
        ws.write(r, c, head)
        c += 1

    for row in datas:
        r += 1
        c = 0
        for ele in row:
            ws.write(r, c, ele)
            c += 1

    return wb


def main(fin,fout):
    headers,datas = load_files(fin)
    datas = patch_datas(datas)
    wb = make_xls(headers,datas)

    wb.save(fout)
    fout.flush()



if __name__ == '__main__':
    fin = sys.stdin
    fout = sys.stdout
    if len(sys.argv) == 2:
        fin = open(sys.argv[1], 'r')
    if len(sys.argv) == 3:
        fin = open(sys.argv[1], 'r')
        fout = open(sys.argv[2], 'w')
    main(fin, fout)
