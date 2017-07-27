import time
from persist_last_value import PersistLastValue
from pydblite.pydblite import Base
from constants import db_name


class MyTrade:
    def __init__(self, hour, min, fac=1, c_min=5):
        self.fac = fac
        self.c_min = c_min
        self.current_high_band = 0
        self.current_low_band = 0
        # self.previous_high_band = 0
        # self.previous_low_band = 0
        self.sell_flag = "False"
        self.buy_flag = "False"
        self.hour = hour
        self.min = min
        self.multiplier = 10

    def initialization(self, close_price):
        #self.pv = PersistLastValue()
        #self.db = Base(db_name, sqlite_compat=True)
        self.current_close = close_price

        # self.close_price_list = list()
        # self.get_all_close_price_list()
        # self.current_close = self.close_price_list[-1]

    # def get_all_close_price_list(self):
    #     if not self.db.exists():
    #         raise Exception("Nothing to read")
    #     self.db.open()
    #     for record in self.db:
    #         if (int(time.time()) - record['time']) < 50*1000:
    #             self.close_price_list.append(record['last_price'])

    # def compute_atr(self):
    #     tr_list = [abs(x - self.close_price_list[i - 1]) for i, x in enumerate(self.close_price_list)][1:]
    #     return sum(i for i in tr_list) / len(tr_list)

    def compute_current_high_band(self):
        #self.current_high_band = (max(self.close_price_list) + min(self.close_price_list)) / 2 + self.multiplier * self.compute_atr()
        self.current_high_band = self.current_close + (self.fac * 0.0005 * self.current_close * pow(self.c_min, 1/2))

    def compute_current_low_band(self):
        #self.current_low_band = (max(self.close_price_list) + min(self.close_price_list)) / 2 - self.multiplier * self.compute_atr()
        self.current_low_band = self.current_close - (self.fac * 0.0005 * self.current_close * pow(self.c_min, 1/2))

    # def compute_previous_high_band(self):
    #     self.previous_high_band = self.pv.get_persisted_value()['previous_hiband']
    #     if not self.previous_high_band:
    #
    # def compute_previous_low_band(self):
    #     self.previous_low_band = self.pv.get_persisted_value()['previous_loband']
    #     if not self.previous_low_band:

    def super_trend_decision(self):
        # self.compute_previous_low_band()
        # self.compute_previous_high_band()

        if not self.current_low_band:
            self.compute_current_low_band()

        if not self.current_high_band:
            self.compute_current_high_band()

        #previous_close = self.close_price_list[-2]
        # if self.current_high_band < self.previous_high_band < previous_close:
        #     self.current_high_band = self.current_high_band
        # else:
        #     self.current_high_band = self.previous_high_band
        #
        # if self.current_low_band > self.previous_low_band > previous_close:
        #     self.current_low_band = self.current_low_band
        # else:
        #     self.current_low_band = self.previous_low_band

        #self.pv.persist_value(previous_hiband=self.current_high_band, previous_loband=self.current_low_band)

        if self.sell_flag == "False" and self.buy_flag == "False":
            if self.current_close < self.current_low_band:
                self.sell_flag = "True"
                self.sell_flag = "False"
                self.sell_instrument()
                self.compute_current_high_band()

            if self.current_close > self.current_high_band:
                self.buy_flag = "True"
                self.sell_flag = "False"
                self.buy_instrument()
                self.compute_current_low_band()

        if self.buy_flag == "True":
            if self.current_close < self.current_low_band:
                self.sell_flag = "True"
                self.buy_flag = "False"
                self.sell_instrument()
            else:
                self.compute_current_low_band()

        if self.sell_flag == "True":
            if self.current_close > self.current_high_band:
                self.buy_flag = "True"
                self.sell_flag = "False"
                self.buy_instrument()
            else:
                self.compute_current_high_band()

        print "Current Price %s HighBand %s Lowband %s Sell Flag %s Buy Flag %s" % (self.current_close, self.current_high_band, self.current_low_band, self.sell_flag, self.buy_flag)

    def sell_instrument(self):
        print "SELL @ %s HighBand %s LowBand %s SELL Flag %s Buy Flag %s" % (self.current_close, self.current_high_band, self.current_low_band, self.sell_flag, self.buy_flag)

    def buy_instrument(self):
        print "BUY @ %s HighBand %s LowBand %s SELL Flag  %s Buy Flag %s" % (self.current_close, self.current_high_band, self.current_low_band,self.sell_flag, self.buy_flag)

if __name__ == "__main__":
    # import random
    # db = Base(db_name, sqlite_compat=True)
    # if not db.exists():
    #     raise Exception("Nothing to read")
    # db.open()
    # for i in range(1, 50):
    #     db.insert(time=int(time.time()),
    #               instrument_token=784129,
    #               last_price=round(random.uniform(234.1, 238.5), 2),
    #               mode='ltp',
    #               tradeable=True)
    #     db.commit()
    #
    # for record in db:
    #     if (int(time.time()) - record['time']) < 50*6000:
    #         print record['last_price']
    #
    trade = MyTrade(220.13, 10, 15)
    trade.super_trend_decision()
