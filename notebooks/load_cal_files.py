import numpy as np
import pandas as pd
import os
import xarray as xr

def load_cal_from_file(cal_dir):
    """Load all calibration data files (file.cal) from a directory.
    Returns a list with the calibration data as pandas DataFrames.
    """
    cal_files = [f for f in os.listdir(cal_dir) if f.endswith('.cal')]
    cal_list = []
    for cal_file in cal_files:
        column_names = ['PRES', 'TEMP', 'POT. TEMP', 'PSAL', 'DYN. HT', 'ga', 'DIS. OX']
        cal_list.append(pd.read_csv(os.path.join(cal_dir, cal_file), names=column_names, skiprows=12, sep='\s+'))
    return cal_list

def create_nc_file(cal_list):
    """Create a netCDF file with the calibration data.
    """
    nc_list = []
    for i in range(len(cal_list)):
        nc_list.append(cal_list[i].to_xarray())
    return nc_list

        #pd.to_datetime(df1[['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']])

def create_coordinates(cal_dir):
    ### create a list with all infromation in the first line and second line
    ### but for the second line take the fifth element as the date in the fromat xx/xx/xx
    cal_files = [f for f in os.listdir(cal_dir) if f.endswith('.cal')]
    for i in cal_files:
        with open('/Users/tillmoritz/Desktop/Work/WBTSData/GC_2001_04/CTD/ab0104031_aoml.cal', 'r') as file:
            first_line = file.readline().split()
            second_line = file.readline().split()
            ### date is sometimes split into two/three elemnts
            if len(second_line) == 7:
                second_line[4] = second_line[4] + second_line[5]
                second_line.pop(5)
            if len(second_line) == 8:
                second_line[4] = second_line[4] + second_line[5] + second_line[6]
                second_line.pop(5)
                second_line.pop(5)
            #second_line_date = second_line[4]
    return first_line, second_line
    