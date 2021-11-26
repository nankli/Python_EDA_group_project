# -*- coding: utf-8 -*-
"""
This is a modified script based on webscraper.py 
It is modified to save the absolute temperature data into .csv files
for global area

Created on Nov 24, 2021

@author: Nan Li, Justin To
"""

import pandas as pd
import numpy as np
import urllib.request

with urllib.request.urlopen('http://berkeleyearth.lbl.gov/auto/Global/Complete_TAVG_complete.txt') as f:
    html = f.readlines()
    
col_names = ['Year', 
             'Month',
             'Monthly_temperature',
             ]
monthly_temp_line = -9999
month_temp=[]
df = pd.DataFrame(data=None, columns=col_names)
for line in html:
         #monthly_temp_line = 55
    s = line.decode('iso-8859-1')[:-1]   
    if 'Estimated Jan 1951-Dec 1980 monthly absolute temperature:' in s:
        monthly_temp_line = html.index(line) + 2
    if html.index(line) == monthly_temp_line:                
        month_temp = s.split()[1:]
        break
month_temp = [float(i) for i in month_temp]
for line in html:
    s= str(line)[2:-3]
    if s.startswith('%') or s == ' ':
        continue
    else:
        s = s.split()
        s = [int(s[x]) if x in [0,1]  
             else (np.nan if s[x] == 'NaN' else float(s[x]))
             for x in range(0, 3)]
        # print(s.split())
        s[2] = s[2] + month_temp[s[1] - 1]
        new_data = pd.DataFrame(data=[s], columns=col_names)
        df = pd.concat([df, new_data], ignore_index=True)

df = df.set_index('Year')
df.to_csv('GlobalTemp_absoluteT.csv')

    
    
# with open('test.txt', 'w') as file:
#     file.write(html)    