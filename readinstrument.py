class MyTrade:
    def __init__(self, fac=1, c_min=5):
        self.fac = fac
        self.c_min = c_min
        self.current_high_band = 0.0
        self.current_low_band = 0.0
        self.sell_flag = "False"
        self.buy_flag = "False"
        self.current_close = 0.0
        from kiteconnect import KiteConnect
        self.kite = KiteConnect(api_key="lzxojcmp16le5ep8")  # paid app
        self.kite.set_access_token('phuz7rw7g3459xjm8z0754n3da4o54yj')

    def initialize_close_price(self, close_price):
        self.current_close = close_price

    def compute_current_high_band(self):
        return self.current_close + (self.fac*25)#(self.fac * 0.0005 * self.current_close * pow(self.c_min, 1/2))

    def compute_current_low_band(self):
        return self.current_close - (self.fac*25)#(self.fac * 0.0005 * self.current_close * pow(self.c_min, 1/2))

    def super_trend_decision(self, hour=0, minute=0):
        if not self.current_low_band:
            self.current_low_band = self.compute_current_low_band()

        if not self.current_high_band:
            self.current_high_band = self.compute_current_high_band()

        print "Close Price %s" % self.current_close

        # Should Enter Only Once
        if self.sell_flag == "False" and self.buy_flag == "False":
            if self.current_close < self.current_low_band:
                self.sell_flag = "True"
                self.buy_flag = "False"
                self.sell_instrument()
                self.current_high_band = self.compute_current_high_band()
                return

            if self.current_close > self.current_high_band:
                self.buy_flag = "True"
                self.sell_flag = "False"
                self.buy_instrument()
                self.current_low_band = self.compute_current_low_band()
                return

        if self.buy_flag == "True":
            if self.current_close < self.current_low_band:
                self.sell_flag = "True"
                self.buy_flag = "False"
                self.sell_instrument()
                self.sell_instrument()
            else:
                if self.current_low_band < self.compute_current_low_band():
                    self.current_low_band = self.compute_current_low_band()
                    self.current_high_band = self.compute_current_high_band()
                    print "Recomputed in BUY High Band %s LowBand %s" % (self.current_high_band, self.current_low_band)
            return

        if self.sell_flag == "True":
            if self.current_close > self.current_high_band:
                self.buy_flag = "True"
                self.sell_flag = "False"
                self.buy_instrument()
                self.buy_instrument()
            else:
                if self.current_high_band > self.compute_current_high_band():
                    self.current_high_band = self.compute_current_high_band()
                    self.current_low_band = self.compute_current_low_band()
                    print "Recomputed in SELL High Band %s LowBand %s" % (self.current_high_band, self.current_low_band)

            return

    def sell_instrument(self):
        try:
            order_id = self.kite.order_place(tradingsymbol="BANKNIFTY17SEPFUT",
                                        exchange="NFO",
                                        transaction_type="SELL",
                                        quantity=40,
                                        order_type="MARKET",
                                        product="MIS")

            print("Order placed. ID is", order_id)
        except Exception as e:
            print("Order placement failed", e.message)

        print "SELL @ %s HighBand %s LowBand %s SELL Flag %s Buy Flag %s" % (self.current_close, self.current_high_band, self.current_low_band, self.sell_flag, self.buy_flag)

    def buy_instrument(self):
        try:
            order_id = self.kite.order_place(tradingsymbol="BANKNIFTY17SEPFUT",
                                        exchange="NFO",
                                        transaction_type="BUY",
                                        quantity=40,
                                        order_type="MARKET",
                                        product="MIS")

            print("Order placed. ID is", order_id)
        except Exception as e:
            print("Order placement failed", e.message)

        print "BUY @ %s HighBand %s LowBand %s SELL Flag  %s Buy Flag %s" % (self.current_close, self.current_high_band, self.current_low_band,self.sell_flag, self.buy_flag)


if __name__ == "__main__":
    trade = MyTrade(220.13, 10, 15)
    trade.super_trend_decision()
