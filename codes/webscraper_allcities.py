# -*- coding: utf-8 -*-
"""
A simple script from downloading data from the "Time Series" section of
the Berkeley Earth database (berkeleyearth.org/data/).  This grabs the data
for "large" cities.

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
# Part A: This part compiles the list of largest cities available
# ------------------

column_names = ['city',
                'country',
                'temp',
                'warming_since_1960',
                'uncertainty',
                'location']
cities_df = pd.DataFrame(columns = column_names)
cities_df = cities_df.set_index('city')
largest_cities = []

# access each city page one by one
for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    
    # url is only used to gather the latitude and longtitude
    url = "http://berkeleyearth.lbl.gov/city-list/" + letter
    with urllib.request.urlopen(url) as letter_page:
        letter_source = letter_page.readlines()
        
    # use read_html to get the dataframe containing largest cities of an alphabet
    # read_html seems to use default encoding not based on 'utf-8'.  Is it system encoding?
    df = pd.read_html(url, encoding='utf-8')[0]
    df.columns = column_names[0:3]
    
    # removes the first two rows which should be useless info
    df = df.iloc[2:, :].reset_index(drop = True)
    
    # generates the actual 'warming_since_1960' and 'uncertainty', columns
    df[['warming_since_1960', 'uncertainty']] = df.temp.str \
                                                       .split(' ± ', expand = True) \
                                                       .astype("float")
    
    last_city, last_gps = "", ""    
    largest_cities_temp = []                    
    # to fill in the locations which is used for 
    # accessing the actual text file for each city                                                       
    for line in letter_source:
        try:
            s = codecs.decode(line, 'UTF-8')
        except:
            s = codecs.decode(line, 'iso-8859-1')
        # find the line that contain major city names and their respective countries
        # this should be line 5755 if nothing changes
        if not s.startswith('<tr><td><a href='):
            continue
        else:
            s = s.split('href=')[1:]
            # the structure seems to be that one line is used to contain all largest cities 
            # and their countries.  So there should be [len(df) * 2] entries in it.
            try:
                assert len(s) == len(df) * 2
            except AssertionError:
                print("The file structure seems to have been changed.  Please check.")
                break
            # start gathering the city names and country names.  The entries should
            # go like: city -> country -> city -> country...
            for i in range(len(df) * 2):
                # city rows are even numbered
                if i % 2 == 0:
                    # each even row should have a form of:
                    # '"http://berkeleyearth.lbl.gov/locations/29.74N-31.38E">Cairo</td><td><a '
                    last_city = s[i].split('>')[1][:-4]
                    last_gps = s[i].split('>')[0].strip('"').split('/')[-1]
                    # each even row should have a form of:
                        # '"http://berkeleyearth.lbl.gov/regions/Japan">Japan</td><td>1.63 &plusmn; 0.29</td></tr><tr><td><a '
                    largest_cities.append((last_city, last_gps))
                    largest_cities_temp.append((last_city, last_gps))
                    
    # join the location columns with the other data
    df2 = pd.DataFrame([largest_cities_temp]).T
    df2 = pd.DataFrame(df2[0].tolist())
    df2.columns = ['city', 'location']
    df.city = df2.city
    df['location'] = df2.location
    df = df.set_index('city')
    # join with the main table
    cities_df = pd.concat([cities_df, df])

cities_df = cities_df.reset_index()

# checks for and handles duplicated names by adding 1, 2, 3, etc. to the end.
duplicated_cities = list(cities_df.city.value_counts()[cities_df.city.value_counts() > 1].index)
for city in duplicated_cities:
    duplicated_rows = list(cities_df[cities_df.city == city].index)
    count = 1
    for row_num in duplicated_rows:
        cities_df.iat[row_num, 0] = city + str(count)
        largest_cities[row_num] = (city + str(count), largest_cities[row_num][1])
        count += 1

cities_df.to_csv('../data_files/largest_city_list.csv')
    
# ------------------
# Part B: This part saves the text files to the local drive and also prepares a csv.
# ------------------

# Note: for the main city page (i.e. the one with graphs), utf-8 should be used
# for the text file, use iso-8859-1
def generate_city_csv():
    '''
    requires the list of cities generated from Part A1 above.
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
    
    for i in range(len(largest_cities)):
        city = largest_cities[i][0]
        city_url = ('http://berkeleyearth.lbl.gov/auto/Local/TAVG/Text/'
                    + largest_cities[i][1]
                    + '-TAVG-Trend.txt')
        # open the url
        with urllib.request.urlopen(city_url) as city_file:
            city_data = city_file.readlines()    
   
        df = pd.DataFrame(data=None, columns=col_names)

        for line in city_data:
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

        filename = '../data_files/' + city + '.csv'

        df = df.set_index('Year')
        df.to_csv(filename)

# ------------------
# Part C: This part saves the other data found in the text files into a csv.
# ------------------
    
def generate_metadata_csv():
    '''
    requires the list of cities generated from Part A1 above.
    '''
    monthly_temp_line = -9999
    
    col_names = ['City', 
                  'Latitude',
                  'Longitude',
                  'Neighborhood_water_percent',
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
    
    for i in range(len(largest_cities)):
        city = largest_cities[i][0]
        
        print(f'Handling {city}...')     
        
        # the latitude and longitude are available from the dictionary, though in
        # a different form then the country location data
        Latitude = float(largest_cities[i][1].split('-')[0][:-1])
        if largest_cities[i][1].split('-')[0][-1] == 'S':
            Latitude = -Latitude
            
        Longitude = float(largest_cities[i][1].split('-')[1][:-1])
        if largest_cities[i][1].split('-')[1][-1] == 'W':
            Longitude = -Longitude
            
        # creates and then open the url for the other data    
        city_url = ('http://berkeleyearth.lbl.gov/auto/Local/TAVG/Text/'
                    + largest_cities[i][1]
                    + '-TAVG-Trend.txt')

        with urllib.request.urlopen(city_url) as city_file:
            city_data = city_file.readlines()    
        
        for line in city_data:
            try:
                s = line.decode('iso-8859-1')[:-1]
            except:
                print(line)
                return 0
            # extracts meta data one by one starting from the water percentage.                
            if 'Percent water in local neighborhood:' in s:
                Neighborhood_water_percent = float(s.split()[s.split().index('neighborhood:') + 1]) / 100
            
            elif 'Estimated Jan 1951-Dec 1980 absolute temperature (C):' in s:
                Baseline_temp = float(s.split()[s.split().index('(C):') +1])
                Baseline_temp_uncertainty = float(s.split()[s.split().index('+/-') +1])
                
            elif 'Estimated Jan 1951-Dec 1980 monthly absolute temperature (C):' in s:
                monthly_temp_line = city_data.index(line) + 2
                
            elif city_data.index(line) == monthly_temp_line:
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
                
            elif city_data.index(line) == (monthly_temp_line + 1):
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
        d = [city,
              Latitude,
              Longitude,
              Neighborhood_water_percent,
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
    filename = '../data_files/metadata_largest_city.csv'
    df = df.set_index('City')
    df.to_csv(filename)
