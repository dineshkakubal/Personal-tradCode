#!/usr/bin/env python
import os
import time
import datetime

from kiteconnect import WebSocket
from pydblite.pydblite import Base

from constants import db_name
from constants import instruments
from readinstrument import MyTrade

api_key = os.getenv("API_KEY")
token = os.getenv("PUB_TOKEN")
user = os.getenv("USER_ID")
# Initialise.
# kws = WebSocket("your_api_key", "your_public_token", "logged_in_user_id")
# kws = WebSocket(api_key, token, user)
kws = WebSocket("lzxojcmp16le5ep8", "c0b8c02577a6ec00dd3ddb622aa71c60", "DD1846")

# Initialize DB.

db = Base(db_name, sqlite_compat=True)
if db.exists():
    db.open()
else:
    db.create('time', 'instrument_token', 'last_price', 'mode', 'tradeable')

trade = MyTrade()


# Save ticks Data on file.
def on_tick(tick, ws):
    for each_instrument_tick in tick:
        db.insert(time=int(time.time()),
                  instrument_token=each_instrument_tick['instrument_token'],
                  last_price=each_instrument_tick['last_price'],
                  mode=each_instrument_tick['mode'],
                  tradeable=each_instrument_tick['tradeable'])
        db.commit()
        now = datetime.datetime.now()
        trade.initialize_close_price(each_instrument_tick['last_price'])
        trade.super_trend_decision(now.hour, now.minute)
    time.sleep(60)


# Callback for successful connection.
def on_connect(ws):
    # Subscribe to a list of instrument_tokens (VEDANTA and ACC here).
    ws.subscribe([instruments])

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_LTP, [instruments])


# Assign the callbacks.
kws.on_tick = on_tick
kws.on_connect = on_connect

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()
