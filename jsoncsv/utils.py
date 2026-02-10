# author@alingse
# 2016.11.20

# Type aliases for JSON data structures
JsonType = dict[str, 'JsonType'] | list['JsonType'] | str | int | float | bool | None
PathType = list[int | str]  # Can contain ints (array indices) or strings (dict keys)
DecodedPathType = list[str]  # Decoded paths from keys are always strings
LeafType = tuple[PathType, JsonType]
# Type for leafs that can contain either PathType (from gen_leaf) or DecodedPathType (from restore)
LeafInputType = LeafType | tuple[DecodedPathType, JsonType]

unit_char = '\\'


def encode_safe_key(path: list[str], separator: str) -> str:
    path = [p.replace(unit_char, unit_char * 2) for p in path]
    separator = unit_char + separator
    return separator.join(path)


def decode_safe_key(key: str, separator: str) -> list[str]:
    path: list[str] = []
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
