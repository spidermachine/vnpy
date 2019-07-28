# encoding: UTF-8
from vnpy.trader.gateway import *
from vnpy.trader.object import TickData, OptionTick, RiskTick
from vnpy.trader.constant import Exchange
from vnpy.api.sina.qq import sinaqq
from vnpy.api.sina.stock import sinastock
import datetime
import threading
import time
from vnpy.trader.setting import SETTINGS

class SinaqqMdGateway(BaseGateway):
    """
    market data
    """
    def __init__(self, event_engine, gateway_name='sinaqq'):
        """Constructor"""
        super(SinaqqMdGateway, self).__init__(event_engine, gateway_name)

        self.api = sinaqq
        self.opCodes = list()
        self.isRunning = False
        self.settings = SETTINGS
        self.routine = None

    def update_tick(self):
        """
        固定时间间隔更新tick
        :return:
        """
        interval = 5
        if 'sinaqq.interval' in self.settings:
            interval = self.settings['sinaqq.interval']
        while self.isRunning:
            cur = datetime.datetime.now()
            if cur.second % interval == 0:
                data = self.get_tick_data()
                for item in data:
                    self.on_tick(item)
            time.sleep(1)

    def get_tick_data(self):
        data = sinaqq.get_op_price_batch(self.opCodes)
        vlist = list()
        now = datetime.datetime.now()
        for item in data:
            tick = OptionTick()
            tick.symbol = item[0]
            tick.gateway_name = self.gateway_name
            tick.exchange = Exchange.SHFE
            tick.vt_symbol = tick.symbol + "." + tick.exchange.value
            tick.date = item[1][32][:10]
            tick.time = item[1][32][11:]
            tick.datetime = now

            tick.buy_volume = int(item[1][0])
            tick.buy_price = float(item[1][1])
            tick.last_price = float(item[1][2])
            tick.sell_price = float(item[1][3])
            tick.sell_volume = int(item[1][4])
            tick.open_interest = int(item[1][5])
            tick.rise = float(item[1][6])
            tick.exe_price = float(item[1][7])

            tick.pre_close = float(item[1][8])
            tick.open_price = float(item[1][9])
            tick.last_price = float(item[1][3])

            tick.ask_price_5 = float(item[1][12])
            tick.ask_volume_5 = int(item[1][13])
            tick.ask_price_4 = float(item[1][14])
            tick.ask_volume_4 = int(item[1][15])
            tick.ask_price_3 = float(item[1][16])
            tick.ask_volume_3 = int(item[1][17])
            tick.ask_price_2 = float(item[1][18])
            tick.ask_volume_2 = int(item[1][19])
            tick.ask_price_1 = float(item[1][20])
            tick.ask_volume_1 = int(item[1][21])

            tick.bid_price_1 = float(item[1][22])
            tick.bid_volume_1 = int(item[1][23])
            tick.bid_price_2 = float(item[1][24])
            tick.bid_volume_2 = int(item[1][25])
            tick.bid_price_3 = float(item[1][26])
            tick.bid_volume_3 = int(item[1][27])
            tick.bid_price_4 = float(item[1][28])
            tick.bid_volume_4 = int(item[1][29])
            tick.bid_price_5 = float(item[1][30])
            tick.bid_volume_5 = int(item[1][31])

            tick.under = item[1][36]
            tick.name = item[1][37]
            tick.amp = item[1][38]
            tick.high_price = float(item[1][39])
            tick.low_price = float(item[1][40])
            tick.volume = int(item[1][41])
            vlist.append(tick)
        return vlist

    def connect(self, settings):

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

    def cancel_order(self, req: CancelRequest):
        pass

    def query_account(self):
        pass

    def query_position(self):
        pass

    def send_order(self, req: OrderRequest):
        pass

    def subscribe(self, req: SubscribeRequest):
        pass


class SinaRiskGateway(SinaqqMdGateway):
    """
    risk data
    """
    def __init__(self, event_engine):
        """Constructor"""
        super(SinaRiskGateway, self).__init__(event_engine, 'risk')

    def get_tick_data(self):
        data = sinaqq.get_op_greek_alphabet_batch(self.opCodes)
        vlist = list()
        now = datetime.datetime.now()
        for item in data:
            risk = RiskTick(self.gateway_name, item[0], Exchange.SHFE, now)
            risk.gateway_name = self.gateway_name
            risk.exchange = Exchange.SHFE
            risk.symbol = item[0]
            risk.datetime = now
            risk.vt_symbol = risk.symbol + "." + Exchange.SHFE.value
            risk.name = item[1][0]
            risk.volume = int(item[1][1])
            risk.delta = float(item[1][2])
            risk.gamma = float(item[1][3])
            risk.theta = float(item[1][4])
            risk.vega = float(item[1][5])
            risk.hide_wave = float(item[1][6])
            risk.high_price = float(item[1][7])
            risk.low_price = float(item[1][8])
            risk.symbol = item[1][9]
            risk.exe_price = float(item[1][10])
            risk.last_price = float(item[1][11])
            risk.theory = float(item[1][12])
            vlist.append(risk)
        return vlist


class SinaStockGateway(SinaqqMdGateway):
    """
    股票etf接口
    """
    def __init__(self, event_engine):
        """Constructor"""
        super(SinaStockGateway, self).__init__(event_engine, 'sinastock')

    def connect(self, settings):
        self.opCodes.append("sh510050")
        self.isRunning = True
        self.routine = threading.Thread(target=self.update_tick)
        self.routine.start()

    def subscribe(self, req: SubscribeRequest):
        self.opCodes.append(req.symbol)

    def get_tick_data(self):
        data = sinastock.get_stock_price(self.opCodes)
        vlist = list()
        now = datetime.datetime.now()
        for item in data:
            tick = TickData(self.gateway_name, item[0], Exchange.SSE, now)
            tick.vt_symbol = tick.symbol + "." + tick.exchange.value
            tick.date = item[1][30]
            tick.time = item[1][31]
            tick.open_price = float(item[1][1])
            tick.pre_close = float(item[1][2])
            tick.last_price = float(item[1][3])
            tick.high_price = float(item[1][4])
            tick.low_price = float(item[1][5])
            tick.volume = int(item[1][8])

            tick.ask_volume_1 = int(item[1][10])
            tick.ask_price_1 = float(item[1][11])
            tick.ask_volume_2 = int(item[1][12])
            tick.ask_price_2 = float(item[1][13])
            tick.ask_volume_3 = int(item[1][14])
            tick.ask_price_3 = float(item[1][15])
            tick.ask_volume_4 = int(item[1][16])
            tick.ask_price_4 = float(item[1][17])
            tick.ask_volume_5 = int(item[1][18])
            tick.ask_price_5 = float(item[1][19])

            tick.bid_volume_1 = int(item[1][20])
            tick.bid_price_1 = float(item[1][21])
            tick.bid_volume_2 = int(item[1][22])
            tick.bid_price_2 = float(item[1][23])
            tick.bid_volume_3 = int(item[1][24])
            tick.bid_price_3 = float(item[1][25])
            tick.bid_volume_4 = int(item[1][26])
            tick.bid_price_4 = float(item[1][27])
            tick.bid_volume_5 = int(item[1][28])
            tick.bid_price_5 = float(item[1][29])
            vlist.append(tick)
        return vlist
