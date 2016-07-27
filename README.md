# jsoncsv
将多层次的json转为一层次的json，再转成csv或者xlsx


## 来源说明
因为做爬虫时，经常数据是json 格式的，而很多**客户需要看excel 的，需要耗费人力去填表格。

这两个文件可以连用，可以从原始json（可以用 `jq` 先做一些处理）到xlsx一步完成。

最后再根据具体含义，更改xlsx文件的标题，使有明确含义

## 功能介绍

jsoncsv.expand 展开 多层json
jsoncsv.restore 重构 单层json

mkexcel 代码暂时还没有分割清楚


### 展开 expand 与 restore 重构
 **jsoncsv.expand** 函数 展开

```
echo '[1,2,3,4]'|./jsoncsv/jsoncsv.py -e 
{"1": 2, "0": 1, "3": 4, "2": 3}

echo '"sss"'|./jsoncsv/jsoncsv.py -e    
{"": "sss"}

 echo '1'|./jsoncsv/jsoncsv.py -e
{"": 1}

echo '{"s":[1,2,{"w":1}]}'|./jsoncsv/jsoncsv.py -e
{"s.2.w": 1, "s.0": 1, "s.1": 2}

```  

**jsoncsv.restore** 恢复

每一组第一行是展开，第二行是对展开的结果重构，注意结果对比原始数据

```
echo '[1,2,3,4]'|./jsoncsv/jsoncsv.py -e                            
{"1": 2, "0": 1, "3": 4, "2": 3}
echo '[1,2,3,4]'|./jsoncsv/jsoncsv.py -e|./jsoncsv/jsoncsv.py -r
[1, 2, 3, 4]

echo '1'|./jsoncsv/jsoncsv.py -e                                    
{"": 1}
echo '1'|./jsoncsv/jsoncsv.py -e|./jsoncsv/jsoncsv.py -r
1

echo '"sss"'|./jsoncsv/jsoncsv.py -e                        
{"": "sss"}
echo '"sss"'|./jsoncsv/jsoncsv.py -e|./jsoncsv/jsoncsv.py -r
"sss"

echo '{"s":[1,2,{"w":1}]}'|./jsoncsv/jsoncsv.py -e                      
{"s.2.w": 1, "s.0": 1, "s.1": 2}
echo '{"s":[1,2,{"w":1}]}'|./jsoncsv/jsoncsv.py -e|./jsoncsv/jsoncsv.py -r
{"s": [1, 2, {"w": 1}]}

```


如上，将各种类型的json数据转化层单层的 
####  一点要求
1. 原始json 的 各级key不能包含"."
2. 不能混杂数字。如果全部的key都是数字，恢复重构时会被当成list类型。

例如

```
echo '{"0":1,"2":[1,2]}'|./jsoncsv/jsoncsv.py -e
{"0": 1, "2.1": 2, "2.0": 1}

echo '{"0":1,"2":[1,2]}'|./jsoncsv/jsoncsv.py -e|./jsoncsv/jsoncsv.py -r
[1, [1, 2]]
```
其中恢复重构（`-r`参数）时候，将数字的 "0","2",因为是全是数字，被当成list的恢复了(按照 0，2 排序的结果，没有刻意管理索引值)。


## 格式转换

### csv

  略，以后补充

### xlsx

 mkexcel.py 
 
 读取只有一个层次的json数据，得到xls文件，使用举例
 
 ```
 cat raw.json|./jsoncsv.py -e |./mkexcel.py > test.xls
 ```
 
 其中 `./jsoncsv.py -e` 中 `-e`参数就是展开为一层数据，mkexcle 读取数据即可得到xls
 
 具体数据样例参考某次[爬虫外包](https://github.com/alingse/crawler/tree/master/projects/sfda.gov)的数据处理过程
 
 
 
