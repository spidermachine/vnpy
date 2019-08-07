
from vnpy.event import Event, EventEngine
from vnpy.trader.engine import MainEngine
import requests
import datetime
from vnpy.trader.event import (
    EVENT_TICK,
    # EVENT_TRADE,
    # EVENT_RISK
    # EVENT_ORDER,
    # EVENT_POSITION,
    # EVENT_ACCOUNT,
    # EVENT_LOG
)
from vnpy.trader.setting import SETTING_FILENAME, SETTINGS, get_settings


class hudge:

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        """"""
        super(hudge, self).__init__()

        self.main_engine = main_engine
        self.event_engine = event_engine
        self.server_url_zkp = "https://sc.ftqq.com/SCU7001T3bf48226e1ddbee01c5bd08bbc62096b58d65cc0cecff.send?text={0}&desp={1}"
        # self.server_url_lxf = "https://sc.ftqq.com/SCU10023T7ea46bcfc4cded98590b4e0590397e3859645740a2616.send?text={0}&desp=".format(title)
        self.etf = None
        self.qq = None
        self.start_hudge = None
        self.in_hedge = False
        self.over = False
        self.register_event()

    def register_event(self):
        """"""
        self.event_engine.register(EVENT_TICK, self.process_tick_date)

    def process_tick_date(self, event):

        ldata = event.data
        hedge = get_settings("hedge")
        etf = hedge.get(".etf")
        etfsize = hedge.get(".etfsize")
        qqcode = hedge.get(".qqcode")
        qqcodesize = hedge.get(".qqcodesize")
        stop_hudge = hedge.get(".stop")
        start_hudge = hedge.get(".start")
        if ldata.symbol == etf:
            self.etf = ldata
        elif ldata.symbol.endswith(qqcode):
            self.qq = ldata

        if self.etf and self.qq:
            if self.process_now(self.etf.datetime) == self.process_now(self.qq.datetime):
                money = etfsize * (self.etf.last_price - self.etf.pre_close) - qqcodesize * (self.qq.last_price - self.qq.pre_close) * 10000
                if self.start_hudge is None:
                    self.start_hudge = money

                self.main_engine.write_log(money - self.start_hudge)
                print(money-self.start_hudge)
                if money - self.start_hudge > stop_hudge and not self.over:
                    msg = self.server_url_zkp.format("对冲stop", money - self.start_hudge)
                    self.main_engine.write_log("send to zkp stop hudge")
                    self.over = True
                    try:
                        requests.get(msg)
                    except:
                        pass

                if money - self.start_hudge < start_hudge and not self.in_hedge:
                    msg = self.server_url_zkp.format("对冲start", money - self.start_hudge)
                    self.main_engine.write_log("send to zkp start hudge")
                    self.in_hedge = True
                    try:
                        requests.get(msg)
                    except:
                        pass

                self.etf = None
                self.qq = None

    def process_now(self, now):
        if str(now.second).endswith("1"):
            return now - datetime.timedelta(seconds=1)
        return now.replace(microsecond=0)
