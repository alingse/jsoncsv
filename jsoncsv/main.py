# coding=utf-8

from __future__ import print_function

import argparse
import json
import sys

from jsoncsv.jsontool import expand, restore
from jsoncsv.dumptool import dump_csv, dump_xls, dumpfile


def load_jsontool_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s',
                        '--separator',
                        action='store',
                        help='the separator for join keys',
                        default='.')
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
    else:
        func = expand

    if args.input is not None:
        fin = open(args.input, 'r')
    else:
        fin = sys.stdin

    if args.output is not None:
        fout = open(args.output, 'w')
    else:
        fout = sys.stdout

    if args.expand:
        func = expand
    if args.restore:
        func = restore

    separator = args.separator

    for line in fin:
        obj = json.loads(line)
        new = func(obj, separator=separator)
        out = json.dumps(new, ensure_ascii=False).encode('utf-8')
        fout.write(out)
        fout.write('\n')


def mkexcel():
    parser = load_mkexcel_parse()
    args = parser.parse_args()

    if args.type == 'csv':
        dumpf = dump_csv
    elif args.type == 'xls':
        dumpf = dump_xls
    else:
        # can't reach here
        print('can not reach here', file=sys.stderr)
        exit()

    if args.input is not None:
        fin = open(args.input, 'r')
    else:
        fin = sys.stdin

    if args.output is not None:
        fout = open(args.output, 'w')
    else:
        fout = sys.stdout

    dumpfile(fin, fout, dumpf)
