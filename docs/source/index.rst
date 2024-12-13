.. WBTSdata documentation master file, created by
   sphinx-quickstart on Tue Oct 29 11:30:19 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to WBTSdata's documentation!
======================================

WBTSdata is a Python package aiming to create netCDF files for each individual year of the Western Boundary Times Series (WBTS) project.

The WBTS is a comprehensive observational program designed to monitor the Atlantic Meridional Overturning Circulation (AMOC) and its associated boundary currents, such as the Florida and Antilles Currents. These observations are critical for understanding the role of ocean circulation in regulating global climate and assessing changes over time.
The program is primarily conducted by the National Oceanic and Atmospheric Administration (NOAA). Data are collected along hydrographic sections using ship-based methods, which include:

Lowered Acoustic Doppler Current Profiler (LADCP): This instrument measures water velocity throughout the water column, providing detailed insights into the flow patterns of boundary currents.
Conductivity-Temperature-Depth (CTD): These sensors measure the physical properties of seawater, such as temperature, salinity, and density, which are essential for characterizing oceanographic conditions.
The calibrated WBTS data, including LADCP and CTD measurements, are made publicly available through NOAA’s Atlantic Oceanographic and Meteorological Laboratory (AOML) (see: https://www.aoml.noaa.gov/western-boundary-time-series/).
 
We provide an example notebook to demonstrate how the data is loaded and merged into xarray.Datasets. The data is then saved as netCDF files for each individual year.

======================================

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   demo.ipynb
   WBTSdata


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
