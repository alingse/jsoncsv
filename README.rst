
jsoncsv : convert json to csv or xlsx
=================================================

.. image:: https://img.shields.io/pypi/v/jsoncsv.svg
    :target: https://pypi.python.org/pypi/jsoncsv

jsoncsv is a command tool to convert json file to csv or xlsx file.

It has not ready to be use as a module. :(

command line example :

.. code-block:: bash

    cat raw.json|jsoncsv|mkexcel > output.csv
    cat raw.json|jsoncsv|mkexcel -t xls > output.xls

    jsoncsv raw.json expand.json

    mkexcel expand.json -o output.csv
    mkexcel expand.json -t xls -o output.csv

    cat expand.json|jsoncsv -r > raw.json

    cat raw.json|jsoncsv --safe|mkexcel > output.csv


    jsoncsv --help



jsoncsv
>>>>>>>>

example：

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
restore 重构被展开的json

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

['aa', 'bb', 'www.xxx.com'] --> 'aa\.bb\.www.xxx.com'

restore:

'aa\.bb\.www.xxx.com' --> ['aa', 'bb', 'www.xxx.com']


mkexcel
>>>>>>>>>>>

dump expanded (by **jsoncsv**) json file to `csv` or `xls`

将**jsoncsv** expand 的 json文件转成 csv/xls

.. code-block:: bash

    mkexcel expand.json -o output.csv
    cat expand.json|mkexcel > output.csv
    cat expnad.json|mkexcel -t xls > output.xls


-t,--type
--------------

chose dump type in ['csv', 'xls']

.. code-block:: bash

    cat expand.json|mkexcel -t csv > output.csv
    cat expand.json|mkexcel -t xls > output.xls


NOTE/TODO
>>>>>>>>>

1. key can't be all intenger string
-----------------------------------


example:

.. code-block:: bash

	echo '{"0":1,"1":[1,2]}'|jsoncsv -e| jsoncsv -r
	[1, [1, 2]]


如果要考虑，实现方案会过于复杂，不想考虑在expand的json中添加类型信息


2. write in xlsx is always `str`
----------------------------------

wait next version
