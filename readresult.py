# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 12:50:27 2018

@author: lenovo
"""

import pandas as pd
import tushare as ts
from tushare.stock import cons as ct
stockgem=ts.get_gem_classified()
stockgem.to_excel('stockgem.xls')
conn=ts.get_apis()
tp=ts.bar('600000',conn,start_date='2018-08-15', end_date='2018-09-15',freq='XD', asset='E',adj='qfq')
ts.get_k_data()
df=ts.bar('600000',conn)
print(ts.get_h_data('600000',start='2018-09-25', end='2018-10-10'))
print(df)
df.drop(columns=['p_change'],inplace=True)
df['p_change']
print(df['vol'])
ts.MA()
stock_basics=ts.get_stock_basics()
stock_data=pd.DataFrame()
for code in stock_basics.index:
    stock_data_temp=ts.bar(code,conn,start_date='2018-09-25', end_date='2018-10-10')
    print(stock_data_temp)
mkcode = ts.get_mkcode(code='600000', asset='E', xapi=None)
ct._market_code('600000')
print(tp['vol']*100)
192361952.0
