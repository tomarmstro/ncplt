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


for file in glob.glob('GBROOS_CTD_NetCDF/HIS/*.nc'):
    print(file)
    data = Dataset(file, 'r')
    time = data.variables['TIME']
    temp = data.variables['TEMP']
    depth = data.variables['DEPTH']
    # sns.pairplot(depth, hue=['TIME'], height=2.5)
    
    ds = xr.open_dataset(file)
    df = ds.to_dataframe()
    
    
    # plt.plot(df['TEMP'])
    x = df['TEMP']
    y = df['PRES_REL']
    
    plt.figure(1)
    plt.plot(df['TEMP'], df['PRES_REL'])
    
    plt.figure(2)
    plt.plot(df['PSAL'], df['PRES_REL'])
    
    
    
    # g = sns.FacetGrid(df, col=df['TEMP'])
    # g.map(sns.kdeplot, "tip")
    
    