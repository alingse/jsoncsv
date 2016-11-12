# jsoncsv 

将多层次的json转为一层次的json，再转成csv或者xlsx 的工具

```
cat raw.json|jsoncsv|mkexcel > output.csv
cat raw.json|jsoncsv|mkexcel -t xls > output. xls
```


## 1. jsoncsv

```bash
echo '{"s":[1,2,{"w":1}]}'|jsoncsv
{"s.2.w": 1,"s.0": 1,"s.1": 2}
```

### -e -r

`-e`,`--expand` expand 展开 json 数据

```
jsoncsv -e raw.json
{"s":[1,2,{"w":1}]} ----> {"s.2.w": 1,"s.0": 1,"s.1": 2}
```
`-r`,`--restore` restore 重构被展开的json

```
jsoncsv -r expand.json
{"s.2.w": 1,"s.0": 1,"s.1": 2} ----> {"s": [1, 2, {"w": 1}]}
```

### -s

 `-s`,`--separator`  default is `.`

## 2.mkexcel

```
cat expand.json|mkexcel -o output.csv
cat expnad.json|mkexcel -t xls > output.xls
```


### -t -o

`-t`,`--type` dump type `['csv', 'xls']`

```
cat expand.json|mkexcel -t csv > output.csv
cat expand.json|mkexcel -t xls > output.xls
```

`-o`,`--output` 指定输出文件


##  NOTE

1. 原始json 的 各级key不能包含"."，因为`.`是expand后key的连接字符。
  
  key can't contains separator `.` 
  
  下个版本会考虑这个问题
  
2. 字典key中不能混杂数字。如果全部的key都是数字，恢复重构时会被当成list类型。

   example:
   
	```
	echo '{"0":1,"2":[1,2]}'|jsoncsv -e| jsoncsv -r
	[1, [1, 2]]
	```

## TODO

以下按顺序来做，

1. <s>增加unittest</s> 完成，
2. 更多的出错检查
3. <s>把文件读写从jsoncsv 中分离出来看</s>
4. <s>mkexcel 重构</s> 完成
5. <s>构建包</s> 完成
6. 支持 separator 的转义
7. mkexcel 的效率
8. mkexcel csv xls dump 的 重构
9. dumptool.dump_xls 对 int 日期等支持
  
