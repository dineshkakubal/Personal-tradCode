import random
import time
from persist_last_value import PersistLastValue
from pydblite.pydblite import Base

from constants import db_name
pv = PersistLastValue()
db = Base(db_name, sqlite_compat=True)

if not db.exists():
	raise Exception("Nothing to read")
db.open()


# for i in range(1, 50):
# 	db.insert(time=int(time.time()),
# 			  instrument_token=784129,
# 			  last_price=round(random.uniform(234.1, 238.5), 2),
# 			  mode='ltp',
# 			  tradeable=True)
# 	db.commit()
last_price_list = list()
for record in db:
	if (int(time.time()) - record['time']) < 50*6000:
		last_price_list.append(record['last_price'])


# Variables

BUY_SIGNAL = False
SELL_SIGNAL = False
high_value = max(last_price_list)
low_value = min(last_price_list)

MULTIPLIER = 10
tr_list = [abs(x - last_price_list[i - 1]) for i, x in enumerate(last_price_list)][1:]
ATR = sum(i for i in tr_list) / len(tr_list)

INITIAL_UPPERBAND = (high_value + low_value) / 2 + MULTIPLIER * ATR
INITIAL_LOWERBAND = (high_value + low_value) / 2 - MULTIPLIER * ATR

PREVIOUS_FINAL_UPPERBAND = pv.get_persisted_value()['previous_upperband']

PREVIOUS_FINAL_LOWERBAND = pv.get_persisted_value()['previous_lowerband']


if INITIAL_UPPERBAND < PREVIOUS_FINAL_UPPERBAND < last_price_list[-2]:
	FINAL_UPPERBAND = INITIAL_UPPERBAND
else:
	FINAL_UPPERBAND = PREVIOUS_FINAL_UPPERBAND

pv.persist_value(previous_upperband=FINAL_UPPERBAND)

if INITIAL_LOWERBAND > PREVIOUS_FINAL_LOWERBAND > last_price_list[-2]:
	FINAL_LOWERBAND = INITIAL_LOWERBAND
else:
	FINAL_LOWERBAND = PREVIOUS_FINAL_LOWERBAND

pv.persist_value(previous_lowerband=FINAL_LOWERBAND)

if last_price_list[-1] < FINAL_LOWERBAND:
	SELL_SIGNAL = True
	print "SELL"

if last_price_list[-1] > FINAL_UPPERBAND:
	BUY_SIGNAL = True
	print "BUY"

print pv.get_persisted_value()
print "Last" + str(last_price_list[-1])
print "Last but 1" + str(last_price_list[-2])
print FINAL_UPPERBAND
print FINAL_LOWERBAND
print INITIAL_LOWERBAND
print INITIAL_UPPERBAND

'''
if ((current INI_HI_BAND < previous HI_BAND < previous close))

HI_BAND = INI_HI_BAND

else

HI_BAND = previous HI_BAND


if ((current INI_LO_BAND > previous LO_BAND) > previous close))

LO_BAND = INI_LO_BAND

else

LO_BAND = previous LO_BAND


if (candle close > HI_BAND)
BUY_SIGNAL=1

if (candle close < LO_BAND)
SELL_SIGNAL=1
'''