import numpy as np
import pandas as pd
import os
import xarray as xr
import datetime
from load_data import load_vel_files, load_cal_files

def create_coordinates_with_ADCPtimes(cal_dir, dir_list_ADCP):
    '''create the coordinates for the calibration data with the time from the ADCP data.'''
    year = cal_dir[-11:-4]
    for j in dir_list_ADCP:
        if year in j:
            _,coords_ADCP,_ = load_vel_files.create_coordinates(j)
            coords_CTD = load_cal_files.create_coordinates(cal_dir)
            for coords_i in coords_ADCP:
                Cast = coords_i[0] 
                for coords_j in coords_CTD:
                    if Cast == coords_j[0]:
                        coords_j[3] = coords_i[2]
                        break
                    else:
                        continue
            coordinates = coords_CTD
    return coordinates

def create_CTD_Dataset_with_ADCPtimes(cal_dir,dir_list_ADCP):
    """Create a xr.Dataset from the calibration data files in a directory.
    """
    cal_list = load_cal_files.load_cal_from_file(cal_dir)
    coordinates = create_coordinates_with_ADCPtimes(cal_dir, dir_list_ADCP)

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

def merge_datasets(cal_dir, vel_dir, dir_list_ADCP):
    """Merge velocity and calibration data into a single xarray dataset.
    """
    ds_CTD = create_CTD_Dataset_with_ADCPtimes(cal_dir, dir_list_ADCP)
    ds_ADCP = load_vel_files.create_Dataset(vel_dir)
    ## change coordinates name of PRES to DEPTH for ADCP data
    ds_CTD = ds_CTD.rename({'PRES': 'DEPTH'})
    ## merge the two datasets
    ds_merge = xr.merge([ds_CTD, ds_ADCP], compat='override')
    return ds_merge
    
