#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tdx
import akshare_script
import jinrongjie
import time

T1 = time.time()

jinrongjie.function()

# akshare_script.getLiqudStockBase('000927')
# tdx.work()


T2 = time.time()
print('程序运行时间:%s秒' % (round(T2 - T1, 2)))
