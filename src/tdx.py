#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pytdx.hq import TdxHq_API
from pytdx.hq import TDXParams

def work():
    api = TdxHq_API()
    with api.connect('119.147.212.81', 7709):
        print("股票详情")
        data=api.get_security_quotes([(0, '300013'), (1, '300013')])
        print(data)

        # print("股票详情")
        # data=api.get_company_info_category(TDXParams.MARKET_SZ, '603117')
        # print(data)

        # print("股票列表")
        # data=api.get_security_list(1, 0)
        # print(data)

        # print("京东方A的数据")
        # data = api.get_security_bars(9, 0, '000725', 0, 10)  # 返回普通list
        # print(data)

    print("END........")
