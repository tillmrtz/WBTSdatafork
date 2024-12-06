import numpy as np
import pandas as pd
import os
import xarray as xr
import datetime
from load_data.convert import process_dataset

column_names = ['z_depth', 'u_water_velocity_component', 'v_water_velocity_component', 'error_velocity']
units = ['meters', 'cm_per_s', 'cm_per_s', 'cm_per_s']

def load_vel_from_file(vel_dir):
    """Load all velocity data files (file.vel) from a directory.
    Returns a list with the velocity data as pandas DataFrames.
    """
    vel_files = [f for f in os.listdir(vel_dir) if f.endswith('.vel')]
    vel_list = []
    ### sort the files by the Cast number
    vel_files = sorted(vel_files, key=lambda x: int(x[7:9]))
    for vel_file in vel_files:
        vel_list.append(pd.read_csv(os.path.join(vel_dir, vel_file),names=column_names, skiprows=74, sep='\s+', encoding='utf-8'))
    return vel_list

def create_coordinates(vel_dir):
    ''' extract all the relevenat infromation from the file that is needed for the dataset.
        Returns a list with the information for each file.
    '''
    vel_files = [f for f in os.listdir(vel_dir) if f.endswith('.vel')]

    avg_coordinates = []
    start_coordinates = []
    end_coordinates = []
    for i in vel_files:
        with open(vel_dir +'/'+ i, 'rb') as file:
            file_content = file.read()
            long_Cast_number = file_content.splitlines()[21].decode('utf-8').split()[-1]
            if long_Cast_number[-1] == 'N' or long_Cast_number[-1] == 'S':
                Cast = int(long_Cast_number[-4:-1])
            else:
                Cast = int(long_Cast_number[-3:])

            Configuration = file_content.splitlines()[19].decode('utf-8').split()[-1]
            for i in [25,35,45]:
                lat = file_content.splitlines()[i].decode('utf-8').split()[-1]
                lon = file_content.splitlines()[i+1].decode('utf-8').split()[-1]
                date = file_content.splitlines()[i+2].decode('utf-8').split()[-1]
                time = file_content.splitlines()[i+3].decode('utf-8').split()[-1]
                date_time = datetime.datetime.strptime(date + time, '%m/%d/%y%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                if i == 25:
                    avg_values = [Cast,Configuration,date_time,lat,lon]
                elif i == 35:
                    start_values = [Cast,Configuration,date_time,lat,lon]
                else:
                    end_values = [Cast,Configuration,date_time,lat,lon]

        avg_coordinates.append(avg_values)
        start_coordinates.append(start_values)
        end_coordinates.append(end_values)
        ### sort the list by the Cast number
        avg_coordinates = sorted(avg_coordinates, key=lambda x: x[0])
        start_coordinates = sorted(start_coordinates, key=lambda x: x[0])
        end_coordinates = sorted(end_coordinates, key=lambda x: x[0])
    return avg_coordinates, start_coordinates, end_coordinates

def create_Dataset(vel_dir, config=None):
    """Create a xr.Dataset from the calibration data files in a directory.
    """
    if not isinstance(config, dict):
        config = tools.get_config()
    vel_list = load_vel_from_file(vel_dir)
    avg_coords, start_coords, end_coords = create_coordinates(vel_dir)
    coordinates = start_coords

    Cast = np.zeros(len(coordinates))
    Lat = np.zeros(len(coordinates))
    Lon = np.zeros(len(coordinates))
    
    nc_list = []
    for i in range(len(vel_list)):
        vel_list[i].insert(loc=0, column='DATETIME', value=np.full(len(vel_list[i]),datetime.datetime.strptime(coordinates[i][2], '%Y-%m-%d %H:%M:%S')))
        #nc_list.append(vel_list[i].to_xarray())
        nc_list.append(vel_list[i].set_index(['DATETIME','z_depth']).to_xarray())
        Cast[i] = coordinates[i][0]
        Lat[i] = coordinates[i][3]
        Lon[i] = coordinates[i][4]
    ds = xr.concat(nc_list, dim='DATETIME')
    ds.coords['latitude'] = ('DATETIME', Lat)
    ds.coords['longitude'] = ('DATETIME', Lon)
    ds = ds.assign({'CAST': ('DATETIME', Cast)})
    ### add units
    for i in range(len(column_names)):
        ds[column_names[i]].attrs['units'] = units[i]

    ### Add a string variable for each datetime which is the string 'GC_YYYY_MM' from the string cal_dir
    gc_string = [s for s in vel_dir.split('/') if s.startswith('GC')][0]
    gc_string = gc_string[:10]
    ds['gc_string'] = ('DATETIME', [gc_string] * len(ds['DATETIME']))
        
    ### add attributes and variable information
    ds,_ = process_dataset(ds, config)
    ### sort the dataset by longitude
    ds = ds.sortby('LONGITUDE')

    return ds

def create_complete_Dataset(directory_list):
    """Create a xr.Dataset from a list of directories containing velocity data files.
    """
    ds_list = []
    for vel_dir in directory_list:
        ds_list.append(create_Dataset(vel_dir))
    return xr.concat(ds_list, dim='DATETIME')
