# -*- coding: UTF-8 -*-
"""
金融界爬虫获取的数据
"""

import requests
import time
import json
import akshare_script
import config
import mail_work


# 时间戳函数
def getTimeStamp():
    millis = int(round(time.time() * 1000))
    # print("时间戳:", millis)
    return millis


# 请求数据的函数
def posts():
    # c=s,ta,tm,sl,cot,cat,ape&n=hqa&o=cat,d&p=1060&_dc=1649728485102
    payload = {
        'c': 's,ta,tm,sl,cot,cat,ape',
        'n': 'hqa',
        'o': 'cat,d',  # 排序规则
        'p': '10' + str(config.get()['strategy']['page']),  # 分页
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


# 友好显示数据的函数
# 0:长代号 1:短代号 2:股票名 3: 4: 5: 6:  9:涨跌幅 11:量比
def washData(jsoon):
    stocklst = []
    # TODO 计算耗时代码段
    for line in jsoon:      # TODO 异步执行，并发的
        stock = {}
        name = line[2]

        gain = line[9]  # 涨幅过滤
        if gain > config.get()['strategy']['gain-limit']:
            if config.get()['DEBUG']:
                print("涨幅过滤：%s %s" % (name, config.get()['strategy']['gain-limit']))
            continue

        code = line[1]
        akshare_script.getStockInfo(code)
        stockbase = akshare_script.getLiqudStockBase(code)
        if stockbase > config.get()['strategy']['stockbase-limit']:  # 如果大于一千万，就过滤掉
            if config.get()['DEBUG']:
                print("流通股本过滤：%s %s" % (name, config.get()['strategy']['stockbase-limit']))
            continue

        PER = line[14]
        if PER > config.get()['strategy']['PER-limit']:  # 市盈率大于500
            if config.get()['DEBUG']:
                print("市盈率过滤：%s %s" % (name, config.get()['strategy']['PER-limit']))
            continue

        stock['code'] = code
        stock['name'] = name
        stock['gain'] = gain
        stock['vol'] = line[11]
        stock['stockbase'] = stockbase
        stock['PER'] = PER
        stock['lcode'] = line[0]
        stocklst.append(stock)

        call_sleep = config.get()['strategy']['call_sleep']
        if 0 < call_sleep:              # 睡眠时间
            call_sleep=call_sleep / 1000
            time.sleep(call_sleep)
            print("sleep\t",call_sleep)

    return stocklst


def htmlFormat(stocklst):
    codes=[]
    html = '拉到最下面可以复制股票代码<br/>'
    html=html+'<table border="1">'
    html = html + '<tr><th>#</th><th>短代号</th><th>股票名</th><th>涨跌幅</th><th>量比</th><th>流通股本</th><th>市盈率</th><th>长代号</th></tr>'

    codezone="<br/>"
    index = 0
    for line in stocklst:
        index = index + 1
        html = html + '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td><td>{6}</td><td>{7}</td></tr>'.format(
            index, line['code'], line['name'], line['gain'], line['vol'], line['stockbase'], line['PER'], line['lcode'])
        codezone=codezone+line['code']+"<br/>"

    html = html + "</table>"
    html=html+codezone
    print(html)
    return html


def function():
    print("--------------------")
    print("现在的时间是：%s，开始今天的荐股任务了" % (time.strftime('%Y/%m/%d %H:%M:%S')))
    result = posts()
    print(result.url)
    print(result.status_code)
    # print(result.text)
    data = result.text
    if 'HqData:' in data:
        jsoon = cutIt(result)
        stocklst = washData(jsoon)
        # displayStock(stocklst)
        html = htmlFormat(stocklst)  # 格式化成HTML
        mail_work.sendMail(mail_work.login(), config.get()['email']['receivers'], "每日竞价集合自动荐股", html)  # 发送邮件

    # TODO 按照我的 市盈率市净率条件过滤一遍
    else:
        print("很遗憾，没有获取到数据")
    print("=====END==========")
