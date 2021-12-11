# -*- coding: utf-8 -*-
"""
A simple script from downloading data from the "Time Series" section of
the Berkeley Earth database (berkeleyearth.org/data/).  This grabs the data
for the north and south hemispheres.

To use, just place this script in the folder that you would like to
download the data to, and run this script.

Created on a Windows 7 machine using Spyder, let me know if you have issues
with opening it.

Created on Sat Nov 13 22:26:57 2021

@author: Justin To
"""

import pandas as pd
import numpy as np
import urllib.request
import codecs
from urllib.parse import quote

# ------------------
# Part A: This part saves the text files to the local drive and also prepares a csv.
# ------------------

# Note: for the main city page (i.e. the one with graphs), utf-8 should be used
# for the text file, use iso-8859-1
def generate_hemispheres_csv():
    '''
    only the north and south hemisphere text files are parsed.
    '''    
    col_names = ['Year', 
                 'Month',
                 'Monthly_Anomaly',
                 'Monthly_Uncertainty',
                 'Annual_Anomaly',
                 'Annual_Uncertainty',
                 'Five_year_Anomaly',
                 'Five_year_Uncertainty',
                 'Ten_year_Anomaly',
                 'Ten_year_Uncertainty',
                 'Twenty_year_Anomaly',
                 'Twenty_year_Uncertainty']
    
    for hemisphere in ['northern', 'southern']:
        hemisphere_url = ('http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/'
                          + hemisphere
                          + '-hemisphere-TAVG-Trend.txt')
        # open the url
        with urllib.request.urlopen(hemisphere_url) as hemisphere_file:
            hemisphere_data = hemisphere_file.readlines()    
   
        df = pd.DataFrame(data=None, columns=col_names)

        for line in hemisphere_data:
            s = str(line)[2:-3]
            if s.startswith('%') or s == ' ':
                continue
            else:
                s = s.split()
                s = [int(s[x]) if x in [0,1]  
                     else (np.nan if s[x] == 'NaN' else float(s[x]))
                     for x in range(0, 12)]
                # print(s.split())
                new_data = pd.DataFrame(data=[s], columns=col_names)
                df = pd.concat([df, new_data], ignore_index=True)

        filename = '../data_files/' + hemisphere + '.csv'

        df = df.set_index('Year')
        df.to_csv(filename)

# ------------------
# Part C: This part saves the other data found in the text files into a csv.
# ------------------
    
def generate_metadata_csv():
    '''
    only the north and south hemisphere text files are parsed.
    '''
    monthly_temp_line = -9999
    
    col_names = ['Hemisphere',
                 'Baseline_temp',
                 'Baseline_temp_uncertainty',
                 'Jan_temp',
                 'Jan_uncertainty',
                 'Feb_temp',
                 'Feb_uncertainty',
                 'Mar_temp',
                 'Mar_uncertainty',
                 'Apr_temp',
                 'Apr_uncertainty',
                 'May_temp',
                 'May_uncertainty',
                 'Jun_temp',
                 'Jun_uncertainty',
                 'Jul_temp',
                 'Jul_uncertainty',
                 'Aug_temp',
                 'Aug_uncertainty',
                 'Sep_temp',
                 'Sep_uncertainty',
                 'Oct_temp',
                 'Oct_uncertainty',
                 'Nov_temp',
                 'Nov_uncertainty',
                 'Dec_temp',
                 'Dec_uncertainty']
    
    df = pd.DataFrame(data=None, columns=col_names)
    
    for hemisphere in ['northern', 'southern']:
        
        print(f'Handling {hemisphere} hemisphere...')     
        
           
        # creates and then open the url for the other data    
        hemisphere_url = ('http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/'
                          + hemisphere
                          + '-hemisphere-TAVG-Trend.txt')

        with urllib.request.urlopen(hemisphere_url) as hemisphere_file:
            hemisphere_data = hemisphere_file.readlines()    
        
        for line in hemisphere_data:
            try:
                s = line.decode('iso-8859-1')[:-1]
            except:
                print(line)
                return 0
            # extracts meta data one by one starting from the water percentage.                
            
            if 'Estimated Jan 1951-Dec 1980 absolute temperature (C):' in s:
                Baseline_temp = float(s.split()[s.split().index('(C):') +1])
                Baseline_temp_uncertainty = float(s.split()[s.split().index('+/-') +1])
                
            elif 'Estimated Jan 1951-Dec 1980 monthly absolute temperature (C):' in s:
                monthly_temp_line = hemisphere_data.index(line) + 2
                
            elif hemisphere_data.index(line) == monthly_temp_line:
                Jan_temp = float(s.split()[1])
                Feb_temp = float(s.split()[2])
                Mar_temp = float(s.split()[3])
                Apr_temp = float(s.split()[4])
                May_temp = float(s.split()[5])
                Jun_temp = float(s.split()[6])
                Jul_temp = float(s.split()[7])
                Aug_temp = float(s.split()[8])
                Sep_temp = float(s.split()[9])
                Oct_temp = float(s.split()[10])
                Nov_temp = float(s.split()[11])
                Dec_temp = float(s.split()[12])
                
            elif hemisphere_data.index(line) == (monthly_temp_line + 1):
                Jan_uncertainty = float(s.split()[2])
                Feb_uncertainty = float(s.split()[3])
                Mar_uncertainty = float(s.split()[4])
                Apr_uncertainty = float(s.split()[5])
                May_uncertainty = float(s.split()[6])
                Jun_uncertainty = float(s.split()[7])
                Jul_uncertainty = float(s.split()[8])
                Aug_uncertainty = float(s.split()[9])
                Sep_uncertainty = float(s.split()[10])
                Oct_uncertainty = float(s.split()[11])
                Nov_uncertainty = float(s.split()[12])
                Dec_uncertainty = float(s.split()[13])
                
        # compiles the entries for a new row
        d = [hemisphere,
             Baseline_temp,
             Baseline_temp_uncertainty,
             Jan_temp,
             Jan_uncertainty,
             Feb_temp,
             Feb_uncertainty,
             Mar_temp,
             Mar_uncertainty,
             Apr_temp,
             Apr_uncertainty,
             May_temp,
             May_uncertainty,
             Jun_temp,
             Jun_uncertainty,
             Jul_temp,
             Jul_uncertainty,
             Aug_temp,
             Aug_uncertainty,
             Sep_temp,
             Sep_uncertainty,
             Oct_temp,
             Oct_uncertainty,
             Nov_temp,
             Nov_uncertainty,
             Dec_temp,
             Dec_uncertainty]  
        
        # merges with existing data
        new_df = pd.DataFrame(data=[d], columns=col_names)
        df = pd.concat([df, new_df], ignore_index=True)
        
    # outputs the data frame to a csv  
    filename = '../data_files/metadata_hemispheres.csv'
    df = df.set_index('Hemisphere')
    df.to_csv(filename)
