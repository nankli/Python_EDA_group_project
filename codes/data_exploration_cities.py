# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 22:05:33 2021

@author: user
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

city_list = pd.read_csv('../data_files/largest_city_list.csv')
metadata = pd.read_csv('../data_files/metadata_largest_city.csv', index_col = 'City')


def retrieve_city_data():
    '''
    Reads in all city based csv files.  Run at start of session by default.
    '''
    city_data = {}
    
    for city in city_list.city:
        filename = city + '.csv'
        city_data.update({city: pd.read_csv(filename)})
    
    return city_data


# def col_data_by_year_and_month(Year, Month, ColName ='Ten_year_Anomaly'):
#     '''
#     Extracts the temperature value (or other column values) of a city at the
#     specified year and month, and compiles the result answer into a data frame
#     for further use.
#     '''   
#     temp_list = []
    
#     for city in metadata.index:
#         df = city_data[city]
#         value = df.loc[(df['Year'] == Year) & (df['Month'] == Month)].loc[:,ColName].iat[0]
#         temp_list.append(value)
    
#     ans = metadata
#     ans[ColName] = temp_list
    
#     return ans

# if __name__ == '__main__':
#     city_data = retrieve_city_data()

# ---------------
# Exploration on Latitude and Longitude
# ---------------

# ---- Using warming since 1960 figures ----
base_data = metadata.copy()
base_data['warming_since_1960'] = city_list.set_index('city').warming_since_1960
northhem_data = base_data[base_data.Latitude > 0]
southhem_data = base_data[base_data.Latitude < 0]
southhem_data['Latitude'] = abs(southhem_data.Latitude)

fig = plt.figure(figsize=(9,5))
ax = fig.add_subplot(1,1,1)

ax.scatter(northhem_data.Latitude, northhem_data.warming_since_1960, c="#3D59AB", marker="^", label="Northern Hemisphere Cities")
ax.scatter(southhem_data.Latitude, southhem_data.warming_since_1960, c="#CD9B9B", marker="v", label="Southern Hemisphere Cities")

## For base trend line
z = np.polyfit(northhem_data.Latitude, northhem_data.warming_since_1960, 1)
p = np.poly1d(z)
ax.plot(northhem_data.Latitude, p(northhem_data.Latitude), 
        c="#698B69", linewidth=0.5, label="Trend Line for Northern Hemisphere",
        linestyle = (0,(4,1)))

# # For modified trend line
modified_northern = northhem_data[northhem_data.Latitude >= 20]
z = np.polyfit(modified_northern.Latitude, modified_northern.warming_since_1960, 1)
p = np.poly1d(z)
ax.plot(modified_northern.Latitude, p(modified_northern.Latitude), 
        c="#698B69", linewidth=0.5, label="Trend Line for Cities at 20N or above",
        linestyle = (0,(4,1)))

ax.set_xlabel("Absolute latitude (Degrees)")
ax.set_ylabel("Temperature rise (10-year-avg)")
ax.set_title("Do All Places Heat Up Evenly:\nTemperature Rise versus Latitude ")
ax.legend(loc=0)


# ---- Using ten year anomaly figures ----
# base_data = col_data_by_year_and_month(2015, 6)
# northhem_data = base_data[base_data.Latitude > 0]
# southhem_data = base_data[base_data.Latitude < 0]
# southhem_data['Latitude'] = abs(southhem_data.Latitude)

# fig = plt.figure(figsize=(9,5))
# ax = fig.add_subplot(1,1,1)

# ax.scatter(northhem_data.Latitude, northhem_data.Ten_year_Anomaly, c="#3D59AB", marker="^", label="Northern Hemisphere Cities")
# ax.scatter(southhem_data.Latitude, southhem_data.Ten_year_Anomaly, c="#CD9B9B", marker="v", label="Southern Hemisphere Cities")

# ## For base trend line
# z = np.polyfit(northhem_data.Latitude, northhem_data.Ten_year_Anomaly, 1)
# p = np.poly1d(z)
# ax.plot(northhem_data.Latitude, p(northhem_data.Latitude), 
#         c="#698B69", linewidth=0.5, label="Trend Line for Northern Hemisphere",
#         linestyle = (0,(4,1)))

# # # For modified trend line
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

