# coding=utf-8
# author@alingse
# 2016.11.20


__all__ = []

unit_char = '\\'


def separator_type(sep):
    import click

    if len(sep) > 1:
        raise click.BadOptionUsage('separator can only be a char')
    if sep == unit_char:
        raise click.BadOptionUsage('separator can not be `\\` ')
    return sep


def encode_safe_key(path, separator):
    path = [p.replace(unit_char, unit_char*2) for p in path]
    separator = unit_char + separator
    return separator.join(path)


def decode_safe_key(key, separator):
    path = []
    p = ''
    escape = False

    for char in key:
        if escape and char == separator:
            path.append(p)
            p = ''
            escape = False
        elif escape and char == unit_char:
            p += unit_char
            escape = False
        elif not escape and char == unit_char:
            escape = True
        else:
            p += char

    if p != '':
        path.append(p)
    return path
