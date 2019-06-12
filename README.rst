
jsoncsv : easily convert json to csv or xlsx
==============================================

.. image:: https://img.shields.io/pypi/v/jsoncsv.svg
    :target: https://pypi.python.org/pypi/jsoncsv

.. image:: https://api.travis-ci.org/alingse/jsoncsv.svg?branch=master

.. image:: https://coveralls.io/repos/github/alingse/jsoncsv/badge.svg
    :target: https://coveralls.io/github/alingse/jsoncsv


jsoncsv && mkexcel is a command tool to convert json file to csv/xlsx file.

It's simple, and no need user to specify the keys. :)

Quick Start :
=================

cat the raw.json to csv/xls on command line

.. code-block:: bash

    cat raw.json |jsoncsv |mkexcel > output.csv
    cat raw.json |jsoncsv |mkexcel -t xls > output.xls

or

.. code-block:: bash

    jsoncsv raw.json expand.json
    mkexcel expand.json -t xls output.xls

more options see --help.

.. code-block:: bash

    jsoncsv --help
    mkexcel --help

just expand/restore the json

.. code-block:: bash

    jsoncsv raw.json expand.json
    jsoncsv -r expand.json raw.json
    cat raw.json|jsoncsv |jsoncsv -r > raw2.json

mkexcel the expanded json (one layer)

.. code-block:: bash

    mkexcel expand.json output.csv
    mkexcel -t xls expand.json > output.xls

safe mod

.. code-block:: bash

    cat raw.json|jsoncsv --safe|mkexcel > output.csv


jsoncsv
>>>>>>>>

use jsoncsv to expand json files to 1 layer json

like this：

.. code-block:: bash

    echo '{"s":[1,2,{"w":1}]}'|jsoncsv
    {"s.2.w": 1,"s.0": 1,"s.1": 2}


-e, --expand
-------------

expand json, 展开 json

.. code-block:: bash

    jsoncsv -e raw.json expand.json
    cat raw.json expand.json
    {"s":[1,2,{"w":1}]}
    {"s.2.w": 1,"s.0": 1,"s.1": 2}


{"s":[1,2,{"w":1}]} transformed to {"s.2.w": 1,"s.0": 1,"s.1": 2}

expand.json is only one layer json, it can be easy change to csv or xlsx

-r,--restore
---------------
restore the expanded json 重构被展开的json

.. code-block:: bash

    jsoncsv -r expand.json raw.json
    cat expand.json raw.json
    {"s.2.w": 1,"s.0": 1,"s.1": 2}
    {"s": [1, 2, {"w": 1}]}

{"s.2.w": 1,"s.0": 1,"s.1": 2} change to {"s":[1,2,{"w":1}]}

-s,--separator
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

    mkexcel expand.json -o output.csv
    cat expand.json|mkexcel > output.csv
    cat expand.json|mkexcel -t xls > output.xls


-t,--type
--------------

chose dump type in ['csv', 'xls']

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

wait next version
