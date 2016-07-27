# jsoncsv
将多层次的json转为一层次的json，再转成csv或者xlsx

## 来源说明
因为做爬虫时，经常数据是json 格式的，而很多**客户需要看excel 的，需要耗费人力去填表格。

这两个文件可以连用，可以从原始json（可以用 `jq` 先做一些处理）到xlsx一步完成。

最后再根据具体含义，更改xlsx文件的标题，使有明确含义

# 展开 expand
 jsoncsv / expand 函数

## 给个例子

随手写一个字典里有数组，数组里有数字，字典，数组的
这样一个多层的混杂的json

```
echo '{"s":["t",{"w":[[2,3],{"m":0}]}]}'|jq -r ''
``` 
原始结构如图

```
 {
  "s": [
    "t",
    {
      "w": [
        [
          2,
          3
        ],
        {
          "m": 0
        }
      ]
    }
  ]
}
```

经过 jsoncsv.py 里的expand 函数后

```echo '{"s":["t",{"w":[[2,3],{"m":0}]}]}'|./jsoncsv/jsoncsv.py  -e|jq -r ''```

```
{
  "s.1.w.0.0": 2,
  "s.1.w.0.1": 3,
  "s.1.w.1.m": 0,
  "s.0": "t"
}
```


# csv

  略，以后补充


# xlsx

 mkexcel.py 
 读取只有一个层次的json数据，得到xls文件 
 使用举例
 
 ```cat csv.json |./mkexcel.py > test.xls```
 
 利用 expand 中展开的一层数据，即可得到xls
 
 样例参考某次[爬虫外包](https://github.com/alingse/crawler/tree/master/projects/sfda.gov)的数据处理过程
 
 
 
