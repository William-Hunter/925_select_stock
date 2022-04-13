# -*- coding: UTF-8 -*-
"""
金融界爬虫获取的数据
"""

import requests
import json
import simplejson
import akshare_script
import config
import mail_work
import time
import datetime
import threading


# 时间戳函数
def getTimeStamp():
    millis = int(round(time.time() * 1000))
    # print("时间戳:", millis)
    return millis


# 请求数据的函数
def posts():
    payload = {
        'c': 's,ta,tm,sl,cot,cat,ape',
        'n': 'hqa',
        'o': 'cat,d',  # 排序规则
        'p': '10' + str(config.get()['strategy']['page']),  # 分页
        '_dc': getTimeStamp(),  # 时间戳
    }
    result = requests.get("http://q.jrjimg.cn/?q=cn|s|sa", params=payload)
    if config.get()['DEBUG']:
        print(result.url)
        print(result.status_code)
        print(result.text)

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
    print("流通股本", end=TABFORMAT)
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


def washStock(line, stockList):
    """
    清洗单个股票数据
    :param line:
    :return:
    """
    stock = {}
    gain = line[9]  # 涨幅过滤
    name = line[2]
    code = line[1]
    PER = line[14]
    print("%s 开始洗数据 %s" % (name, datetime.datetime.now()))

    if gain < 0:
        if config.get()['DEBUG']:
            print("涨幅为负过滤：%s %s" % (name, config.get()['strategy']['gain-limit']))
        print("%s 洗数据完毕 %s" % (name, datetime.datetime.now()))
        return None
    elif gain > config.get()['strategy']['gain-limit']:
        if config.get()['DEBUG']:
            print("涨幅过滤：%s %s" % (name, config.get()['strategy']['gain-limit']))
        print("%s 洗数据完毕 %s" % (name, datetime.datetime.now()))
        return None

    x1 = time.time()
    loop = True  # 循环标记
    while loop:
        try:
            stockbase = akshare_script.getLiqudStockBase(code)
        except simplejson.errors.JSONDecodeError:
            print("akshare查询结果有问题")
        else:
            loop = False
            print("akshare查询完成")
    print("跳出循环")
    x2 = time.time()
    print('%s 流通股本过滤运行时间: %s 毫秒' % (name, round((x2 - x1) * 1000, 2)))

    if stockbase > config.get()['strategy']['stockbase-limit']:  # 如果大于一千万，就过滤掉
        if config.get()['DEBUG']:
            print("流通股本过滤：%s %s" % (name, config.get()['strategy']['stockbase-limit']))
        print("%s 洗数据完毕 %s" % (name, datetime.datetime.now()))
        return None

    if PER > config.get()['strategy']['PER-limit']:  # 市盈率大于500
        if config.get()['DEBUG']:
            print("市盈率过滤：%s %s" % (name, config.get()['strategy']['PER-limit']))
        print("%s 洗数据完毕 %s" % (name, datetime.datetime.now()))
        return None

    stock['code'] = code
    stock['name'] = name
    stock['gain'] = gain
    stock['vol'] = line[11]
    stock['stockbase'] = stockbase
    stock['PER'] = PER
    stock['lcode'] = line[0]
    print("%s 洗数据完毕 %s" % (name, datetime.datetime.now()))

    stockList.append(stock)
    # return stock


def threadWashData(jsoon):
    """
    使用多线程方式去执行数据处理任务
    :param jsoon:
    :return:
    """
    processList = list()
    stockList = list()
    for line in jsoon:  # 分发任务
        process = threading.Thread(target=washStock, args=(line, stockList))
        processList.append(process)
        print("分发任务%s" % (line[2]))
    for process in processList:
        process.start()
    print("Start")
    for process in processList:
        process.join()
    print("join")
    return stockList


def htmlFormat(stocklst):
    """
    将数据设置为html格式的String
    :param stocklst:
    :return:
    """
    html = '拉到最下面可以复制股票代码<br/>'
    html = html + '<table border="1">'
    html = html + '<tr><th>#</th><th>短代号</th><th>股票名</th><th>涨跌幅</th><th>量比</th><th>流通股本</th><th>市盈率</th><th>长代号</th></tr>'

    codezone = "<br/>"
    index = 0
    for line in stocklst:
        index = index + 1
        html = html + '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td><td>{6}</td><td>{7}</td></tr>'.format(
            index, line['code'], line['name'], line['gain'], line['vol'], line['stockbase'], line['PER'], line['lcode'])
        codezone = codezone + line['code'] + "<br/>"

    html = html + "</table>"
    html = html + codezone
    print(html)
    return html


def function():
    print("--------------------")
    print("现在的时间是：%s，开始今天的荐股任务了" % (datetime.datetime.now()))
    result = posts()
    data = result.text
    if 'HqData:' in data:
        jsoon = cutIt(result)
        stocklst = threadWashData(jsoon)
        # displayStock(stocklst)
        html = htmlFormat(stocklst)  # 格式化成HTML
        mail_work.sendMail(mail_work.login(), config.get()['email']['receivers'], "每日竞价集合自动荐股", html)  # 发送邮件

    # TODO 按照我的 市盈率市净率条件过滤一遍
    else:
        print("很遗憾，没有获取到数据")
    print("=====END==========")
