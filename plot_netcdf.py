# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 14:55:55 2020

@author: thoma
"""
## Imports
from netCDF4 import Dataset
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import glob
import seaborn as sns
import numpy.ma as ma
import xarray as xr


#import CTD netcdf files

#split CTD netcdf files into 1st/2nd semesters

#plot all CTD netcdf files in a folder ontop of each other
#temp, sal, DO, turb, pres

#Import all files in folder
# for file in glob.glob('GBROOS_CTD_NetCDF/HIS/*.nc'):
#     print(file)
    
    # Set variables
    # data = Dataset(file, 'r')
    # time = data.variables['TIME']
    # temp = data.variables['TEMP']
    # depth = data.variables['DEPTH']
    # pressure = data.variables['PRES_REL']
    # conduct = data.variables['CNDC']
    # do = data.variables['DOX']
    # turb = data.variables['TURB']
    # chlorophyll = data.variables['CPHL']
    
    # data.variables.keys()
    # fig, axes = plt.subplots(1, 2, sharex=True, figsize=(10,5))
    # sns.lineplot(temp[:], depth[:])
    # sns.lineplot(ax=axes[1], conduct[:], depth[:])
    # a = ma.masked_equal(time[:])
    
    #Convert time to date from epoch
    # def serial_date_to_string(srl_no):
    #     new_date = datetime.datetime(1950,1,1,0,0) + datetime.timedelta(srl_no - 1)
    #     return new_date.strftime("%Y-%m-%d")
    # epoch_time = ma.getdata(time[:])
    # conv_time = serial_date_to_string(epoch_time)
    
    
    
## Create 
def serial_date_to_string(srl_no):
        new_date = datetime.datetime(1950,1,1,0,0) + datetime.timedelta(srl_no - 1)
        return new_date.strftime("%Y-%m-%d")    


def plot_netcdf(mooring):
    for file in glob.glob('GBROOS_CTD_NetCDF/' + mooring + '/*.nc'):
        #Used with netCDF data
        #variables
        data = Dataset(file, 'r')
        time = data.variables['TIME']
        temp = data.variables['TEMP']
        depth = data.variables['DEPTH']
        pressure = data.variables['PRES_REL']
        conduct = data.variables['CNDC']
        
        # print(data.variables.keys())
        
        #convert time
        epoch_time = ma.getdata(time[:])
        conv_time = serial_date_to_string(epoch_time)
        
        #plots
        sns.lineplot(temp[:], depth[:])
        sns.lineplot(conduct[:], depth[:])
        
        #converted to dataframe
        ds = xr.open_dataset(file)
        df = ds.to_dataframe()
        
        sns.relplot(x=df.TEMP, y=df.TEMP, hue=file, style="event",
        col=file, col_wrap=5,
        height=3, aspect=.75, linewidth=2.5,
        kind="line", data=df);
        

        
        
        

    
    
    




























# r'C:\Users\thoma\Python\netCDF\IMOS_ANMN-NRS_CSTZ_20080917T000001Z_NRSYON_FV01_NRSYON-0809-SBE37-SM-6.5_END-20081125T060002Z_C-20180913T020043Z.nc'














# yon0809_path = r'C:\Users\thoma\Python\netCDF\NRSYON_0809.nc'
# yon1006_path = r'C:\Users\thoma\Python\netCDF\NRSYON_1006.nc'

# yon0809 = Dataset(yon0809_path)
# yon1006 = Dataset(yon1006_path)


# plt.plot(yon0809['TIME'], yon0809['TEMP'])
# plt.plot(yon1006['TIME'], yon1006['TEMP'])

# plt.show()


##Convert time since EPOCH to Date

# for file in glob.glob('*.nc'):
# print(file)
    # data = Dataset(file, 'r')
    # time = data.variables['TIME'][:]
    # temperature = data.variables['TEMP']
    # temps = data.variables['TEMP'][:]
    # list1 = []
    # list1.append(temps)
    # plt.plot(list1, time)
    # plt.show()
    # df = pd.DataFrame(0.0, columns = (time, temperature), index = temperature)
    # df = pd.DataFrame(temps)
    # ts = np.ma.masked_array(data = time, mask = False, fill_value=1e+20)
    # df['0'] = time
    # def serial_date_to_string(time):
    #     new_date = datetime.datetime(1950,1,1,0,0) + datetime.timedelta(time - 1)
    #     return new_date.strftime("%Y-%m-%d")
    
    
    

    
    
    # pd.DataFrame.apply(serial_date_to_string(ts))
    
    
# temps = data.variables['TEMP'][:]
# df = pd.DataFrame(0.0, columns = (float(temps), float(time)), index = temperature)

# list1 = []
# list1.append(temps)

# plt.plot(temps, time)
# dt = datetime.datetime.fromtimestamp(21444.000012)

