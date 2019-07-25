#!/usr/bin/python
#  -*- coding: UTF-8 -*-
from requests import get


def get_stock_price(codes):
    url = "http://hq.sinajs.cn/list={}".format(','.join(codes))
    data = get(url).content.decode('gbk')
    data = data[data.find('"') + 1: data.rfind('"')].split(',')
    # fields = ['股票名字', '今日开盘价', '昨日收盘价',
    # '当前价格', '今日最高价', '今日最低价',
    # '竞买价', '竞卖价', '成交的股票数',
    # '成交金额', '买一量', '买一价',
    # '买二量', '买二价', '买三量',
    # '买三价', '买四量', '买四价',
    #           '买五量', '买五价', '卖一量',
    #           '卖一价', '卖二量', '卖二价',
    #           '卖三量', '卖三价', '卖四量',
    #           '卖四价','卖五量', '卖五价', '日期', '时间']
    return zip(codes, data)
