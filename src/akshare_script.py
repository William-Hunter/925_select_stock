#!/usr/bin/python
# -*- coding: UTF-8 -*-

import akshare as ak

def getLiqudStockBase(code):
    info = getStockInfo(code)
    basebase = info.values[7][1]
    # basebase = basebase / 10000
    return basebase


def getStockInfo(code):
    stock_individual_info_em_df = ak.stock_individual_info_em(symbol=code)
    # print(stock_individual_info_em_df)
    return stock_individual_info_em_df
