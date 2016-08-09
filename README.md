# jsoncsv
将多层次的json转为一层次的json，再转成csv或者xlsx

**展开为1层json**

```
echo '{"s":[1,2,{"w":1}]}'|./jsoncsv.py -e |jq -r ''
{
  "s.2.w": 1,
  "s.0": 1,
  "s.1": 2
}
```
**制作xlsx** 

```
cat raw.json|./jsoncsv.py -e |./mkexcel.py > test.csv
cat raw.json|./jsoncsv.py -e |./mkexcel.py -t xls > test.xls
```



## 来源说明
因为做爬虫时，经常数据是json 格式的，而很多**客户需要看excel 的，需要耗费人力去填表格。

这两个文件可以连用，可以从原始json（可以用 `jq` 先做一些处理）到csv/xlsx一步完成。

最后再根据具体含义，更改xlsx文件的标题，使有明确含义

## 功能介绍

jsoncsv.expand 展开 多层json
jsoncsv.restore 重构 单层json

mkexcel 代码暂时还没有分割清楚


### 展开 expand 与 restore 重构
 **jsoncsv.expand** 函数 展开

```
echo '[1,2,3,4]'|./jsoncsv.py -e 
{"1": 2, "0": 1, "3": 4, "2": 3}

echo '"sss"'|./jsoncsv.py -e    
{"": "sss"}

 echo '1'|./jsoncsv.py -e
{"": 1}

echo '{"s":[1,2,{"w":1}]}'|./jsoncsv.py -e
{"s.2.w": 1, "s.0": 1, "s.1": 2}

```  

**jsoncsv.restore** 恢复

每一组第一行是展开，第二行是对展开的结果重构，注意结果对比原始数据

```
echo '[1,2,3,4]'|./jsoncsv.py -e                            
{"1": 2, "0": 1, "3": 4, "2": 3}
echo '[1,2,3,4]'|./jsoncsv.py -e|./jsoncsv.py -r
[1, 2, 3, 4]

echo '1'|./jsoncsv.py -e

{"": 1}
echo '1'|./jsoncsv.py -e|./jsoncsv.py -r
1

echo '"sss"'|./jsoncsv.py -e                        
{"": "sss"}
echo '"sss"'|./jsoncsv.py -e|./jsoncsv.py -r
"sss"

echo '{"s":[1,2,{"w":1}]}'|./jsoncsv.py -e

{"s.2.w": 1, "s.0": 1, "s.1": 2}
echo '{"s":[1,2,{"w":1}]}'|./jsoncsv.py -e|./jsoncsv.py -r
{"s": [1, 2, {"w": 1}]}

```


如上，将各种类型的json数据转化层单层的 
####  此版本要求
1. 原始json 的 各级key不能包含"."，因为`.`是expand后key的连接字符。
2. 字典key中不能混杂数字。如果全部的key都是数字，恢复重构时会被当成list类型。

例如

```
echo '{"0":1,"2":[1,2]}'|./jsoncsv.py -e
{"0": 1, "2.1": 2, "2.0": 1}

echo '{"0":1,"2":[1,2]}'|./jsoncsv.py -e|./jsoncsv.py -r
[1, [1, 2]]
```
其中恢复重构（`-r`参数）时候，将数字的 "0","2",因为是全是数字，被当成list的恢复了(按照 0，2 排序的结果，没有刻意管理索引值)。


## 格式转换
使用 mkexcel.py 文件，接受一个层次的json文件

即可以使用上面`jsoncsv.py`展开的的json，dump为需要的格式（csv/xls）

`cat raw.json|./jsoncsv.py -e |./mkexcel.py -t xls > test.xls`

其中 `./jsoncsv.py -e` 中 `-e`参数就是展开为一层数据，mkexcle 读取数据即可得到指定的格式

### csv
`csv` 是默认格式
```
cat expand.json|./mkexcel.py > test.csv
cat expand.json|./mkexcel.py -t csv > test.csv
./mkexcel.py expand.json text.csv
./mkexcel.py expand.json > text.csv
```
  
### xlsx

使用`-t xls`或`--type xls`，声明dump 为 xls 格式

 ```
cat expand.json|./mkexcel.py -t xls > test.xls
./mkexcel.py -t xls expand.json text.csv
./mkexcel.py -t xls  expand.json > text.csv
 ```


## 实践
 
 具体实践样例参考某次[爬虫外包](https://github.com/alingse/crawler/tree/master/projects/sfda.gov)的数据处理过程
 (**旧版本下的，应该需要相应调整**)
 
## 测试

简单的 unittest
```
python -m unittest test.test
```

## TODO

以下按顺序来做，

1. <s>增加unittest</s> 完成，
2. 更多的出错检查
3. <s>把文件读写从jsoncsv 中分离出来看</s> 暂时没必要
4. <s>mkexcel 重构</s> 完成
5. 构建包
  
