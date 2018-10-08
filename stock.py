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
    file_path_L,file_L=read_file_name(r'C:\new_tdx\T0002\export')
    dict_stocode=extr_dict_stocode(file_path_L)
    log_path='C:\\Stock_Get\\dlog.txt'
    log=exc_dlog(log_path)
    log=datetime.datetime.strptime(log, "%Y-%m-%d")
    now_time=datetime.datetime.strptime(now_time, "%Y-%m-%d")
    daysdiff=(now_time-log).days
    if (daysdiff):
        stime=(now_time-datetime.timedelta(days=daysdiff-1))
        etime=now_time
        df=pd.DataFrame()
        for file_name in file_L:
            stock_code=file_name[3:9]
            stock_data=get_h_data(stock_code,start=stime.strftime('%Y-%m-%d'),end=etime.strftime('%Y-%m-%d'))
            df=pd.concat([df,stock_data])
        with open(log_path,'a') as f:
            for i in range(daysdiff):
                dtime=(stime+datetime.timedelta(days=i)).strftime('%Y-%m-%d')
                f.write(dtime+':has been exc'+'\n')
        try:
            stock_data['stock_name']=
    print(stock_data.info())
