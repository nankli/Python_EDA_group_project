# -*- coding: utf-8 -*-
"""
This is a modified script based on webscraper_country.py 
It is modified to save the absolute temperature data into .csv files
for a list of countries

Created on Nov 24, 2021

@author: Nan Li, Justin To
"""

import pandas as pd
import numpy as np
import urllib.request
import codecs
from urllib.parse import quote



# countries hold the list of available country names
country_source = ['svalbard-and-jan-mayen', 'canada','greenland','denmark','iran']
countries = country_source

def generate_country_absolute_csv():
    '''
    requires the list of countries generated from Part A1 above.
    '''    
    col_names = ['Year', 
                 'Month',
                 'Monthly_temperature',
                 ]

    for country in countries:
        country_url = ('http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/'
                       + quote(country, encoding='iso-8859-1')
                       + '-TAVG-Trend.txt')
        monthly_temp_line = -9999
        # open the url
        with urllib.request.urlopen(country_url) as country_file:
            country_data = country_file.readlines()    
        #process the baseline data
        month_temp = []

        for line in country_data:
                #monthly_temp_line = 55
            s = line.decode('iso-8859-1')[:-1]   
            if 'Estimated Jan 1951-Dec 1980 monthly absolute temperature (C):' in s:
                monthly_temp_line = country_data.index(line) + 2
            if country_data.index(line) == monthly_temp_line:                
                month_temp = s.split()[1:]
                break
        month_temp = [float(i) for i in month_temp]
#process temperature data   
        df = pd.DataFrame(data=None, columns=col_names)
        with urllib.request.urlopen(country_url) as country_file:
            country_data = country_file.readlines()   
        for line in country_data:
            s = str(line)[2:-3]
            if s.startswith('%') or s == ' ':
                continue
            else:
                s = s.split()
                s = [int(s[x]) if x in [0,1]  
                     else (np.nan if s[x] == 'NaN' else float(s[x]))
                     for x in range(0, 3)]
                #add base line temperature to monthly temperature

                s[2] = s[2] + month_temp[s[1] - 1]
                new_data = pd.DataFrame(data=[s], columns=col_names)
                df = pd.concat([df, new_data], ignore_index=True)

        filename = country + '_absoluteT.csv'

        df = df.set_index('Year')
        df.to_csv(filename)

generate_country_absolute_csv()