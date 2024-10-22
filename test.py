import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

moor3 = xr.open_dataset('/Users/tillmoritz/Desktop/Studies/Master_Studies/Messmethoden_Fernerkundung/Mooring_data/Aquadopp')

moor3.plot()