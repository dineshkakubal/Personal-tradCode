#!/usr/bin/env python
import os
import time
import datetime

from kiteconnect import WebSocket
from pydblite.pydblite import Base

from constants import db_name
from constants import instruments
from trading import Trade

api_key = os.getenv("API_KEY")
token = os.getenv("PUB_TOKEN")
user = os.getenv("USER_ID")
# Initialise.
# kws = WebSocket("your_api_key", "your_public_token", "logged_in_user_id")
kws = WebSocket(api_key, token, user)

# Initialize DB.

db = Base(db_name, sqlite_compat=True)
if db.exists():
    db.open()
else:
    db.create('time', 'instrument_token', 'last_price', 'mode', 'tradeable')


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
        trade = Trade(each_instrument_tick['last_price'], hour=now.hour, min=now.minute)
        trade.super_trend_decision()


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
