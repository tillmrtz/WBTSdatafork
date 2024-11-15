import numpy as np
import xarray as xr
from load_data import vocabularies
from load_data import attr_input
import gsw
import logging
from datetime import datetime

_log = logging.getLogger(__name__)


def rename_dimensions(ds, rename_dict=vocabularies.dims_rename_dict):
    """
    Rename dimensions of an xarray Dataset based on a provided dictionary vocabulary.

    Parameters
    ----------
    ds (xarray.Dataset): The dataset whose dimensions are to be renamed.
    rename_dict (dict, optional): A dictionary where keys are the current dimension names 
                                  and values are the new dimension names. Defaults to 
                                  vocabularies.dims_rename_dict.

    Returns
    -------
    xarray.Dataset: A new dataset with renamed dimensions.
    
    Raises:
    Warning: If no variables with dimensions matching any key in rename_dict are found.
    """
    # Check if there are any variables with dimensions matching 'sg_data_point'
    matching_vars = [var for var in ds.variables if any(dim in ds[var].dims for dim in rename_dict.keys())]
    if not matching_vars:
        _log.warning("No variables with dimensions matching any key in rename_dict found.")
    dims_to_rename = {dim: rename_dict[dim] for dim in ds.dims if dim in rename_dict}
    return ds.rename_dims(dims_to_rename)

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
    if 'TEMP' in ds.variables:
        attributes = attr_input.attr_CTD
    elif 'U_WATER_VELOCITY' and 'TEMP' in ds.variables:
        attributes = attr_input.attr_merge
    else:
        attributes = attr_input.attr_ADCP

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