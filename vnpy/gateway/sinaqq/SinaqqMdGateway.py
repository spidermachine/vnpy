# encoding: UTF-8
from vnpy.trader.vtGateway import *
from vnpy.trader.vtFunction import getJsonPath
from vnpy.api.sina.qq import sinaqq
from vnpy.api.sina.stock import sinastock
import json
import datetime
import threading
from .optionData import OptionTick, RiskTick


class SinaqqMdGateway(VtGateway):
    """
    market data
    """
    def __init__(self, eventEngine, gatewayName='Sinaqqmd'):
        """Constructor"""
        super(SinaqqMdGateway, self).__init__(eventEngine, gatewayName)

        self.fileName = self.gatewayName + '_connect.json'
        self.filePath = getJsonPath(self.fileName, __file__)
        self.api = sinaqq
        self.opCodes = list()
        self.isRunning = False
        self.settings = None
        self.routine = None

    def update_tick(self):
        """
        固定时间间隔更新tick
        :return:
        """
        interval = 5
        if 'interval' in self.settings:
            interval = self.settings['interval']
        while self.isRunning:
            cur = datetime.datetime().now()
            if cur.second % interval == 0:
                data = self.get_tick_data()
                for item in data:
                    self.onTick(item)
            time.sleep(1)

    def get_tick_data(self):
        data = sinaqq.get_op_price_batch(self.opCodes)
        vlist = list()
        now = datetime.datetime.now()
        # date_str = now.strftime('%Y%m%d')
        # time_str = now.strftime('%H:%M:%S')
        for item in data:
            tick = OptionTick()
            tick.symbol = item[0]
            tick.gatewayName = self.gatewayName
            tick.exchange = ''
            tick.vtSymbol = tick.exchange + tick.symbol
            tick.date = item[1][32][:10]
            tick.time = item[1][32][11:]
            tick.datetime = now

            tick.buyVolume = item[1][0]
            tick.buyPrice = item[1][1]
            tick.lastPrice = item[1][2]
            tick.sellPrice = item[1][3]
            tick.sellVolume = item[1][4]
            tick.openInterest = item[1][5]
            tick.rise = item[1][6]
            tick.exePrice = item[1][7]

            tick.preClosePrice = item[1][8]
            tick.openPrice = item[1][9]
            tick.lastPrice = item[1][3]

            tick.askPrice5 = item[1][12]
            tick.askVolume5 = item[1][13]
            tick.askPrice4 = item[1][14]
            tick.askVolume4 = item[1][15]
            tick.askPrice3 = item[1][16]
            tick.askVolume3 = item[1][17]
            tick.askPrice2 = item[1][18]
            tick.askVolume2 = item[1][19]
            tick.askPrice1 = item[1][20]
            tick.askVolume1 = item[1][21]

            tick.bidVolume1 = item[1][22]
            tick.bidPrice1 = item[1][23]
            tick.bidVolume2 = item[1][24]
            tick.bidPrice2 = item[1][25]
            tick.bidVolume3 = item[1][26]
            tick.bidPrice3 = item[1][27]
            tick.bidVolume4 = item[1][28]
            tick.bidPrice4 = item[1][29]
            tick.bidVolume5 = item[1][30]
            tick.bidPrice5 = item[1][31]

            tick.under = item[1][36]
            tick.name = item[1][37]
            tick.amp = item[1][38]
            tick.highPrice = item[1][39]
            tick.lowPrice = item[1][40]
            tick.volume = item[1][41]
            vlist.append(tick)
        return vlist

    
    def connect(self):

        try:
            f = open(self.filePath)
        except IOError:
            log = VtLogData()
            log.gatewayName = self.gatewayName
            log.logContent = u'读取连接配置出错，请检查'
            self.onLog(log)
            return

        # 解析json文件
        self.settings = json.load(f)
        f.close()

        if len(self.opCodes) == 0:
            dates = sinaqq.get_op_dates()
            for opt_date in dates:
                up_codes, down_codes = sinaqq.get_op_codes(opt_date)
                self.opCodes += up_codes
                self.opCodes += down_codes
        self.isRunning = True
        self.routine = threading.Thread(target=self.update_tick)
        self.routine.start()

    def close(self):
        self.isRunning = False


class SinaRiskGateway(SinaqqMdGateway):
    """
    risk data
    """
    def __init__(self, eventEngine, gatewayName='Sinaqqmd'):
        """Constructor"""
        super(SinaRiskGateway, self).__init__(eventEngine, gatewayName)

    def get_tick_data(self):
        data = sinaqq.get_op_greek_alphabet_batch(self.opCodes)
        vlist = list()
        for item in data:
            risk = RiskTick()
            risk.name = item[1][0]
            risk.volume = item[1][1]
            risk.delta = item[1][2]
            risk.gamma = item[1][3]
            risk.theta = item[1][4]
            risk.vega = item[1][5]
            risk.hideWave = item[1][6]
            risk.highPrice = item[1][7]
            risk.lowPrice = item[1][8]
            risk.symbol = item[1][9]
            risk.exePrice = item[1][10]
            risk.lastPrice = item[1][11]
            risk.theory = item[1][12]
            vlist.append(risk)
        return vlist


class SinaStockGateway(SinaqqMdGateway):
    """
    股票etf接口
    """
    def __init__(self, eventEngine, gatewayName='Sinaqqmd'):
        """Constructor"""
        super(SinaStockGateway, self).__init__(eventEngine, gatewayName)

    def connect(self):
        pass

    def subscribe(self, subscribeReq):
        self.opCodes.append()

    def get_tick_data(self):
        data = sinastock.get_stock_price(self.opCodes)
        vlist = list()
        for item in data:
            tick = VtTickData()
            tick.symbol = item[0]
            tick.gatewayName = self.gatewayName
            tick.exchange = item[0][:2]
            tick.vtSymbol = tick.exchange + tick.symbol
            tick.date = item[1][30]
            tick.time = item[1][31]
            tick.datetime = datetime.datetime.now()
            tick.openPrice = item[1][1]
            tick.preClosePrice = item[1][2]
            tick.lastPrice = item[1][3]
            tick.highPrice = item[1][4]
            tick.lowPrice = item[1][5]
            tick.volume = item[1][8]

            tick.askVolume1 = item[1][10]
            tick.askPrice1 = item[1][11]
            tick.askVolume2 = item[1][12]
            tick.askPrice2 = item[1][13]
            tick.askVolume3 = item[1][14]
            tick.askPrice3 = item[1][15]
            tick.askVolume4 = item[1][16]
            tick.askPrice4 = item[1][17]
            tick.askVolume5 = item[1][18]
            tick.askPrice5 = item[1][19]

            tick.bidVolume1= item[1][20]
            tick.bidPrice1 = item[1][21]
            tick.bidVolume2 = item[1][22]
            tick.bidPrice2 = item[1][23]
            tick.bidVolume3 = item[1][24]
            tick.bidPrice3 = item[1][25]
            tick.bidVolume4 = item[1][26]
            tick.bidPrice4 = item[1][27]
            tick.bidVolume5 = item[1][28]
            tick.bidPrice5 = item[1][29]
            vlist.append(tick)
        return vlist
