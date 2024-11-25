# Attributes to add for both the CTD and ADCP datasets
contrib_to_append = {
    'contributor_name': 'Eleanor Frajka-Williams',
    'contributor_email': 'eleanorfrajka@gmail.com',
    'contributor_role': 'Data scientist',
    #'contributor_role_vocabulary': 'http://vocab.nerc.ac.uk/search_nvs/W08',
    'contributing_institutions': 'University of Hamburg - Institute of Oceanography',
    #'contributing_institutions_vocabulary': 'https://edmo.seadatanet.org/report/1156',
    'contributing_institutions_role': 'Data scientist',
    #'contributing_institutions_role_vocabulary': 'http://vocab.nerc.ac.uk/search_nvs/W08',
}

attr_CTD = {
    'title': 'CTD data of the Abaco Cruise',
    'platform': 'CTD',
    'project': 'Western Boundary Time Series',
    'doi': '',
    'data_url': '',
}

attr_ADCP = {
    'title': 'LADCP data of the Abaco Cruise',
    'platform': 'Lowered Acoustic Doppler Current Profilers',
    'project': 'Western Boundary Time Series',
    'doi': '',
    'data_url': '', # file where created data is located
}
attr_merge = {
    'title': 'CTD and LADCP data of the Abaco Cruise',
    'platform': 'CTD and Lowered Acoustic Doppler Current Profilers (LADCP)',
    'project': 'Western Boundary Time Series',
    'doi': '',
    'data_url': '',
}

attr_CTD.update(contrib_to_append)
attr_ADCP.update(contrib_to_append)
attr_merge.update(contrib_to_append)

order_of_attr = [
    'title', # OceanGliders trajectory file
    #'id', # sg015_20040920T000000_delayed
    #'platform_vocabulary', # https://vocab.nerc.ac.uk/collection/L06/current/27
    'platform', # ship 
    #'PLATFORM_SERIAL_NUMBER', # sg015
    #'naming_authority', # edu.washington.apl
    #'institution', # University of washington
    #'internal_mission_identifier', # p0150003_20040924
    'geospatial_lat_min', # decimal degree
    'geospatial_lat_max', # decimal degree
    'geospatial_lon_min', # decimal degree
    'geospatial_lon_max', # decimal degree
    'geospatial_vertical_min', # meter depth
    'geospatial_vertical_max', # meter depth
    'time_coverage_start', # YYYYmmddTTHHMMss
    'time_coverage_end', # YYYYmmddTTHHMMss
    'site', # the Go-ship section name
    'site_vocabulary', # to be defined
    'program', # WBTS
    'program_vocabulary', # to be defined
    #'project', # SAMBA
    #'network', # Southern California Coastal Ocean Observing System (SCCOOS)
    'contributor_name', # Firstname Lastname, Firstname Lastname
    'contributor_email', # name@name.com, name@name.com
    #'contributor_id', # ORCID, ORCID
    'contributor_role', # Data scientist, Data scientist
    'contributor_role_vocabular', # http://vocab.nerc.ac.uk/search_nvs/W08/
    'contributing_institutions', # University of Washington, University of Washington
    'contributing_institutions_vocabulary', # https://edmo.seadatanet.org/report/544, https://ror.org/012tb2g32
    #'contributing_institutions_role', # PI, Operator
    #'contributing_institutions_role_vocabulary', # https://vocab.nerc.ac.uk/collection/W08/current/
    #'uri', # other universal resource identifiers separated by commas
    'data_url', #url link to where OG1.0 file is hosted
    'doi', # data doi for OG1
    #'rtqc_method', # No QC applied
    #'rtqc_method_doi', # n/a
    'web_link', # url for information rleated to glider mission, multiple urls separated by comma
    'comment', # miscellaneous information --> github repository
    #'start_date', # datetime of glider deployment YYYYmmddTHHMMss
    'date_created', # date of creation of this dataset YYYYmmddTHHMMss
    'featureType', #profile / defined in CCHDO netcdf files
    'Conventions', # CF-1.11,OG-1.0 --> CF conventions 
]
