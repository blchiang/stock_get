# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 16:24:30 2018

@author: lenovo
"""

from tushare import *
import datetime
from stock_extract import *
now_time=datetime.datetime.now().strftime('%Y-%m-%d')
def exc_dlog(file):
    with open(file,'r') as f:
        text=f.readlines()
        log=text.pop()
        try:
            log=re.findall(r'.*\d',log)[0]
        except:
            log=text.pop()
            log=re.findall(r'.*\d',log)[0]
    return log
if __name__ == "__main__":
    stock_basics=get_stock_basics()
    print(stock_basics.info())
    log_path='C:\\Users\\lenovo\\Desktop\\stock_get\\dlog.txt'
    log=exc_dlog(log_path)
    log=datetime.datetime.strptime(log, "%Y-%m-%d")
    now_time=datetime.datetime.strptime(now_time, "%Y-%m-%d")
    daysdiff=(now_time-log).days
    stock_basics=get_stock_basics()
    if (daysdiff):
        stime=(now_time-datetime.timedelta(days=daysdiff-1))
        etime=now_time
        stock_data=pd.DataFrame()
        for code in stock_basics.index:
            stock_data_temp=get_h_data(code,start=stime.strftime('%Y-%m-%d'),end=etime.strftime('%Y-%m-%d'))
            stock_data_temp['stockcode']=code
            stock_data=pd.concat([stock_data,stock_data_temp])
        with open(log_path,'a') as f:
            for i in range(daysdiff):
                dtime=(stime+datetime.timedelta(days=i)).strftime('%Y-%m-%d')
                f.write(dtime+':has been exc'+'\n')
    stock_data=stock_data.reset_index()
    stock_basics=stock_basics.reset_index()
    stock_basics.rename(columns={'code':'stockcode'},inplace = True)
    stock_bsc=stock_basics.loc[:,['stockcode','name','industry','area'] ]
    result=pd.merge(stock_data,stock_bsc,on='stockcode',how='left')
#==============================================================================
#     #行业分类
#     industry_classified=get_industry_classified()
#     industry_classified.rename(columns={'code':'stockcode','c_name':'industry_classified'},inplace = True)
#     result=pd.merge(result,industry_classified.loc[:,['stockcode','industry_classified']],on='stockcode',how='left')
#     #概念分类
#     concept_classified=get_concept_classified()
#     concept_classified.rename(columns={'code':'stockcode','c_name':'concept_classified'},inplace = True)
#     result=pd.merge(result,concept_classified.loc[:,['stockcode','concept_classified']],on='stockcode',how='left')
#     #创业板分类
#     gem_classified=get_gem_classified()
#     gem_classified['gem_classified']='创业板'
#     gem_classified.rename(columns={'code':'stockcode'},inplace = True)
#     result=pd.merge(result,gem_classified.loc[:,['stockcode','gem_classified']],on='stockcode',how='left')
#==============================================================================
