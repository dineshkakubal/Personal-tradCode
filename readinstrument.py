import time
from persist_last_value import PersistLastValue
from pydblite.pydblite import Base
from constants import db_name
# for i in range(1, 50):
# 	db.insert(time=int(time.time()),
# 			  instrument_token=784129,
# 			  last_price=round(random.uniform(234.1, 238.5), 2),
# 			  mode='ltp',
# 			  tradeable=True)
# 	db.commit()


class Trade:
    def __init__(self, current_close_price, hour, min, fac=1, c_min=5):
        self.current_close = current_close_price
        self.fac = fac
        self.c_min = c_min
        self.current_high_band = 0
        self.current_low_band = 0
        self.previous_high_band = 0
        self.previous_low_band = 0
        self.hour = hour
        self.min = min
        self.buy_flag = False
        self.sell_flag = False
        self.multiplier = 10
        self.close_price_list = list()
        self.pv = PersistLastValue()
        self.db = Base(db_name, sqlite_compat=True)

    def get_all_close_price_list(self):
        if not self.db.exists():
            raise Exception("Nothing to read")
        self.db.open()
        for record in self.db:
            if (int(time.time()) - record['time']) < 50*6000:
                self.close_price_list.append(record['last_price'])

    def compute_atr(self):
        tr_list = [abs(x - self.close_price_list[i - 1]) for i, x in enumerate(self.close_price_list)][1:]
        return sum(i for i in tr_list) / len(tr_list)

    def compute_current_high_band(self):
        self.current_high_band = (max(self.close_price_list) + min(self.close_price_list)) / 2 + self.multiplier * self.compute_atr()

    def compute_current_low_band(self):
        self.current_low_band = (max(self.close_price_list) + min(self.close_price_list)) / 2 - self.multiplier * self.compute_atr()

    def compute_previous_high_band(self):
        if not self.previous_high_band:
            phb = self.current_close + (self.fac * 0.0005 * self.current_close * pow(self.c_min, 1/2))
        else:
            phb = self.pv.get_persisted_value()['previous_upperband']
        self.previous_high_band = phb

    def compute_previous_low_band(self):
        if not self.previous_low_band:
            plb = self.current_close - (self.fac * 0.0005 * self.current_close * pow(self.c_min, 1/2))
        else:
            plb = self.pv.get_persisted_value()['previous_lowerband']
        self.previous_low_band = plb

    def super_trend_decision(self):
        self.get_all_close_price_list()
        self.compute_previous_low_band()
        self.compute_previous_high_band()
        self.compute_current_low_band()
        self.compute_current_high_band()

        previous_close = self.close_price_list[-2]
        if not self.current_high_band < self.previous_high_band < previous_close:
            self.current_high_band = self.previous_high_band

        if not self.current_low_band > self.previous_low_band > previous_close:
            self.current_low_band = self.previous_low_band

        self.pv.persist_value(previous_hiband=self.current_high_band, previous_loband=self.current_low_band)

        if self.current_close < self.current_low_band:
            self.buy_flag = True
            self.sell_instrument()

        if self.current_close > self.current_high_band:
            self.buy_flag = True
            self.buy_instrument()

    @staticmethod
    def sell_instrument():
        print "SELL"

    @staticmethod
    def buy_instrument():
        print "BUY"


