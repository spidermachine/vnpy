
from vnpy.trader.vtGateway import *


class OptionTick(VtTickData):

    def __init__(self):
        super(OptionTick, self).__init__()

        self.buyPrice = EMPTY_FLOAT
        self.buyVolume = EMPTY_INT
        self.sellPrice = EMPTY_FLOAT
        self.sellVolume = EMPTY_INT
        self.amp = EMPTY_FLOAT
        self.exePrice = EMPTY_FLOAT
        self.under = EMPTY_STRING
        self.name = EMPTY_STRING
        self.rise = EMPTY_FLOAT


class RiskTick(VtBaseData):

    def __int__(self):
        super(RiskTick, self).__int__()
        self.symbol = EMPTY_STRING
        self.vtSymbol = EMPTY_STRING
        self.name = EMPTY_STRING
        self.volume = EMPTY_STRING
        self.delta = EMPTY_FLOAT
        self.gamma = EMPTY_FLOAT
        self.theta = EMPTY_FLOAT
        self.vega = EMPTY_FLOAT
        self.hideWave = EMPTY_FLOAT
        self.theory = EMPTY_FLOAT
        self.exePrice = EMPTY_FLOAT

        self.highPrice = EMPTY_FLOAT
        self.lowPrice = EMPTY_FLOAT
        self.lastPrice = EMPTY_FLOAT
