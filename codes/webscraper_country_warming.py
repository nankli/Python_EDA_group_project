# -*- coding: utf-8 -*-
"""
This is a modified script (based on webscraper_country.py from Justin) to 
get the warming temperature since 1960 data for a list of countries
http://berkeleyearth.lbl.gov/country-list/

Created on Mon Nov 15 2021
Authors: Nan Li, Justin To
"""
import re
import pandas as pd
import numpy as np
import urllib.request
import codecs
from urllib.parse import quote

# ------------------
# Part A1: This part compiles the list of countries available
# ------------------

with urllib.request.urlopen('http://berkeleyearth.lbl.gov/country-list/') as country_page:
    country_source = country_page.readlines()

# countries hold the list of available country names
countries = []
#warming hold the list of warming temperature data since 1960
warming = []
#warming_var hold the list of warming temperature data since 1960 deviation
warming_var = []
# a dictionary to keep the region categorization.  Those without a region treated
# as "None"
regions = {'Asia':[],
           'Africa':[],
           'Europe':[],
           'Oceania':[],
           'North America':[],
           'South America':[],
           'None':[]}

inv_regions = {}

# to generate list of available countries
last_country = ''
for line in country_source:
    s = codecs.decode(line, 'UTF-8')[2:]
    # find the lines that contain country names
    if s.startswith('<tr><td>'):
        start_char = s.find('region') + 8 # finds the first char of the country
        i = 1
        # loops until we find the last char of the country name
        while True:
            if not s[start_char + i] == '"':
                i += 1
            else:
                end_char = start_char + i
                break
        # stores the country name and also append it to the list of countries
        last_country = s[start_char: end_char]
        countries.append(last_country)
        
    # the lines starting with <td> only always trail a line with a country name
    # this line contains the temperature data as well as the region name, if any.
    elif s.startswith('<td>'):
        #compile the pattern to capture two float numbers
        num_p = re.compile(r'\d+\.\d+')
        #warming temperature 
        warming_t = [float(i) for i in num_p.findall(s)][0]
        #warming temperature uncertainty
        warming_t_var = [float(i) for i in num_p.findall(s)][1]
        warming.append(warming_t)
        warming_var.append(warming_t_var)
        region_found = False
        for region in regions:         
            if region in s:
                regions[region].append(last_country)
                inv_regions.update({last_country: region})
                region_found = True
                break
        if not region_found:
            regions['None'].append(last_country)
            inv_regions.update({last_country: np.nan})
    # other lines are useless
    else:
        continue
region_list = inv_regions.values()
    
# ------------------
# Part A2: This part compiles the list of countries available
# ------------------

def output_country_t_incr_list():
    '''
    requires the list of countries generated from Part A1 above.
    ''' 
    df = pd.DataFrame(data=[countries, warming, warming_var, region_list]).T
    df.columns = ['Country', 'Warming_since_1960','Warming_since_1960_uncertainty','Region']
    df = df.set_index('Country')
    df.to_csv('./data_files/country_t_incr_list.csv')

