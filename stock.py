# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 16:24:30 2018

@author: lenovo
"""

from tushare import *
import datetime
from stock_extract import *
import pymssql
import gc
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

##定义操作数据库类
class MSSQL:
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        #查询完毕后必须关闭连接
        self.conn.close()
        return resList
        
    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
        
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
            stock_data_temp=get_k_data(code,start_date=stime.strftime('%Y-%m-%d'),end=etime.strftime('%Y-%m-%d'))
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
    print(result)
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
    ms = MSSQL(host="127.0.0.1:1433",user="sa",pwd="sqladmin",db="stock_manage")
    reslist = ms.ExecQuery("select * from stockdata")
    for index, row in result.iterrows():
    #遍历导入
        date = row['date']
        if (date == 'nan'):
            date = ''
         
        open_p = row['open']
        if (open_p == 'nan'):
            open_p = ''
        
        close_p = row['close']
        if (close_p == 'nan'):
            close_p = ''
            
        low_p = row['low']
        if (low_p == 'nan'):
            low_p = ''
        
        high_p = row['high']
        if (high_p == 'nan'):
            high_p = ''
        
        volume = int(row['volume'])
        if (volume == 'nan'):
            volume = ''
            
        name = row['name']
        if (name == 'nan'):
            name = ''
            
        stockcode = row['stockcode']
        if (stockcode == 'nan'):
            stockcode = ''
            
        industry = row['industry']
        if (industry == 'nan'):
            industry = ''
            
        area = row['area']
        if (area == 'nan'):
            area = ''
            
        amount = row['amount']
        if (amount == 'nan'):
            amount = ''
        
        ms.ExecNonQuery("insert into stockdata values('%s','%f','%f','%f','%f','%d','%f','%s','%s','%s','%s')"%(date,open_p,close_p,high_p,low_p,volume,amount,stockcode,name,industry,area))