# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 22:05:33 2021

@author: user
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

city_list = pd.read_csv('../data_files/major_city_list.csv')
metadata = pd.read_csv('../data_files/metadata_city.csv', index_col = 'City')


def retrieve_city_data():
    '''
    Reads in all city based csv files.  Run at start of session by default.
    '''
    city_data = {}
    
    for city in city_list.City:
        filename = '../data_files/' + city + '.csv'
        city_data.update({city: pd.read_csv(filename)})
    
    return city_data


def col_data_by_year_and_month(Year, Month, ColName ='Ten_year_Anomaly'):
    '''
    Extracts the temperature value (or other column values) of a city at the
    specified year and month, and compiles the result answer into a data frame
    for further use.
    '''   
    temp_list = []
    
    for city in metadata.index:
        df = city_data[city]
        value = df.loc[(df['Year'] == Year) & (df['Month'] == Month)].loc[:,ColName].iat[0]
        temp_list.append(value)
    
    ans = metadata
    ans[ColName] = temp_list
    
    return ans

if __name__ == '__main__':
    city_data = retrieve_city_data()

# ---------------
# Exploration on Latitude and Longitude
# ---------------

# ---- Preliminary Plots Covering All Months of the Year ----
# fig, ax = plt.subplots(4, 3, figsize = (5,5))
# fig.subplots_adjust(hspace=.4)

# for month in range(1,13):
#     row = month//3 - 1
#     col = (month - 1) % 3 
      
#     base_data = col_data_by_year_and_month(2015, month)
#     northhem_data = base_data[base_data.Latitude > 0]
#     southhem_data = base_data[base_data.Latitude < 0]
#     southhem_data['Latitude'] = abs(southhem_data.Latitude)
    
#     ax[row,col].scatter(northhem_data.Latitude, northhem_data.Ten_year_Anomaly, c="#3D59AB", marker="^")
#     ax[row,col].scatter(southhem_data.Latitude, southhem_data.Ten_year_Anomaly, c="#CD9B9B", marker="v")

# ---- Chose Jun as the month ----
base_data = col_data_by_year_and_month(2015, 6)
northhem_data = base_data[base_data.Latitude > 0]
southhem_data = base_data[base_data.Latitude < 0]
southhem_data['Latitude'] = abs(southhem_data.Latitude)

# fig = plt.figure(figsize=(9,5))
# ax = fig.add_subplot(1,1,1)

# ax.scatter(northhem_data.Latitude, northhem_data.Ten_year_Anomaly, c="#3D59AB", marker="^", label="Northern Hemisphere Cities")
# ax.scatter(southhem_data.Latitude, southhem_data.Ten_year_Anomaly, c="#CD9B9B", marker="v", label="Southern Hemisphere Cities")

## For base trend line
# z = np.polyfit(northhem_data.Latitude, northhem_data.Ten_year_Anomaly, 1)
# p = np.poly1d(z)
# ax.plot(northhem_data.Latitude, p(northhem_data.Latitude), 
#         c="#698B69", linewidth=0.5, label="Trend Line for Northern Hemisphere",
#         linestyle = (0,(4,1)))

# # For modified trend line
# modified_northern = northhem_data[northhem_data.Latitude >= 20]
# z = np.polyfit(modified_northern.Latitude, modified_northern.Ten_year_Anomaly, 1)
# p = np.poly1d(z)
# ax.plot(modified_northern.Latitude, p(modified_northern.Latitude), 
#         c="#698B69", linewidth=0.5, label="Trend Line for Cities at 20N or above",
#         linestyle = (0,(4,1)))

# ax.set_xlabel("Absolute latitude (Degrees)")
# ax.set_ylabel("Temperature rise (10-year-avg)")
# ax.set_title("Do All Places Heat Up Evenly:\nTemperature Rise versus Latitude ")
# ax.legend(loc=0)

# ---------------
# Question: Do Temperatures Tend to Converge after Warming?  If so, by how much?
# ---------------

# temp_after_heating = base_data.Baseline_temp + base_data.Ten_year_Anomaly
# modified_basedata = base_data.copy()
# modified_basedata['Temp_after_heating'] = (modified_basedata.Baseline_temp 
#                                            + modified_basedata.Ten_year_Anomaly)

# fig = plt.figure(figsize=(9,5))
# ax = fig.add_subplot(1,1,1)

# ax.scatter(modified_basedata.Baseline_temp, modified_basedata.Temp_after_heating, c="#DC143C", marker="d", label="All Major Cities")

# ax.set_xlabel("Baseline Temperature before Heating")
# ax.set_ylabel("Temperature after Heating")
# ax.set_title("Do Temperatures Tend to Converge after Warming?:\nTemperature after Warming versus Original Temperature ")
# ax.legend(loc=0)

# ---------------
# Exploration on Effect of Water
# ---------------

# fig = plt.figure(figsize=(9,5))
# ax = fig.add_subplot(1,1,1)

# water = base_data.copy()
# water['WaterContent'] = water.Neighborhood_water_percent * 100

# ax.scatter(water.WaterContent, water.Ten_year_Anomaly, c="#00008B", marker=".", label="% of Water in Neighbohood")

# ax.set_xlabel("Percentage of Water Near City")
# ax.set_xlim(-5, 105)
# ax.set_ylabel("Temperature rise (10-year-avg)")
# ax.set_title("Presence of Water Doesn't Seem to Alleviate Heating:\nTemperature Rise versus Percentage of Water Near City")
# ax.legend(loc=0)

# ---------------
# Exploration on Average Warming During Different Months
# ---------------
'''
This part uses global data for initial exploration
'''
# My own file structure is like this:
    # Data
    # |_ MajorCities folder containing city CSVs and the webscraper
    # |_ Countru folder containing country CSVs and the webscraper
    # |_ GlobalTemp.csv
    # |_ the original webscraper for global data
    
global_data = pd.read_csv('..\\GlobalTemp.csv')

monthly_temp = {'Jan':[],
                'Feb':[],
                'Mar':[],
                'Apr':[],
                'May':[],
                'Jun':[],
                'Jul':[],
                'Aug':[],
                'Sep':[],
                'Oct':[],
                'Nov':[],
                'Dec':[]}

fig = plt.figure(figsize=(9,5))
ax = fig.add_subplot(1,1,1)

'''
Using five-year averages
'''
# for i in [1,6]:
#     pre_avg_data = global_data[(global_data.Year >= 1898) 
#                                 & (global_data.Month == i)]
#     month = list(monthly_temp.keys())[i - 1]
#     monthly_temp[month].append(pre_avg_data)
    
#     # Computing five-year averages:
#     five_year_avg = {}
#     for row in range(2, (len(pre_avg_data) - 2)):
#         year = pre_avg_data.iloc[row, 0]
#         avg_temp = (pre_avg_data.iloc[row - 2, 2]
#                     + pre_avg_data.iloc[row - 1, 2]
#                     + pre_avg_data.iloc[row, 2]
#                     + pre_avg_data.iloc[row + 1, 2]
#                     + pre_avg_data.iloc[row + 2, 2]) / 5
#         five_year_avg.update({year: [avg_temp]})
#     avg_data = pd.DataFrame(data=five_year_avg).T 
#     monthly_temp[month].append(avg_data)  
    
#     ax.plot(avg_data, label=f"{month} data")
    
# ax.legend(loc=0)    
     
'''
Using ten-year averages
''' 
# month_colors = {'Dec': "#97FFFF",
#                 'Jan': "#79CDCD",
#                 'Jun': "#EEC900",
#                 'Jul': "#DAA520",
#                 'Aug': "#EEB422"}

# for i in [12, 1, 6, 7]:
#     pre_avg_data = global_data[(global_data.Year >= 1896) 
#                                 & (global_data.Month == i)]
#     month = list(monthly_temp.keys())[i - 1]
#     monthly_temp[month].append(pre_avg_data)
    
#     # Computing ten-year averages:
#     ten_year_avg = {}
#     for row in range(4, (len(pre_avg_data) - 5)):
#         year = pre_avg_data.iloc[row, 0]
        
#         avg_temp = 0
#         for j in range(-4, 6):
#             avg_temp += pre_avg_data.iloc[row + j, 2]
#         avg_temp /= 10
        
#         ten_year_avg.update({year: [avg_temp]})
        
#     avg_data = pd.DataFrame(data=ten_year_avg).T 
#     monthly_temp[month].append(avg_data)  
    
#     ax.plot(avg_data, c=month_colors[month], label=f" {month} data only")
#     ax.set_title("Do Winter Months Heat Up More:\nGlobal Temperature Change from 1900 to 2016")
    
#     ax.set_xlabel("Year")
#     ax.set_xlim(1900, 2020)
#     ax.set_ylabel("10-year Moving Average of Temperature (C)")
    
# ax.legend(loc=0)        

'''
Attempt at using seasons
''' 

seasonal_temp = {'Spring':[],
                 'Summer':[],
                 'Fall':[],
                 'Winter':[]}

season_colors = {'Spring': "#006400",
                 'Summer': "#8B1A1A",
                 'Fall': "#EEB422",
                 'Winter': "#009ACD"}

seasonal_data = global_data.copy()
seasonal_data['Season'] = 'Spring'
seasonal_data.loc[(seasonal_data.Month == 12) | (seasonal_data.Month <= 2), 'Season'] = 'Winter'
seasonal_data.loc[(seasonal_data.Month >= 6) & (seasonal_data.Month <= 8), 'Season'] = 'Summer'
seasonal_data.loc[(seasonal_data.Month >= 9) & (seasonal_data.Month <= 11), 'Season'] = 'Fall'

# for season in ['Summer', 'Winter']:
for season in ['Spring', 'Summer', 'Fall', 'Winter']:
    pre_avg_data = seasonal_data[(seasonal_data.Year >= 1896) 
                                 & (seasonal_data.Season == season)]

    seasonal_temp[season].append(pre_avg_data)
    
    # Computing five-year averages:
    ten_year_avg = {}
    for row in range(4, (len(pre_avg_data) - 5)):
        year = pre_avg_data.iloc[row, 0]
        
        avg_temp = 0
        for j in range(-4, 6):
            avg_temp += pre_avg_data.iloc[row + j, 2]
        avg_temp /= 10
        
        ten_year_avg.update({year: [avg_temp]})
        
    avg_data = pd.DataFrame(data=ten_year_avg).T 
    seasonal_temp[season].append(avg_data)  
    
    ax.plot(avg_data, c=season_colors[season], label=f" {season} months only")
    ax.set_title("Do Winter Months Heat Up More:\nGlobal Temperature Change from 1900 to 2016")
    
    ax.set_xlabel("Year")
    ax.set_xlim(1900, 2020)
    ax.set_ylabel("10-year Moving Average of Temperature (C)")
    
ax.legend(loc=0)   
    