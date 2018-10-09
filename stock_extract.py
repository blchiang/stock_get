# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# =============================================================================
# 1、读取指定目录下的所有文件
# 2、读取文件，正则匹配出需要的内容，获取文件名
# 3、打开此文件(可以选择打开可以选择复制到别的地方去)
# =============================================================================
import os
import pandas as pd
from save_dict import *
import pymssql
#读取路径
def read_file_name(file_dir):
    file_path_L=[]
    file_L=[]
    for root,dirs,files in os.walk(file_dir):
        for file in files:
            file_path_L.append(os.path.join(root,file))
            file_L.append(os.path.join(file))
    return file_path_L,file_L
#删除文本文档erase_line行
def erase(file,erase_line):
    temp=0
    file_data=''
    with open(file, "r", encoding="gb18030") as f:
        for line in f:
            temp+=1
            if temp in erase_line:
                continue
            else:
                file_data += line
    with open(file,"w",encoding="gb18030") as f:
        f.write(file_data)
#一共多少行
def comp_line(file):
    temp=0
    with open(file, "r", encoding="gb18030") as f:
        for line in f:
            temp+=1
    return temp

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
    file_path_L,file_L=read_file_name(r'D:\blj\finance\TDX')
    dict_stocode=extr_dict_stocode(file_path_L)
    for k in range(len(file_path_L)):#删除所有文件第1行
            total_line=comp_line(file_path_L[k])
            erase(file_path_L[k],[1,2,total_line])
    df=pd.DataFrame(columns=range(7))
    df['stockcode']=[]
    for i in range(len(file_L)):
        try:
            df_temp=pd.read_table(file_path_L[i],encoding="gb18030",header=None)
        except:
            continue
        df_temp['stockcode']=file_L[i][3:9]
        df=pd.concat([df,df_temp],ignore_index=True)
    df.rename(columns={0:'date', 1:'open', 2:'high',3:'low',4:'close',5:'volume',6:'amount'}, inplace = True)
    #df['date'] = pd.to_datetime(df['date'])
    stock_basics=get_stock_basics()
    stock_basics=stock_basics.reset_index()
    stock_basics.rename(columns={'code':'stockcode'},inplace = True)
    stoct_bsc=stock_basics.loc[:,['stockcode','name','industry','area'] ]
    result=pd.merge(df,stoct_bsc,on='stockcode',how='left')
      #行业分类
#==============================================================================
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
    result.to_csv('test.csv')
    print(result.info())
    #to sql
    ms = MSSQL(host="127.0.0.1:1433",user="sa",pwd="sqladmin",db="stock_manage")
    reslist = ms.ExecQuery("select * from stockdata")
    ms.ExecNonQuery("insert into stockdata(date) values('2018-09-09')")
    for index, row in result.iterrows():
        print(row)
    df0 = pd.read_sql("select * from stockdata",ms.c)