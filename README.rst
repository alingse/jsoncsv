
jsoncsv : easily convert json to csv or xls[x]
==============================================

.. image:: https://img.shields.io/pypi/v/jsoncsv.svg
    :target: https://pypi.python.org/pypi/jsoncsv

.. image:: https://api.travis-ci.org/alingse/jsoncsv.svg?branch=master

.. image:: https://coveralls.io/repos/github/alingse/jsoncsv/badge.svg
    :target: https://coveralls.io/github/alingse/jsoncsv


jsoncsv (with `mkexcel`) is a command tool to convert json file to csv/xlsx file.

It's simple, and no need user to specify the keys.

Just use them.

Quick Start :
=================

cat the raw.json to csv/xls use command line tool

.. code-block:: bash

    cat raw.json | jsoncsv | mkexcel > output.csv
    cat raw.json | jsoncsv | mkexcel -t xls > output.xls

make sure each line of raw json text file is a json object

.. code-block:: bash

    $cat raw.json
    {"id":1, "name":"A", "year": 2015}
    {"id":2, "name":"S", "zone": "china"}
    $cat raw.json | jsoncsv | mkexcel > output.csv
    $cat output.csv
    id,name,year,zone
    1,A,2015,
    2,S,,china

This is easily and needn't care the different keys from any two object.

if input file is an json_array, use `-A/--array` to decode it

.. code-block:: bash

    $cat raw.json
    [{"id":1, "name":"A", "year": 2015}, {"id":2, "name":"S", "zone": "china"}]
    $cat raw.json | jsoncsv -A | mkexcel > output.csv
    $cat output.csv
    id,name,year,zone
    1,A,2015,
    2,S,,china

another way to convert file step by step

.. code-block:: bash

    $jsoncsv raw.json expand.json
    $mkexcel expand.json -t xls output.xls

get more options with `--help`.

.. code-block:: bash

    jsoncsv --help
    mkexcel --help

Install
================

.. code-block:: bash

    pip install jsoncsv


Usage
=================

see #QuickStart and get more options with `--help`.

just expand/restore the json, the expand json is one layer json.

.. code-block:: bash

    jsoncsv raw.json expand.json
    jsoncsv -r expand.json raw.json
    cat raw.json | jsoncsv | jsoncsv -r > raw2.json

mkexcel the expanded json (one layer)

.. code-block:: bash

    mkexcel expand.json output.csv
    mkexcel -t xls expand.json > output.xls
    mkexcel -t csv expand.json > output.csv

-e, --expand
-------------

expand json, 展开 json

.. code-block:: bash

    $jsoncsv -e raw.json expand.json
    $cat raw.json expand.json
    {"s":[1,2,{"w":1}]}
    {"s.2.w": 1,"s.0": 1,"s.1": 2}


{"s":[1,2,{"w":1}]} will transformed to {"s.2.w": 1,"s.0": 1,"s.1": 2}

the output "expand.json" is only one layer json, it can be easy change to csv or xlsx (with `mkexcel`)

-r, --restore
---------------
restore the expanded json 重构被展开的json

.. code-block:: bash

    jsoncsv -r expand.json raw.json
    cat expand.json raw.json
    {"s.2.w": 1,"s.0": 1,"s.1": 2}
    {"s": [1, 2, {"w": 1}]}

{"s.2.w": 1,"s.0": 1,"s.1": 2} change to {"s":[1,2,{"w":1}]}

-s, --separator
---------------

separator used for combine the keys in the tree

default separator is **.**

--safe
---------
on safe mode, use escape separator to avoid confilct

expand:

['aa', 'bb', 'www.xxx.com'] --> 'aa\\.bb\\.www.xxx.com'

restore:

'aa\\.bb\\.www.xxx.com' --> ['aa', 'bb', 'www.xxx.com']


mkexcel
>>>>>>>>>>>

dump expanded (by **jsoncsv**) json file to csv or xls file

.. code-block:: bash

    mkexcel expand.json output.csv

-t, --type
--------------

chose dump type in ['csv', 'xls'] default is 'csv'

.. code-block:: bash

    cat expand.json|mkexcel -t csv > output.csv
    cat expand.json|mkexcel -t xls > output.xls


NOTE/TODO
>>>>>>>>>

1. dict keys can't be  just array indexes
--------------------------------------------

example:

.. code-block:: bash

	echo '{"0":1,"1":[1,2]}'|jsoncsv -e| jsoncsv -r
	[1, [1, 2]]


2. mkexcel enable hooks
-----------------------------------------

wait next next version


3. unicodecsv is not good enough
-----------------------------------------

but better than python strand library csv.

4. Windows is poor support
-----------------------------------------
see https://github.com/alingse/jsoncsv/issues/37

try use https://jsoncsv.jsonutil.online/ instead
