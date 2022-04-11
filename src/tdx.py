#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pytdx.hq import TdxHq_API


def work():
    api = TdxHq_API()
    with api.connect('119.147.212.81', 7709):
        # some codes

        print("股票列表")
        data=api.get_security_list(1, 0)
        print(data)

        # print("京东方A的数据")
        # data = api.get_security_bars(9, 0, '000725', 0, 10)  # 返回普通list
        # print(data)

    print("END........")
