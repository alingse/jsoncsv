import sys

import click

from jsoncsv import dumptool, jsontool
from jsoncsv.dumptool import dump_excel
from jsoncsv.jsontool import convert_json
from jsoncsv.utils import unit_char


def separator_type(sep):
    if len(sep) != 1:
        raise click.BadOptionUsage(option_name='separator',
                                   message='separator can only be a char')
    if sep == unit_char:
        raise click.BadOptionUsage(option_name='separator',
                                   message='separator can not be `\\` ')
    return sep


@click.command()
@click.option('-A',
              '--array',
              'json_array',
              is_flag=True,
              default=False,
              help='read input file as json array')
@click.option('-s',
              '--sep',
              'separator',
              type=separator_type,
              default='.',
              help='separator')
@click.option('--safe', is_flag=True, help='use safe mode')
@click.option('-r',
              '--restore',
              'restore',
              is_flag=True,
              help='restore expanded json')
@click.option('-e',
              '--expand',
              'expand',
              is_flag=True,
              help='expand json (default True)')
@click.argument('input', type=click.File('r', encoding='utf-8'), default='-')
@click.argument('output', type=click.File('w', encoding='utf-8'), default='-')
def jsoncsv(output, input, expand, restore, safe, separator, json_array):
    if expand and restore:
        raise click.UsageError('can not choose both, default is `-e`')

    func = jsontool.expand if not restore else jsontool.restore

    convert_json(input,
                 output,
                 func,
                 separator=separator,
                 safe=safe,
                 json_array=json_array)

    input.close()
    output.close()


@click.command()
@click.option('-t',
              '--type',
              'type_',
              type=click.Choice(['csv', 'xls']),
              default='csv',
              help='choose dump format')
@click.option('-r',
              '--row',
              type=int,
              default=None,
              help='number of pre-read `row` lines to load `headers`')
@click.option('-s',
              '--sort',
              'sort_',
              is_flag=True,
              default=False,
              help='enable sort the headers keys')
@click.argument('input', type=click.File('r', encoding='utf-8'), default='-')
@click.argument('output', type=click.Path(), default='-')
def mkexcel(output, input, sort_, row, type_):
    klass = dumptool.DumpCSV
    if type_ == "xls":
        klass = dumptool.DumpXLS

    # Open file in appropriate mode based on type
    if output == '-':
        fout = sys.stdout.buffer if type_ == 'xls' else sys.stdout
        dump_excel(input, fout, klass, read_row=row, sort_type=sort_)
    else:
        mode = 'wb' if type_ == 'xls' else 'w'
        encoding = None if type_ == 'xls' else 'utf-8'
        newline = '' if type_ == 'csv' else None
        with open(output, mode, encoding=encoding, newline=newline) as fout:
            dump_excel(input, fout, klass, read_row=row, sort_type=sort_)

    input.close()
