import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import os
import sys

def remove_problematic_attrs(ds):
    for variable in ds.variables.values():
        if 'coordinates' in variable.attrs:
            del variable.attrs['coordinates']

input_file = str(sys.argv[1])
fallow_file = str(sys.argv[2])

if (os.path.exists(input_file) != True):
    print('WRF input file not found.')
    sys.exit(1)
if (os.path.exists(fallow_file) != True):
    print('Fallow NetCDF file not found')

try:
    wrfinput= xr.open_dataset(input_file)
    fallow_data = xr.open_dataset(fallow_file)

except Exception:
    print('You got 99 problems and these files are among them...')
    sys.exit(1)


fallow = fallow_data['Band1']*100
shdmax = wrfinput['SHDMAX']

rep = xr.where(fallow>20,shdmax-fallow,shdmax)

rep = xr.where(rep<0,0.05,rep)
wrfinput['SHDMAX'] = rep
remove_problematic_attrs(wrfinput)
wrfinput.to_netcdf(input_file+'_modified')
wrfinput.close()
