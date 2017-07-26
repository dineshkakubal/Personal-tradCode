
class Trade:
    def __init__(self, close_price, hour, min, fac=1, c_min=5):
        self.close = close_price
        self.fac = fac
        self.c_min = c_min
        self.high_band = 0
        self.low_band = 0
        self.hour = hour
        self.min = min
        self.buy_flag = False
        self.sell_flag = False

    def compute_high_band(self):
        return self.close + (self.fac * 0.0005 * self.close * pow(self.c_min, 1/2))

    def compute_low_band(self):
        return self.close - (self.fac * 0.0005 * self.close * pow(self.c_min, 1/2))

    def super_trend_decision(self):

        if not self.high_band:
            self.high_band = self.compute_high_band()

        if not self.low_band:
            self.low_band = self.compute_low_band()

        if not (self.buy_flag and self.sell_flag):
            if self.close > self.high_band:
                self.buy_flag = True
                self.buy_instrument()
            else:
                self.sell_flag = True
                self.sell_instrument()

        if self.buy_flag:
            if self.close < self.low_band:
                self.sell_flag = True
                self.buy_flag = False
                self.sell_instrument()

        if self.sell_flag:
            if self.close > self.high_band:
                self.buy_flag = True
                self.sell_flag = False
                self.buy_instrument()

        if self.hour == 15 and self.min == 10 and self.buy_flag:
            # Call Sell Code and reset flags
            self.sell_instrument()
            self.sell_flag = False
            self.buy_flag = False

        if self.hour == 15 and self.min == 10 and self.sell_flag:
            # Call Buy Code and reset flags
            self.buy_instrument()
            self.buy_flag = False
            self.sell_flag = False

    @staticmethod
    def sell_instrument(self):
        print "SELL"

    @staticmethod
    def buy_instrument(self):
        print "BUY"
