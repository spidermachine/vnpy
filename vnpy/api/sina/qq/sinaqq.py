#!/usr/bin/python
#  -*- coding: UTF-8 -*-
from requests import get


def get_op_dates():
    url = "http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getStockName"
    dates = get(url).json()['result']['data']['contractMonth']
    return [''.join(i.split('-')) for i in dates][1:]


def get_op_expire_day(date):
    url = "http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getRemainderDay?date={date}01"
    data = get(url.format(date=date)).json()['result']['data']
    return data['expireDay'], int(data['remainderDays'])


def get_op_codes(date):
    url_up = "http://hq.sinajs.cn/list=OP_UP_510050" + str(date)[-4:]
    url_down = "http://hq.sinajs.cn/list=OP_DOWN_510050" + str(date)[-4:]
    data_up = str(get(url_up).content).replace('"', ',').split(',')
    codes_up = [i for i in data_up if i.startswith('CON_OP_')]
    data_down = str(get(url_down).content).replace('"', ',').split(',')
    codes_down = [i for i in data_down if i.startswith('CON_OP_')]
    return codes_up, codes_down


def get_op_price(code):
    url = "http://hq.sinajs.cn/list=CON_OP_{code}".format(code=code)
    data = get(url).content.decode('gbk')
    data = data[data.find('"') + 1: data.rfind('"')].split(',')
    # fields = ['买量', '买价', '最新价',
    # '卖价', '卖量', '持仓量',
    # '涨幅', '行权价', '昨收价8',
    # '开盘价9', '涨停价',
    #           '跌停价',
    #           '申卖价五12', '申卖量五', '申卖价四',
    #           '申卖量四', '申卖价三', '申卖量三',
    #           '申卖价二',
    #           '申卖量二', '申卖价一', '申卖量一',
    #           '申买价一', '申买量一 ', '申买价二',
    #           '申买量二', '申买价三',
    #           '申买量三', '申买价四', '申买量四',
    #           '申买价五', '申买量五', '行情时间32',
    #           '主力合约标识', '状态码',
    #           '标的证券类型', '标的股票', '期权合约简称',
    #           '振幅', '最高价', '最低价',
    #           '成交量', '成交额']
    # result = list(zip(fields, data))
    return data


def get_op_greek_alphabet(code):
    url = "http://hq.sinajs.cn/list=CON_SO_{code}".format(code=code)
    data = get(url).content.decode('gbk')
    data = data[data.find('"') + 1: data.rfind('"')].split(',')
    # fields = ['期权合约简称', '成交量', 'Delta', 'Gamma', 'Theta', 'Vega', '隐含波动率', '最高价', '最低价', '交易代码',
    #           '行权价', '最新价', '理论价值']
    return [data[0]] + data[4:]


def get_op_greek_alphabet_batch(codes):
    opt_codes = ["CON_SO_" + code[7:] for code in codes]
    url = "http://hq.sinajs.cn/list={}".format(','.join(opt_codes))
    data = get(url).content.decode('gbk')
    data = data.split('\n')
    vlist = list()
    for item in data:
        if len(item) == 0:
            continue
        ldata = item[item.find('"') + 1: item.rfind('"')].split(',')
        vlist.append([ldata[0]] + ldata[4:])
    return zip(codes, vlist)


def get_op_price_batch(codes):
    opt_codes = ["CON_OP_" + code[7:] for code in codes]
    url = "http://hq.sinajs.cn/list={}".format(",".join(opt_codes))
    data = get(url).content.decode('gbk')
    data = data.split('\n')
    vlist = list()
    for item in data:
        if len(item) == 0:
            continue
        ldata = item[item.find('"') + 1: item.rfind('"')].split(',')
        vlist.append(ldata)
    return zip(codes, vlist)
