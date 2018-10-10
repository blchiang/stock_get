# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 12:50:27 2018

@author: lenovo
"""

import pandas as pd
import tushare as ts
stockgem=ts.get_gem_classified()
stockgem.to_excel('stockgem.xls')
conn=ts.get_apis()
df=ts.bar('600000',conn,start_date='2018-09-25', end_date='2018-10-10')
df=ts.bar('600000',conn)
print(ts.get_h_data('600000',start='2018-09-25', end='2018-10-10'))
print(df)