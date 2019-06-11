# coding=utf-8

import click
import sys

from jsoncsv.dumptool import dump_excel
from jsoncsv.dumptool import convert_json
from jsoncsv.utils import separator_type


@click.command()
@click.option(
    '-s',
    '--sep',
    'separator',
    type=separator_type,
    default='.',
    help='separator')
@click.option(
    '--safe',
    is_flag=True,
    help='use safe mode')
@click.option(
    '-r',
    '--restore',
    'restore',
    is_flag=True,
    help='restore expanded json')
@click.option(
    '-e',
    '--expand',
    'expand',
    is_flag=True,
    help='expand json')
@click.argument(
    'input',
    type=click.File('r'),
    default=sys.stdin)
@click.argument(
    'output',
    type=click.File('w'),
    default=sys.stdout)
def jsoncsv(output, input, expand, restore, safe, separator):
    if expand and restore:
        raise click.UsageError('can not choose both, default is `-e`')

    type = "expand"  # default
    if restore:
        type = "restore"

    convert_json(input, output, type, separator, safe)

    input.close()
    output.close()


@click.command()
@click.option(
    '-t',
    '--type',
    'type_',
    type=click.Choice(['csv', 'xls']),
    default='csv',
    help='choose dump format')
@click.option(
    '-r',
    '--row',
    type=int,
    default=None,
    help='number of pre-read `row` lines to load `headers`')
@click.option(
    '-s',
    '--sort',
    'sort_',
    is_flag=True,
    default=False,
    help='enable sort the headers keys')
@click.argument(
    'input',
    type=click.File('r'),
    default=sys.stdin)
@click.argument(
    'output',
    type=click.File('wb'),
    default=sys.stdout)
def mkexcel(output, input, sort_, row, type_):
    if output == sys.stdout and type_ == "xls":
        output = click.get_binary_stream('stdout')

    dump_excel(input, output, type_, read_row=row, sort_type=sort_)

    input.close()
    output.close()
