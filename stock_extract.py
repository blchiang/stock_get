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
if __name__ == "__main__":
    file_path_L,file_L=read_file_name(r'C:\new_tdx\T0002\export')
    dict_stocode=extr_dict_stocode(file_path_L)
    for k in range(len(file_path_L)):#删除所有文件第1行
            total_line=comp_line(file_path_L[k])
            erase(file_path_L[k],[1,2,total_line])
    df=pd.DataFrame(columns=range(7))
    df['stockname']=[]
    df['stockcode']=[]
    for i in range(len(file_L)):
        try:
            df_temp=pd.read_table(file_path_L[i],encoding="gb18030",header=None)
        except:
            continue
        stock_name=dict_stocode[file_L[i][3:9]]
        df_temp['stockname']=stock_name
        df_temp['stockcode']=file_L[i][3:9]
        df=pd.concat([df,df_temp],ignore_index=True)
    df.rename(columns={0:'date', 1:'open', 2:'high',3:'low',4:'close',5:'volume',6:'amount'}, inplace = True)
    df['date'] = pd.to_datetime(df['date'])
    print(df.info())