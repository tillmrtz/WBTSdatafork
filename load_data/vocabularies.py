dims_rename_dict = {}

# Specify the preferred units, and it will convert if the conversion is available in unit_conversion
preferred_units = ['m s-1', 'dbar', 'Celsius', 'psu', 'umol kg-1', 'gamma', 'm']

# String formats for units.  The key is the original, the value is the desired format
unit_str_format = {
    'cm_per_s': 'cm s-1',
    'meters': 'm',
    'deg c': 'Celcius',
    'psu': 'psu',
    'dyn. cm': 'cm',
    'gamma': 'gamma',
    'umol/kg': 'umol kg-1',
    'dbars': 'dbar',
}

# Various conversions from the key to units_name with the multiplicative conversion factor
unit_conversion = {
    'cm/s': {'units_name': 'm/s', 'factor': 0.01},
    'cm s-1': {'units_name': 'm s-1', 'factor': 0.01},
    'cm_per_s': {'units_name': 'm s-1', 'factor': 0.01},
    'meters': {'units_name': 'm', 'factor': 1},
    'cm': {'units_name': 'm', 'factor': 0.01},
    'dyn. cm': {'units_name': 'cm', 'factor': 1},
}

# Based on https://github.com/voto-ocean-knowledge/votoutils/blob/main/votoutils/utilities/vocabularies.py
standard_names = {
    "latitude": "LATITUDE",
    "longitude": "LONGITUDE",
    "z_depth": "DEPTH",
    "pr": "PRES",
    "ox": "DOXY",
    "te": "TEMP",
    "sa": "PSAL",
    "ctd_density": "POTDENS0", # Seawater potential density - need to check standard name for sigma
    "CAST": "CAST_NUMBER",
    "th": "THETA",
    "u_water_velocity_component": "U_WATER_VELOCITY",
    "v_water_velocity_component": "V_WATER_VELOCITY",
    "error_velocity": "ERROR_VELOCITY",
    "ga": "GAMMA",
    "ht": "DYN_HEIGHT",
    "gc_string": "GC_STRING",
}

vars_to_remove = []

vocab_attrs = {
    "LATITUDE": {
        "coordinate_reference_frame": "urn:ogc:crs:EPSG::4326",
        "long_name": "Latitude north",
        "observation_type": "measured",
        "platform": "platform",
        "reference": "WGS84",
        "standard_name": "latitude",
        "units": "degrees_north",
        "valid_max": 90,
        "valid_min": -90,
        "axis": "Y",
        "URI": "https://vocab.nerc.ac.uk/collection/OG1/current/LAT/",
    },
    "LONGITUDE": {
        "coordinate_reference_frame": "urn:ogc:crs:EPSG::4326",
        "long_name": "Longitude east",
        "observation_type": "measured",
        "platform": "platform",
        "reference": "WGS84",
        "standard_name": "longitude",
        "units": "degrees_east",
        "valid_max": 180,
        "valid_min": -180,
        "axis": "X",
        "URI": "https://vocab.nerc.ac.uk/collection/OG1/current/LON/",
    },
    "DATETIME": {
        "long_name": "time of measurement",
        "units": "UTC time",
        "observation_type": "measured",
        "standard_name": "time",
        "URI": "https://vocab.nerc.ac.uk/collection/P02/current/AYMD/",
    },
    "DEPTH": {
        "source": "pressure",
        "long_name": "glider depth",
        "standard_name": "depth",
        "units": "m",
        "comment": "from science pressure and interpolated",
        "sensor": "sensor_ctd",
        "observation_type": "calculated",
        "accuracy": 1,
        "precision": 2,
        "resolution": 0.02,
        "platform": "platform",
        "valid_min": 0,
        "valid_max": 2000,
        "reference_datum": "surface",
        "positive": "down",
    },
    "DOXY": {
        "long_name": "oxygen concentration",
        "observation_type": "calculated",
        "standard_name": "mole_concentration_of_dissolved_molecular_oxygen_in_sea_water",
        "units": "umol kg-1",
        "valid_max": 425,
        "valid_min": 0,
        "URI": "https://vocab.nerc.ac.uk/collection/P02/current/DOXY/",
    },
    "PRES": {
        "comment": "ctd pressure sensor",
        "sensor": "sensor_ctd",
        "long_name": "Pressure (spatial coordinate) exerted by the water body by profiling pressure sensor and "
        "correction to read zero at sea level",
        "observation_type": "measured",
        "positive": "down",
        "reference_datum": "sea-surface",
        "standard_name": "sea_water_pressure",
        "units": "dbar",
        "valid_max": 2000,
        "valid_min": 0,
        "URI": "https://vocab.nerc.ac.uk/collection/OG1/current/PRES",
    },
    "PSAL": {
        "long_name": "water salinity",
        "standard_name": "sea_water_practical_salinity",
        "units": "1e-3",
        "comment": "Practical salinity of the water body by CTD and computation using UNESCO 1983 algorithm",
        "sources": "CNDC, TEMP, PRES",
        "observation_type": "calculated",
        "sensor": "sensor_ctd",
        "valid_max": 40,
        "valid_min": 0,
        "URI": "https://vocab.nerc.ac.uk/collection/OG1/current/PSAL/",
    },
    "TEMP": {
        "long_name": "Temperature of the water body by CTD ",
        "observation_type": "measured",
        "standard_name": "sea_water_temperature",
        "units": "Celsius",
        "valid_max": 42,
        "valid_min": -5,
        "URI": "https://vocab.nerc.ac.uk/collection/OG1/current/TEMP/",
    },
    "THETA": {
        "long_name": "Potential temperature of the water body by computation using UNESCO 1983 algorithm.",
        "observation_type": "calculated",
        "sources": "salinity temperature pressure",
        "standard_name": "sea_water_potential_temperature",
        "units": "Celsius",
        "valid_max": 42,
        "valid_min": -5,
        "URI": "https://vocab.nerc.ac.uk/collection/OG1/current/THETA/",
    },
    "CAST_NUMBER": {
        "long_name": "Cast index",
        "units": "1",
    },
    "U_WATER_VELOCITY": {
        "long_name": "Eastward water velocity",
        "observation_type": "measured",
        "standard_name": "eastward_sea_water_velocity",
        "units": "m s-1",
        "valid_max": 3,
        "valid_min": -3,
        "URI": "",
    },
    "V_WATER_VELOCITY": {
        "long_name": "Northward water velocity",
        "observation_type": "measured",
        "standard_name": "northward_sea_water_velocity",
        "units": "m s-1",
        "valid_max": 3,
        "valid_min": -3,
        "URI": "",
    },
    "ERROR_VELOCITY": {
        "long_name": "Error in water velocity",
        "observation_type": "measured",
        "standard_name": "error_sea_water_velocity",
        "units": "m s-1",
        "valid_max": 2,
        "valid_min": 0,
        "URI": "",
    },
    "DYN_HEIGHT": {
        "long_name": "Dynamic height",
        "observation_type": "calculated",
        "standard_name": "sea_surface_height_above_geoid",
        "units": "cm",
        "valid_max": 2,
        "valid_min": -2,
        "URI": "",
    },
    "GC_STRING": {
        "long_name": "GC string",
        "units": "1",
    },
    "TIME_FLAG": {
        "long_name": "Time flag",
        "units": "1",
        "Value 0" : "Start time of the cast",
        "Value 1" : "Start time of cast needs to be checked in Cruise report",
        "Value 2" : "End time of cast",

    },

}

# Various sensor vocabularies for OG1: http://vocab.nerc.ac.uk/scheme/OG_SENSORS/current/
sensor_vocabs = {
    "Seabird unpumped CTD": {
        "sensor_type": "CTD",
        "sensor_type_vocabulary": "https://vocab.nerc.ac.uk/collection/L05/current/130/",
        "sensor_maker": "Sea-Bird Scientific",
        "sensor_maker_vocabulary": "https://vocab.nerc.ac.uk/collection/L35/current/MAN0013/",
        "sensor_model": "Sea-Bird CT Sail CTD",
        "sensor_model_vocabulary": "http://vocab.nerc.ac.uk/collection/L22/current/TOOL1188/",
        "long_name": "Sea-Bird CT Sail CTD",
    },
}