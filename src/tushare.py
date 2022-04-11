#!/usr/bin/python
# -*- coding: UTF-8 -*-


pro = ts.pro_api('22c86de26f5dd8eab821fde40714b694b0753940024109152c74e854')

print("hello,world\t tushare version is ", ts.__version__)

# print("整个4月的不能交易的日子如下图所示")
# df = pro.trade_cal(exchange='', start_date='20220401', end_date='20220430',
#                    fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
# print(df)

# print("整个4月的能交易的日子如下图所示")
# df = pro.trade_cal(exchange='SSE', is_open='1', start_date='20220401', end_date='20220430', fields='cal_date')
# print(df.head())

# print("通富微电的交易数据")
# data=ts.get_hist_data('002156') #一次性获取全部数据
# print(data)

print("集合竞价")
# df = ts.get_realtime_quotes('002156')
# # df=pro.get_realtime_quotes()
# print(df[['code','name','price','bid','ask','volume','amount','time']])


df = pro.stk_mins(ts_code='',start_time='2022-04-08 09:30:00',end_time='2022-04-08 15:00:00',freq='5min')
print(df)


