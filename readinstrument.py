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

INITIAL_HIBAND = (high_value + low_value) / 2 + MULTIPLIER * ATR
INITIAL_LOBAND = (high_value + low_value) / 2 - MULTIPLIER * ATR

PREVIOUS_HIBAND = pv.get_persisted_value()['previous_upperband']

PREVIOUS_LOBAND = pv.get_persisted_value()['previous_lowerband']


if INITIAL_HIBAND < PREVIOUS_HIBAND < last_price_list[-2]:
	HIBAND = INITIAL_HIBAND
else:
	HIBAND = PREVIOUS_HIBAND

pv.persist_value(previous_hiband=HIBAND)

if INITIAL_LOBAND > PREVIOUS_LOBAND > last_price_list[-2]:
	LOBAND = INITIAL_LOBAND
else:
	LOBAND = PREVIOUS_LOBAND

pv.persist_value(previous_loband=LOBAND)

if last_price_list[-1] < LOBAND:
	SELL_SIGNAL = True
	print "SELL"

if last_price_list[-1] > HIBAND:
	BUY_SIGNAL = True
	print "BUY"

print pv.get_persisted_value()
print "Last" + str(last_price_list[-1])
print "Last but 1" + str(last_price_list[-2])
print HIBAND
print LOBAND
print INITIAL_LOBAND
print INITIAL_HIBAND

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