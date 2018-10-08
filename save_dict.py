# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 20:26:46 2018

@author: lpp
"""

#提取股票代码名称字典
import re
def extr_dict_stocode(file_path_L):
    dict_stocode={}
    for path in file_path_L:
        f=open(path,'r')
        str1=f.readline()
        code=re.findall(r'\d{6}',str1)[0]
        name=re.findall(r'\s.* 日',str1)[0]
        name=name[1:-2]
        dict_stocode.update({code:name})
    return dict_stocode