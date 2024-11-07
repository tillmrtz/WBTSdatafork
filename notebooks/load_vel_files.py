import numpy as np
import pandas as pd
import os
import xarray as xr
import datetime

def load_vel_from_file(vel_dir):
    """Load all velocity data files (file.vel) from a directory.
    Returns a list with the velocity data as pandas DataFrames.
    """
    vel_files = [f for f in os.listdir(vel_dir) if f.endswith('.vel')]
    vel_list = []
    for vel_file in vel_files:
        column_names = ['z_depth', 'u_water_velocity_component', 'v_water_velocity_component', 'error_velocity']
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
            #Cast = int(file_content.splitlines()[21].decode('utf-8').split()[-1][-3:])
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
    return avg_coordinates, start_coordinates, end_coordinates

def create_Dataset(vel_dir):
    """Create a xr.Dataset from the calibration data files in a directory.
    """
    print(vel_dir)
    
    
    vel_list = load_vel_from_file(vel_dir)
    avg_coords, start_coords, end_coords = create_coordinates(vel_dir)
    coordinates = avg_coords
    nc_list = []
    for i in range(len(vel_list)):
        vel_list[i].insert(loc=0, column='Datetime', value=np.full(len(vel_list[i]),datetime.datetime.strptime(coordinates[i][2], '%Y-%m-%d %H:%M:%S')))
        nc_list.append(vel_list[i].set_index(['z_depth','Datetime']).to_xarray())
    ds = xr.concat(nc_list, dim='Datetime')

    Cast = np.zeros(len(coordinates))
    Lat = np.zeros(len(coordinates))
    Lon = np.zeros(len(coordinates))
    for i in range(len(coordinates)):   
        Cast[i] = coordinates[i][0]
        Lat[i] = coordinates[i][3]
        Lon[i] = coordinates[i][4]
    ds = ds.assign_coords({ 'Cast': ('Datetime', Cast), 'Lat': ('Datetime', Lat), 'Lon': ('Datetime', Lon)})
    ### sort the dataset by longitude
    ds = ds.sortby('Lon')
    return ds

def create_complete_Dataset(directory_list):
    """Create a xr.Dataset from a list of directories containing velocity data files.
    """
    ds_list = []
    for vel_dir in directory_list:
        ds_list.append(create_Dataset(vel_dir))
    return xr.concat(ds_list, dim='Datetime')
