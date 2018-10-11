# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 16:57:40 2018

@author: lenovo
"""

import sys
import os
import pandas as pd
for root,dirs,files in os.walk('C:\\Users\\lenovo\\Anaconda3\\lib\\site-packages\\tushare'):
    sys.path.append(root)
for root,dirs,files in os.walk('C:\\Users\\lenovo\\Anaconda3\\lib\\site-packages\\lxml'):
    sys.path.append(root)
df=pd.DataFrame()
from tushare import __init__
import datetime
import pymssql
import gc
import os
import pandas as pd
import re
from .. import etree
