import xarray as xr
from . import vocabularies
import yaml
import pathlib
import os

def get_config():
    """
    Get the configuration settings from a YAML file.

    Returns
    -------
    dict: The configuration settings.
    """
    # Set the directory for yaml files as the root directory + 'load_data/' --> Could be in 'config/' instead
    script_dir = pathlib.Path(__file__).parent.absolute()
    parent_dir = script_dir.parents[0]
    rootdir = parent_dir
    config_dir = os.path.join(rootdir, 'load_data')

    ### import basepath from mission_config.yaml
    configpath = os.path.join(config_dir, 'config.yaml')
    with open(configpath, 'r') as file:
        config = yaml.safe_load(file)
    return config

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
