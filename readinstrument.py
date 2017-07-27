class MyTrade:
    def __init__(self, fac=1, c_min=5):
        self.fac = fac
        self.c_min = c_min
        self.current_high_band = 0
        self.current_low_band = 0
        self.sell_flag = False
        self.buy_flag = False
        self.current_close = 0

    def initialize_close_price(self, close_price):
        self.current_close = close_price

    def compute_current_high_band(self):
        self.current_high_band = self.current_close + (self.fac * 0.0005 * self.current_close * pow(self.c_min, 1/2))

    def compute_current_low_band(self):
        self.current_low_band = self.current_close - (self.fac * 0.0005 * self.current_close * pow(self.c_min, 1/2))

    def super_trend_decision(self, hour=0, minute=0):
        if not self.current_low_band:
            self.compute_current_low_band()

        if not self.current_high_band:
            self.compute_current_high_band()

        if not (self.sell_flag or self.buy_flag):
            if self.current_close < self.current_low_band:
                self.sell_flag = True
                self.sell_flag = False
                self.sell_instrument()
                self.compute_current_high_band()

            if self.current_close > self.current_high_band:
                self.buy_flag = True
                self.sell_flag = False
                self.buy_instrument()
                self.compute_current_low_band()

        if self.buy_flag:
            if self.current_close < self.current_low_band:
                self.sell_flag = True
                self.buy_flag = False
                self.sell_instrument()
            else:
                self.compute_current_low_band()

        if self.sell_flag:
            if self.current_close > self.current_high_band:
                self.buy_flag = True
                self.sell_flag = False
                self.buy_instrument()
            else:
                self.compute_current_high_band()

        print "Current Price %s HighBand %s Lowband %s Sell Flag %s Buy Flag %s" % (self.current_close, self.current_high_band, self.current_low_band, self.sell_flag, self.buy_flag)

    def sell_instrument(self):
        print "SELL @ %s HighBand %s LowBand %s SELL Flag %s Buy Flag %s" % (self.current_close, self.current_high_band, self.current_low_band, self.sell_flag, self.buy_flag)

    def buy_instrument(self):
        print "BUY @ %s HighBand %s LowBand %s SELL Flag  %s Buy Flag %s" % (self.current_close, self.current_high_band, self.current_low_band,self.sell_flag, self.buy_flag)

if __name__ == "__main__":
    trade = MyTrade(220.13, 10, 15)
    trade.super_trend_decision()
