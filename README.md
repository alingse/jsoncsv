# jsoncsv : easily convert json to csv or xls[x]

[![PyPI](https://img.shields.io/pypi/v/jsoncsv.svg)](https://pypi.python.org/pypi/jsoncsv)
[![CI](https://github.com/alingse/jsoncsv/actions/workflows/ci.yml/badge.svg)](https://github.com/alingse/jsoncsv/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/alingse/jsoncsv/badge.svg)](https://codecov.io/gh/alingse/jsoncsv)
[![Ruff](https://img.shields.io/endpoint?url=https://ruff.ai/api/badge)](https://github.com/astral-sh/ruff)

jsoncsv (with `mkexcel`) is a command tool to convert json file to csv/xlsx file.

It's simple, and no need user to specify the keys.

Just use them.

## Requirements

- Python 3.11 or higher

## Quick Start

Cat the raw.json to csv/xls use command line tool

```bash
cat raw.json | jsoncsv | mkexcel > output.csv
cat raw.json | jsoncsv | mkexcel -t xls > output.xls
```

Each line of raw json text file is a json object

```json
{"id":1, "name":"A", "year": 2015}
{"id":2, "name":"S", "zone": "china"}
```

Jsoncsv will output a csv file

```
id,name,year,zone
1,A,2015,
2,S,,china
```

This is easily and needn't care the different keys from any two object.

### For Json Array

If input file is an json_array, use `-A/--array` to decode it

```bash
cat raw.json | jsoncsv -A | mkexcel > output.csv
```

**Input File**

```json
[
    {"id":1, "name":"A", "year": 2015},
    {"id":2, "name":"S", "zone": "china"}
]
```

**Output File**

```
id,name,year,zone
1,A,2015,
2,S,,china
```

### Step by Step

```bash
jsoncsv raw.json expand.json
mkexcel expand.json -t xls output.xls
```

get more options with `--help`.

```bash
jsoncsv --help
mkexcel --help
```

## Install

Using pip (recommended):

```bash
pip install jsoncsv
```

Using uv (faster):

```bash
uv pip install jsoncsv
```

For development:

```bash
git clone https://github.com/alingse/jsoncsv
cd jsoncsv
uv pip install -e ".[dev]"
```

## Usage

### Expand/Restore JSON

Just expand/restore the json, the expand json is one layer json.

```bash
jsoncsv raw.json expand.json
jsoncsv -r expand.json raw.json
cat raw.json | jsoncsv | jsoncsv -r > raw2.json
```

### Export to Excel/CSV

mkexcel the expanded json (one layer)

```bash
mkexcel expand.json output.csv
mkexcel -t xls expand.json > output.xls
mkexcel -t csv expand.json > output.csv
```

## Options

### -e, --expand

expand json, 展开 json

```bash
jsoncsv -e raw.json expand.json
cat raw.json expand.json
{"s":[1,2,{"w":1}]}
{"s.2.w": 1,"s.0": 1,"s.1": 2}
```

`{"s":[1,2,{"w":1}]}` will transformed to `{"s.2.w": 1,"s.0": 1,"s.1": 2}`

the output "expand.json" is only one layer json, it can be easy change to csv or xlsx (with `mkexcel`)

### -r, --restore

restore the expanded json 重构被展开的json

```bash
jsoncsv -r expand.json raw.json
cat expand.json raw.json
{"s.2.w": 1,"s.0": 1,"s.1": 2}
{"s": [1, 2, {"w": 1}]}
```

`{"s.2.w": 1,"s.0": 1,"s.1": 2}` change to `{"s":[1,2,{"w":1}]}`

### -s, --separator

separator used to combine the keys in the tree

default separator is **.**

### --safe

on safe mode, use escape separator to avoid confilct

expand:

`['aa', 'bb', 'www.xxx.com']` --> `'aa\\.bb\\.www.xxx.com'`

restore:

`'aa\\.bb\\.www.xxx.com'` --> `['aa', 'bb', 'www.xxx.com']`

## Development

Lint and format:

```bash
ruff check .
ruff format .
```

Run tests:

```bash
pytest
```

Type checking:

```bash
mypy jsoncsv
```

Build package:

```bash
python -m build
```

## License

Apache License 2.0
