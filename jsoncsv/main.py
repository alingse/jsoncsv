# coding=utf-8

from __future__ import print_function

import argparse
import json
import sys

from jsoncsv.jsontool import expand, restore
from jsoncsv.dumptool import dump_csv, dump_xls, dumpfile


def load_jsontool_parse():
    parser = argparse.ArgumentParser()

    def separator_type(string):
        if len(string) > 1:
            msg = 'separator can only be a char'
            raise argparse.ArgumentTypeError(msg)
        if string == '\\':
            msg = 'separator can not be `\\` '
            raise argparse.ArgumentTypeError(msg)
        return string

    parser.add_argument('-s',
                        '--separator',
                        action='store',
                        help='the separator for join keys',
                        type=separator_type,
                        default='.')
    parser.add_argument('--safe',
                        action='store_true',
                        help='use safe mode. key1.key2 --> key1\\.key2')
    parser.add_argument('-e',
                        '--expand',
                        action='store_true',
                        help='choose `expand` a json')
    parser.add_argument('-r',
                        '--restore',
                        action='store_true',
                        help='choose `contract` a ｀expanded` json')
    parser.add_argument('-o',
                        '--output',
                        help='file for output, default is stdout')
    parser.add_argument('input',
                        nargs='?',
                        help='input file, default is stdin')

    return parser


def load_mkexcel_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t',
                        '--type',
                        choices=['csv', 'xls'],
                        default='csv',
                        help='choose dump format')
    parser.add_argument('input',
                        nargs='?',
                        help='input file, default is stdin')
    parser.add_argument('output',
                        nargs='?',
                        help='output file, default is stdout')
    return parser


def jsoncsv():
    parser = load_jsontool_parse()
    args = parser.parse_args()

    if args.expand and args.restore:
        print('can not choose both, default is `-e`', file=sys.stderr)
        exit()
    elif args.expand:
        func = expand
    elif args.restore:
        func = restore
    else:
        func = expand

    fin = sys.stdin
    fout = sys.stdout

    if args.input is not None:
        fin = open(args.input, 'r')
    if args.output is not None:
        fout = open(args.output, 'w')

    safe = args.safe
    separator = args.separator

    for line in fin:
        obj = json.loads(line)
        new = func(obj, separator=separator, safe=safe)
        out = json.dumps(new, ensure_ascii=False).encode('utf-8')
        fout.write(out)
        fout.write('\n')


def mkexcel():
    parser = load_mkexcel_parse()
    args = parser.parse_args()

    dumpf = dump_csv

    if args.type == 'csv':
        dumpf = dump_csv
    if args.type == 'xls':
        dumpf = dump_xls

    fin = sys.stdin
    fout = sys.stdout

    if args.input is not None:
        fin = open(args.input, 'r')

    if args.output is not None:
        fout = open(args.output, 'w')

    dumpfile(fin, fout, dumpf)
