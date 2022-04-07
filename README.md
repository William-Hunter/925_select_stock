# 925_select_stock 选股神器

## 规则

1. 9:25集合竞价，按量比排名，将第一屏的股票保存在新建《925》板块中
2. 《925》板块中，删除市盈率大于500的股票
3. 《925》板块中，删除流通股本大于7位数(1M以上)的股票
4. 《925》板块中，删除涨幅大于7%的股票
5. 在剩余的股票中，观察跳空类型的股票，研判

## 思路

其本质就是在集合竞价的基础上，首先找出那些有竞争力的股票，   
其次删除过于泡沫的股票（要是有做空就好了），    
再次删除盘子太大的股票（池子太大，流资难以改变价位）   
然后删除涨幅过高的股票（前期增长过多，后期增长乏力），    
最后再从其中找到跳空的股票，作为投资对象


个人认为，可以再加一个维度，就是有盈利、财报好看的股票

## 我需要什么数据？
有接口能够拉取实时集合竞价的数据，
然后有接口能够获取一只股票的市盈率、流通股本、涨幅、跳空等数据


