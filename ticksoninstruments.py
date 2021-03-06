#!/usr/bin/env python
import os
import time
import datetime
import sys

from kiteconnect import WebSocket
from pydblite.pydblite import Base

from constants import *
from readinstrument import MyTrade
import persist_last_value

api_key = os.getenv("API_KEY")
token = os.getenv("PUB_TOKEN")
user = os.getenv("USER_ID")
# Initialise.
# kws = WebSocket("your_api_key", "your_public_token", "logged_in_user_id")
# kws = WebSocket(api_key, token, user)
kws = WebSocket("lzxojcmp16le5ep8", "9dd813876abe0c06dfca066221f5d1da", "DD1846")

# Initialize DB.

db = Base(db_name, sqlite_compat=True)
if db.exists():
    db.open()
else:
    db.create('time', 'instrument_token', 'last_price', 'mode', 'tradeable')



# Save Initial Time
now = datetime.datetime.now()
tmp_filename = PREVIOUS_TIME+str(int(time.time()))
persist_last_value.save_object(tmp_filename, now)

factor = 1
minutes = 5
trade = MyTrade(fac=factor, c_min=minutes)


# Save ticks Data on file.
def on_tick(tick, ws):
    for each_instrument_tick in tick:
        db.insert(time=int(time.time()),
                  instrument_token=each_instrument_tick['instrument_token'],
                  last_price=each_instrument_tick['last_price'],
                  mode=each_instrument_tick['mode'],
                  tradeable=each_instrument_tick['tradeable'])
        db.commit()
        current_time = datetime.datetime.now()
        previous_time = persist_last_value.retrieve_object(tmp_filename)
        if (current_time - previous_time).total_seconds() >= minutes * 60:
            trade.initialize_close_price(each_instrument_tick['last_price'])
            trade.super_trend_decision(current_time.hour, current_time.minute)
            persist_last_value.save_object(tmp_filename, current_time)
    sys.stdout.flush()


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
