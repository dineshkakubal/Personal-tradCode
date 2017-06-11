from kiteconnect import WebSocket
import numpy as np

# Initialise.
kws = WebSocket("lzxojcmp16le5ep8", "c0b8c02577a6ec00dd3ddb622aa71c60", "DD1846")

# Callback for tick reception.
def on_tick(tick, ws):
        print tick#["last_price"]
	#print type(tick)
	#print tick.split()[1]
	#print xx[0].split()
	#print xx.split()[1].split(sep=",")[0]
	#print len(np.array(tick))
	
	
# Callback for successful connection.
def on_connect(ws):
	# Subscribe to a list of instrument_tokens (VEDANTA and ACC here).
	ws.subscribe([784129])

	# Set RELIANCE to tick in `full` mode.
	ws.set_mode(ws.MODE_LTP, [784129])

# Assign the callbacks.
kws.on_tick = on_tick
kws.on_connect = on_connect

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()
