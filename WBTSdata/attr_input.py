# Attributes to add for both the CTD and ADCP datasets
contrib_to_append = {
    'contributor_name': 'Till Moritz',
    'contributor_email': 'till.moritz@uni-hamburg.de',
    'contributor_role': 'Student assistant',
    'contributing_institutions': 'University of Hamburg - Institute of Oceanography',
    #'contributing_institutions_role': 'Data scientist',
}

attr_general = {
    'project': 'Western Boundary Time Series',
    'data_url': '',
    'web_link':'https://www.aoml.noaa.gov/phod/wbts/data.php',
    'comment':'GIT repository: https://github.com/ifmeo-hamburg/WBTSdata',
    'featureType':'profile',
    'Conventions':'CF-1.11',
    'sections_vocabulary':'Abaco: ',
}

attr_CTD = {
    'title': 'CTD data of the Abaco Cruise',
    'instrument': 'CTD',
}

attr_ADCP = {
    'title': 'LADCP data of the Abaco Cruise',
    'instrument': 'Lowered Acoustic Doppler Current Profilers',
}
attr_merge = {
    'title': 'CTD and LADCP data of the Abaco Cruise',
    'instrument': 'CTD and Lowered Acoustic Doppler Current Profilers (LADCP)',
}

attr_general.update(contrib_to_append)

order_of_attr = [
    'title', # Which kind of data in the file
    'project', # WBTS
    'project_id', # Both the project and cruise id
    'platform', # ship#s name
    'geospatial_lat_min', # decimal degree
    'geospatial_lat_max', # decimal degree
    'geospatial_lon_min', # decimal degree
    'geospatial_lon_max', # decimal degree
    'geospatial_vertical_min', # meter depth
    'geospatial_vertical_max', # meter depth
    'time_cruise_start', # YYYYmmddTTHHMMss
    'time_cruise_end', # YYYYmmddTTHHMMss
    'sections', # sections that has been covered during the mission   #'site', # the Go-ship section name
    'sections_vocabulary', #'site_vocabulary', # to be defined
    #'program', # WBTS
    #'program_vocabulary', # to be defined
    'contributor_CTD', # Firstname Lastname, Firstname Lastname
    'contributor_ADCP', # Firstname Lastname, Firstname Lastname
    'contributor_name', # Firstname Lastname, Firstname Lastname
    'contributor_email', # name@name.com, name@name.com
    'contributor_role', # Data scientist, Data scientist
    #'contributor_role_vocabular', # http://vocab.nerc.ac.uk/search_nvs/W08/
    'contributing_institutions', # University of Washington, University of Washington
    'data_url', 
    #'doi', # data doi for OG1
    'web_link', #where to find the raw WBTS data
    'comment', # miscellaneous information --> github repository
    'date_created', # date of creation of this dataset YYYYmmddTHHMMss
    'featureType', #profile / defined in CCHDO netcdf files
    'Conventions', # CF-1.11,OG-1.0 --> CF conventions 
]
