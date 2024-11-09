import numpy as np
import pandas as pd
import os
import xarray as xr
import datetime
from load_data import missing_datetime_2005_05 as mdt

def load_cal_from_file(cal_dir):
    """Load all calibration data files (file.cal) from a directory.
    Returns a list with the calibration data as pandas DataFrames.
    """
    cal_files = [f for f in os.listdir(cal_dir) if f.endswith('.cal')]
    cal_list = []
    ### sort the files by the Cast number
    cal_files = sorted(cal_files, key=lambda x: int(x[6:8]))
    for cal_file in cal_files:
        column_names = ['PRES', 'TEMPERATURE', 'Pot. Temp', 'PSAL', 'Dyn. Height', 'ga', 'Dis. Oxygen']
        cal_list.append(pd.read_csv(os.path.join(cal_dir, cal_file), names=column_names, skiprows=12, sep='\s+'))
    return cal_list

def create_coordinates(cal_dir):
    '''create a list with all infromation in the first line and second line
        but for the second line take the fifth element as the date in the fromat xx/xx/xx
    '''
    cal_files = [f for f in os.listdir(cal_dir) if f.endswith('.cal')]
    coordinates = []
    for i in cal_files:
        with open(cal_dir +'/'+ i, 'r') as file:
            fl = file.readline().split()
            sl = file.readline().split()
            ### bring date into the right shape and add it to the list. 
            if len(sl) == 7:
                if len(sl[5]) < 2:
                    sl[5] = '0'+sl[5]
                if len(sl[4]) < 2:
                    sl[4] = '0'+sl[4]
                sl[4] = sl[4] +sl[5]
                sl.pop(5)
            if len(sl) == 8:
                if len(sl[4]) < 2:
                    sl[4] = '0'+sl[4]
                if len(sl[5]) < 2:
                    sl[5] = '0'+sl[5]
                if len(sl[6]) < 2:
                    sl[6] = '0'+sl[6]
                sl[4] = sl[4] +sl[5] +sl[6]
                sl.pop(5)
                sl.pop(5)

            ### change the format of the gmt data
            year = i[2:6]
            if 505 == int(year):
                dates = mdt.dates()
                times = mdt.times()
                sl[2] = sl[2].replace('-735234','')
                sl[3] = '0'
                sl[4] = dates[int(i[7:9])]
                sl[5] = times[int(i[7:9])]
            if 703 < int(year) < 1705:
                if len(sl[5]) == 3:
                    if int(sl[5][-2:]) > 59:
                        sl[5] = sl[5][:2] + '0' + sl[5][2]
                elif len(sl[5]) == 2:
                    if int(sl[5][-2:]) > 59:
                        sl[5] = sl[5][0] + '0' + sl[5][1] 
            for i in range(3):
                if len(sl[5]) < 4:
                    sl[5] = '0'+sl[5]

            ### create a datetime object from the date and time
            #print(sl[4]+sl[5])
            Datetime = datetime.datetime.strptime(sl[4]+sl[5], '%m/%d/%y%H%M').strftime('%Y-%m-%d %H:%M:%S')
            sl[4] = Datetime
            sl[0] = int(sl[0])
            ### pop the unnecessary elements
            sl.pop(5)
            sl.pop(3)
            coordinates.append(sl)
            ### sort coordinates by the Cast number
            coordinates = sorted(coordinates, key=lambda x: x[0])
    return coordinates

def create_Dataset(cal_dir):
    """Create a xr.Dataset from the calibration data files in a directory.
    """
    cal_list = load_cal_from_file(cal_dir)
    coordinates = create_coordinates(cal_dir)

    nc_list = []
    Cast = np.zeros(len(coordinates))
    Lat = np.zeros(len(coordinates))
    Lon = np.zeros(len(coordinates))
    for i in range(len(cal_list)):
        cal_list[i].insert(loc=0, column='DATETIME', value=np.full(len(cal_list[i]),datetime.datetime.strptime(coordinates[i][3], '%Y-%m-%d %H:%M:%S')))
        nc_list.append(cal_list[i].set_index(['DATETIME','PRES']).to_xarray())
        Cast[i] = coordinates[i][0]
        Lat[i] = coordinates[i][1]
        Lon[i] = coordinates[i][2]
    ds = xr.concat(nc_list, dim='DATETIME')
    ### assign Longitude, Latitude as coordinates and the Cast number as a variable
    ds.coords['LATITUDE'] = ('DATETIME', Lat)
    ds.coords['LONGITUDE'] = ('DATETIME', Lon)
    ds = ds.assign({'CAST': ('DATETIME', Cast)})
    ### sort the dataset by longitude
    ds = ds.sortby('LONGITUDE')
    return ds



def create_complete_Dataset(directory_list):
    """Create a xr.Dataset from the calibration data files in a list of directories.
    """
    ds_list = []
    for directory in directory_list:
        ds_list.append(create_Dataset(directory))
    ds = xr.concat(ds_list, dim='DATETIME')
    return ds
