import numpy as np
import xarray as xr
from load_data import vocabularies
from load_data import attr_input
import gsw
import logging
from datetime import datetime
import yaml
import time

_log = logging.getLogger(__name__)

def rename_dimensions(ds, rename_dict=vocabularies.dims_rename_dict):
    """
    Renames dimensions in the dataset based on the provided dictionary for OG1.

    Parameters
    ----------
    ds (xarray.Dataset): The input dataset containing dimensions to be renamed.
    rename_dict (dict): A dictionary where keys are the old dimension names and values are the new dimension names.

    Returns
    -------
    xarray.Dataset: The dataset with renamed dimensions.
    """
    for old_name, new_name in rename_dict.items():
        if old_name in ds.dims:
            ds = ds.rename({old_name: new_name})
    return ds

def rename_variables(ds, rename_dict=vocabularies.standard_names):
    """
    Renames variables in the dataset based on the provided dictionary for OG1.

    Parameters
    ----------
    ds (xarray.Dataset): The input dataset containing variables to be renamed.
    rename_dict (dict): A dictionary where keys are the old variable names and values are the new variable names.

    Returns
    -------
    xarray.Dataset: The dataset with renamed variables.
    """
    for old_name, new_name in rename_dict.items():
        suffixes = ['', '_qc', '_raw', '_raw_qc']
        variants = [old_name + suffix for suffix in suffixes]
        variants_new = [new_name + suffix.upper() for suffix in suffixes]
        for variant in variants:
            new_name1 = variants_new[variants.index(variant)]
            if new_name1 in ds.variables:
                print(f"Warning: Variable '{new_name1}' already exists in the dataset.")
            elif variant in ds.variables:
                ds = ds.rename({variant: new_name1})
            elif variant in ds.variables:
                ds = ds.rename({variant: new_name1})
    return ds


def assign_variable_attributes(ds, vocab_attrs=vocabularies.vocab_attrs, unit_format=vocabularies.unit_str_format):
    """
    Assigns variable attributes to a dataset where they are missing and reformats units according to the provided unit_format.
    Attributes that already exist in the dataset are not changed, except for unit reformatting.

    Parameters
    ----------
    ds (xarray.Dataset): The dataset to which attributes will be assigned.
    vocab_attrs (dict): A dictionary containing the vocabulary attributes to be assigned to the dataset variables.
    unit_str_format (dict): A dictionary mapping old unit strings to new formatted unit strings.

    Returns
    -------
    xarray.Dataset: The dataset with updated attributes.
    attr_warnings (set): A set containing warning messages for attribute mismatches.
    """
    attr_warnings = set()
    for var in ds.variables:
        if var in vocab_attrs:
            for attr, new_value in vocab_attrs[var].items():
                if attr in ds[var].attrs:
                    old_value = ds[var].attrs[attr]
                    if old_value in unit_format:
                        ds[var].attrs[attr] = unit_format[old_value]
                    old_value = ds[var].attrs[attr]
                    if old_value != new_value:
                        warning_msg = f"Warning: Variable '{var}' attribute '{attr}' mismatch: Old value: {old_value}, New value: {new_value}"
#                        print(warning_msg)
                        attr_warnings.add(warning_msg)
                else:
                    ds[var].attrs[attr] = new_value
    return ds, attr_warnings


def convert_units(ds, preferred_units=vocabularies.preferred_units, unit_conversion=vocabularies.unit_conversion):
    """
    Convert the units of variables in an xarray Dataset to preferred units.  This is useful, for instance, to convert cm/s to m/s.

    Parameters
    ----------
    ds (xarray.Dataset): The dataset containing variables to convert.
    preferred_units (list): A list of strings representing the preferred units.
    unit_conversion (dict): A dictionary mapping current units to conversion information.
    Each key is a unit string, and each value is a dictionary with:
        - 'factor': The factor to multiply the variable by to convert it.
        - 'units_name': The new unit name after conversion.

    Returns
    -------
    xarray.Dataset: The dataset with converted units.
    """

    for var in ds.variables:
        current_unit = ds[var].attrs.get('units')
        if current_unit in unit_conversion:
            conversion_info = unit_conversion[current_unit]
            new_unit = conversion_info['units_name']
            if new_unit in preferred_units:
                conversion_factor = conversion_info['factor']
                ds[var] = ds[var] * conversion_factor
                ds[var].attrs['units'] = new_unit

    return ds

def attr_cruise(ds):
    # Open and load the YAML file
    with open('load_data/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    GC_string = ds.GC_STRING.values[0]
    project_id = config[GC_string]['Cruise']['cruise_id']
    platform = config[GC_string]['Cruise']['ship']
    time_cruise_start = config[GC_string]['Cruise']['start_date']
    time_cruise_end = config[GC_string]['Cruise']['end_date']
    sections = config[GC_string]['Cruise']['sections']
    contributor_CTD = config[GC_string]['CTD_Contributor']['name']
    contributor_ADCP = config[GC_string]['ADCP_Contributor']['name']
    geospatial_lat_min = ds.LATITUDE.values.min()
    geospatial_lat_max = ds.LATITUDE.values.max()
    geospatial_lon_min = ds.LONGITUDE.values.min()
    geospatial_lon_max = ds.LONGITUDE.values.max()
    if 'PRES' in ds.variables:
        geospatial_vertical_min = ds.PRES.values.min()
        geospatial_vertical_max = ds.PRES.values.max()
    else:
        geospatial_vertical_min = ds.DEPTH.values.min()
        geospatial_vertical_max = ds.DEPTH.values.max()
    date_created = time.strftime("%Y-%m-%d")

    ### create a directory with all specific attributes for the cruise
    attr_cruise = {'project_id': project_id,
               'platform': platform,
               'time_cruise_start': time_cruise_start,
               'time_cruise_end': time_cruise_end,
               'sections': sections,
               'contributor_CTD': contributor_CTD,
               'contributor_ADCP': contributor_ADCP,
               'geospatial_lat_min': geospatial_lat_min,
               'geospatial_lat_max': geospatial_lat_max,
               'geospatial_lon_min': geospatial_lon_min,
               'geospatial_lon_max': geospatial_lon_max,
               'geospatial_vertical_min': geospatial_vertical_min,
               'geospatial_vertical_max': geospatial_vertical_max,
               'date_created': date_created,
               } 
    return attr_cruise 

def add_attributes(ds):
    """
    Add attributes to the variables in a dataset.

    Parameters
    ----------
    ds (xarray.Dataset): The dataset to which attributes will be added.
    attr_dict (dict): A dictionary where keys are variable names and values are dictionaries of attributes to add.

    Returns
    -------
    xarray.Dataset: The dataset with added attributes.
    """
    attributes = attr_input.attr_general
    ### add the cruise specific attributes
    attributes.update(attr_cruise(ds))

    if 'TEMP' in ds.variables:
        attributes.update(attr_input.attr_CTD)
    elif 'U_WATER_VELOCITY' and 'TEMP' in ds.variables:
        attributes.update(attr_input.attr_merge)
    else:
        attributes.update(attr_input.attr_ADCP)

    ### put the atributes in the right order
    attributes = {key: attributes[key] for key in attr_input.order_of_attr}
    ### add the attributes to the dataset
    for key, value in attributes.items():
        ds.attrs[key] = value
    return ds

def process_dataset(ds):
    # Rename variables and attributes, and convert units where necessary
    #-------------------------------------------------------------------
    # Extract the dataset for 'sg_data_point'
    # Must be after split_ds
    renamed_ds = rename_dimensions(ds)
    # Rename variables according to the OG1 vocabulary
    # Must be after rename_dimensions
    renamed_ds = rename_variables(renamed_ds)
    # Convert units in renamed_ds (especially cm/s to m/s)
    renamed_ds = convert_units(renamed_ds)
    # Assign attributes to the variables
    # Must be ater rename_variables
    renamed_ds, attr_warnings = assign_variable_attributes(renamed_ds)
    # Add attributes to the dataset
    renamed_ds = add_attributes(renamed_ds)

    #vars_to_remove = vocabularies.vars_to_remove
    #ds_new = ds_new.drop_vars([var for var in vars_to_remove if var in ds_new.variables])

    return renamed_ds, attr_warnings