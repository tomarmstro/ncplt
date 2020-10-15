# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 16:27:27 2020

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

#Set up plots
fig1, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3)
fig1.suptitle('Jan-June CTD Casts', fontsize=16)
fig1.subplots_adjust(hspace=0.5, wspace=0.5)
ax1.invert_yaxis()
ax1.set_title("Temperature")
ax2.invert_yaxis()
ax2.set_title("Salinity")
ax3.invert_yaxis()
ax3.set_title("DO")
ax4.invert_yaxis()
ax4.set_title("PAR")
ax5.invert_yaxis()
ax5.set_title("Chlorophyll")
ax6.invert_yaxis()
ax6.set_title("Turbidity")
ax6.set_xlim([-5, 5])
ax6.set_ylim([0, 5])

fig2, ((ax7, ax8, ax9), (ax10, ax11, ax12)) = plt.subplots(2, 3)
fig2.suptitle('July-Dec CTD Casts', fontsize=16)
fig2.subplots_adjust(hspace=0.5, wspace=0.5)
ax7.invert_yaxis()
ax7.set_title("Temperature")
ax8.invert_yaxis()
ax8.set_title("Salinity")
ax9.invert_yaxis()
ax9.set_title("DO")
ax10.invert_yaxis()
ax10.set_title("PAR")
ax11.invert_yaxis()
ax11.set_title("Chlorophyll")
ax12.invert_yaxis()
ax12.set_title("Turbidity")

#Looping through files

# def ncplt(mooring):
#     for file in glob.glob('GBROOS_CTD_NetCDF/' + mooring + '/*.nc'):
    
for file in glob.glob('GBROOS_CTD_NetCDF/HIS/*.nc'):
    
    ds = xr.open_dataset(file)
    df = ds.to_dataframe()
    
    # plt.plot(df['TEMP'])
    temp = df['TEMP']
    pres = df['PRES_REL']
    time = df['TIME']
    sal = df['PSAL']
    # dep = df['DEPTH']
    # sal = df['CPHL']
    # turb = df['TURB']
    # pars = df['PAR']
    # do = df['DOX']
    
    
    #Adding variables to plots depending on month of the year
    if int((str(time)[23:25])) <= 6:
        ax1.plot(temp, pres)
        ax2.plot(sal, pres)
        ax3.plot(df['DOX'], df.index)
        ax4.plot(df['PAR'], pres)
        ax5.plot(df['CPHL'], pres)
        # ax6.plot(df['TURB'], pres)
        # print("sem1")
    if int((str(time)[23:25])) > 6:
        ax7.plot(temp, df.index)
        ax8.plot(sal, pres)
        ax9.plot(df['DOX'], df.index)
        ax10.plot(df['PAR'], pres)
        ax11.plot(df['CPHL'], pres)
        # ax12.plot(df['TURB'])
        # print("sem2")
    
          

    
    