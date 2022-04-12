#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import time
import json
import akshare_script

DEBUG = False


# 时间戳函数
def getTimeStamp():
    millis = int(round(time.time() * 1000))
    print("时间戳:", millis)
    return millis


# 请求数据的函数
def posts():
    # c=s,ta,tm,sl,cot,cat,ape&n=hqa&o=cat,d&p=1060&_dc=1649728485102
    payload = {
        'c': 's,ta,tm,sl,cot,cat,ape',
        'n': 'hqa',
        'o': 'cat,d',  # 排序规则
        'p': '1060',  # 分页
        '_dc': getTimeStamp(),  # 时间戳
    }
    result = requests.get("http://q.jrjimg.cn/?q=cn|s|sa", params=payload)
    return result


# 剪切字符串的逻辑
def cutIt(result):
    dataList = result.text.split("HqData:")
    if 1 < len(dataList):
        data = dataList[1]  # 获取后面的字符串
        data = data.strip()[:-2]  # 切掉最后一个字符
        # print("data",data)
        jsoon = json.loads(data)
        # print("jsoon\n", jsoon)
        return jsoon
    else:
        print("数据格式不对")


# 显示股票
def displayStock(stocklst):
    TABFORMAT = ' \t|\t'

    print("#", end=TABFORMAT)
    print("短代号", end=TABFORMAT)
    print("股票名", end=TABFORMAT)
    print("涨跌幅", end=TABFORMAT)
    print("量比", end=TABFORMAT)
    print("流通股本(万)", end=TABFORMAT)
    print("市盈率", end=TABFORMAT)
    print("长代号", end=TABFORMAT)
    print()

    index = 0
    for line in stocklst:
        # 打印数据
        index = index + 1
        print(index, end=TABFORMAT)
        print(line['code'], end=TABFORMAT)
        print(line['name'], end=TABFORMAT)
        print(line['gain'], end=TABFORMAT)
        print(line['vol'], end=TABFORMAT)
        print(line['stockbase'], end=TABFORMAT)
        print(line['PER'], end=TABFORMAT)
        print(line['lcode'], end=TABFORMAT)
        print()


# 友好显示数据的函数
# 0:长代号 1:短代号 2:股票名 3: 4: 5: 6:  9:涨跌幅 11:量比
def washData(jsoon):
    stocklst = []
    for line in jsoon:
        stock = {}
        name = line[2]

        gain = line[9]  # 涨幅过滤
        if gain > 7:
            if DEBUG:
                print("涨幅过滤：", name)
            continue

        code = line[1]
        akshare_script.getStockInfo(code)
        stockbase = akshare_script.getLiqudStockBase(code)
        if stockbase > 10000000:  # 如果大于一千万，就过滤掉
            if DEBUG:
                print("流通股本过滤：", name)
            continue

        PER = line[14]
        if PER > 500:  # 市盈率大于500
            if DEBUG:
                print("市盈率过滤：", name)
            continue

        stock['code'] = code
        stock['name'] = name
        stock['gain'] = gain
        stock['vol'] = line[11]
        stock['stockbase'] = stockbase
        stock['PER'] = PER
        stock['lcode'] = line[0]

        stocklst.append(stock)
    return stocklst


def function():
    result = posts()
    print(result.url)
    print(result.status_code)
    # print(result.text)
    print("--------------------")
    data = result.text
    if 'HqData:' in data:
        jsoon = cutIt(result)
        stocklst = washData(jsoon)
        displayStock(stocklst)
    else:
        print("很遗憾，没有获取到数据")

    print("=====END==========")
