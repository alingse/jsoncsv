#!/usr/bin/python
#coding=utf-8
#author@alingse
#2015.10.09

import argparse
#import xlwt
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


#patch
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


def dump_csv(headers,datas,fout):
    fout.write(','.join(headers))
    fout.write('\n')
    for row in datas:
        fout.write(','.join(row))
        fout.write('\n')
    fout.flush()
    fout.close()


def dump_xls(headers,datas,fout):
    import xlwt
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
    wb.save(fout)
    fout.flush()


def main(fin,fout,dumpf):
    headers,datas = load_files(fin)
    datas = patch_datas(datas)
    dumpf(headers,datas,fout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--type',choices=['csv','xls'],default='csv',help='choose dump format')
    parser.add_argument('input', nargs='?', help='input file, default is stdin')
    parser.add_argument('output', nargs='?', help='output file, default is stdout')
    args = parser.parse_args()

    #default dump
    dumpf = dump_csv
    if args.type == 'xls':
        import xlwt
        dumpf = dump_xls

    #default
    fin = sys.stdin
    fout = sys.stdout
    if args.input != None:
        fin = open(args.input, 'r')
    if args.output != None:
        fout = open(args.output, 'w')

    main(fin,fout,dumpf)
    