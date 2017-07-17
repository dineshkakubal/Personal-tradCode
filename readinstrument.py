import time

from pydblite.pydblite import Base

from constants import db_name
from persist_last_value import PersistLastValue

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
    if (int(time.time()) - record['time']) < 50 * 6000:
        last_price_list.append(record['last_price'])

print last_price_list
# Variables
#
# BUY_SIGNAL = False
# SELL_SIGNAL = False
# high_value = max(last_price_list)
# low_value = min(last_price_list)
#
# MULTIPLIER = 10
# tr_list = [abs(x - last_price_list[i - 1]) for i, x in enumerate(last_price_list)][1:]
# ATR = sum(i for i in tr_list) / len(tr_list)
#
# INITIAL_HIBAND = (high_value + low_value) / 2 + MULTIPLIER * ATR
# INITIAL_LOBAND = (high_value + low_value) / 2 - MULTIPLIER * ATR
#
# PREVIOUS_HIBAND = pv.get_persisted_value()['previous_upperband']
#
# PREVIOUS_LOBAND = pv.get_persisted_value()['previous_lowerband']
#
# if INITIAL_HIBAND < PREVIOUS_HIBAND < last_price_list[-2]:
#     HIBAND = INITIAL_HIBAND
# else:
#     HIBAND = PREVIOUS_HIBAND
#
# pv.persist_value(previous_hiband=HIBAND)
#
# if INITIAL_LOBAND > PREVIOUS_LOBAND > last_price_list[-2]:
#     LOBAND = INITIAL_LOBAND
# else:
#     LOBAND = PREVIOUS_LOBAND
#
# pv.persist_value(previous_loband=LOBAND)
#
# if last_price_list[-1] < LOBAND:
#     SELL_SIGNAL = True
#     print "SELL"
#
# if last_price_list[-1] > HIBAND:
#     BUY_SIGNAL = True
#     print "BUY"
#
# print pv.get_persisted_value()
# print "Last" + str(last_price_list[-1])
# print "Last but 1" + str(last_price_list[-2])
# print HIBAND
# print LOBAND
# print INITIAL_LOBAND
# print INITIAL_HIBAND

#
# if ((current INI_HI_BAND < previous HI_BAND < previous close))
#
# HI_BAND = INI_HI_BAND
#
# else
#
# HI_BAND = previous HI_BAND
#
#
# if ((current INI_LO_BAND > previous LO_BAND) > previous close))
#
# LO_BAND = INI_LO_BAND
#
# else
#
# LO_BAND = previous LO_BAND
#
#
# if (candle close > HI_BAND)
# BUY_SIGNAL=1
#
# if (candle close < LO_BAND)
# SELL_SIGNAL=1
#

# import csv
# import numpy as np
#
#
# NIClose=[]
# NIHour=[]
# NIMin=[]
# Sell=[]
# Buy=[]
#
#
# def get_data(Filename):
#     with open(Filename, 'r') as csvFile:
#         File_Reader=csv.reader(csvFile)
#         next(File_Reader)
#         for row in File_Reader:
#             NIClose.append(float(row[7]))
#             NIHour.append(float(row[2]))
#             NIMin.append(float(row[3]))
#     return
#
#
# def UPBand(Close,Fact,C_Min):
#     return Close + (Fact * 0.0005 * Close * pow(C_Min,1/2))
#
#
# def LOBand(Close,Fact,C_Min):
#     return Close - (Fact * 0.0005 * Close * pow(C_Min,1/2))
#
#
# def STrend(CL,HR,MI,FAC,CNAD_MIN):
#     UBand = LBand = 0
#     BFlag = SFlag = 0
#     for cntr in range(0, len(CL)):
#         if UBand==0 and LBand==0:
#             UBand = UPBand(CL[cntr],FAC,CNAD_MIN)
#             LBand = LOBand(CL[cntr],FAC,CNAD_MIN)
#         #print(UBand, LBand,CL[cntr])
#         if BFlag==0 and SFlag==0 and CL[cntr]>UBand:
#             BFlag=1
#             Buy.append(float(CL[cntr]))
#         if BFlag==0 and SFlag==0 and CL[cntr]<LBand:
#             SFlag=1
#             Sell.append(float(CL[cntr]))
#         if BFlag==1 and CL[cntr]<LBand:
#             SFlag = 1
#             BFlag = 0
#             Sell.append(float(CL[cntr]))
#             Sell.append(float(CL[cntr]))
#         if SFlag==1 and CL[cntr]>UBand:
#             BFlag = 1
#             SFlag = 0
#             Buy.append(float(CL[cntr]))
#             Buy.append(float(CL[cntr]))
#         if HR[cntr] == float(15) and MI[cntr]==float(10) and BFlag == 1:
#             Sell.append(float(CL[cntr]))  #Sell code here
#             BFlag = SFlag = 0
#             UBand = LBand = 0
#         if HR[cntr] == float(15) and MI[cntr]==float(10) and SFlag == 1:
#             Buy.append(float(CL[cntr]))
#             BFlag = SFlag = 0
#             UBand = LBand = 0
#     return
#
#
#
# get_data('VEDL-EQ.csv')#('BANKNIFTY17JULFUT_5min_2.csv')
# STrend(NIClose,NIHour,NIMin,1,5)
# S1=np.array(Sell)
# B1=np.array(Buy)
# print(len(Sell))
# #print(np.sum(S1))
# print(len(Buy))
# print(np.sum(S1)- np.sum(B1))
# print (S1 - B1)
# #print (Sell)
