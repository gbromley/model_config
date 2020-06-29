import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import netCDF4
from scipy import stats
import statsmodels.api as sm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sys
from mpl_toolkits.axes_grid1 import make_axes_locatable
sys.path.append('/Users/gbromley/Dropbox/code/python_utilities/')
from python_data_functions import extract_months
from python_met_functions import sat_vap_pres
from python_data_functions import mk_test
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from matplotlib.offsetbox import AnchoredText
import plotting_functions as pf
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER


# In[4]:


data_dir = '/glade/work/gbromley/CRU/'
wrf_data = '/Users/gbromley/data/fallow_simulations/12km_verification/12km_verification_monthly_crugrid.nc'
temp_file = 'pre/cru_ts4.03.1901.2018.pre.dat.nc'
CRU_TEMP = xr.open_dataset(data_dir+temp_file)
WRF_PRECIP = xr.open_dataset(wrf_data)

### Random Definitions
ext_e = -92
ext_w = -115
ext_n = 55
ext_s = 40

start_year = '2010-10-01'
end_year = '2011-10-01'


### Study Area
ngp_mask = xr.open_dataset('/Users/gbromley/Dropbox/Montana_Climate_Project/Study_Area/ngp_mask.nc')
ngp_mask = ngp_mask.rename({'__xarray_dataarray_variable__':'ngp'})
mask = ngp_mask['ngp']


### Extract Variables
CRU = CRU_TEMP['pre'].sel(time=slice(start_year,end_year))



### Ouput Data
month = ['October','November','December','January','February','March','April','May','June','July','August','September']
lat = CRU.lat
lon = CRU.lon
vals = np.empty(shape=(12,len(lat),len(lon)))
vals[:,:,:] = np.nan
DIFF = xr.DataArray(vals,coords=[month,lat,lon],dims=['month','lat','lon'])
DIFF.name = '2011 Control - CRU'
DIFF.attrs['units'] = 'mm'



# In[ ]:


WRF_PRECIP['I_RAINNC']


# In[7]:


precip = WRF_PRECIP['RAINNC']+1000.0*WRF_PRECIP['I_RAINNC']


# In[ ]:


precip


# In[ ]:



wrf_test = WRF_PRECIP.isel(XTIME=8) - WRF_PRECIP.isel(XTIME=7)


# In[8]:


months = [1,2,3,4,5,6,7,8,9,10,11]
DIFF[0] = 100.0*((precip.isel(XTIME=0)-CRU.isel(time=0))/(CRU.isel(time=0)))
for month in months:
        DIFF[month] = 100.0*(((precip.isel(XTIME=month) - precip.isel(XTIME=(month-1)))-(CRU.isel(time=month)))/(CRU.isel(time=month)))


# In[ ]:



CRU = CRU.sel(lat=slice(ext_s-5,ext_n+5),lon=slice(ext_w-5,ext_e+5))
#wrf_test = wrf_test.sel(lat=slice(ext_s-5,ext_n+5),lon=slice(ext_w-5,ext_e+5))
DIFF = DIFF.sel(lat=slice(ext_s-5,ext_n+5),lon=slice(ext_w-5,ext_e+5))


# In[ ]:


DIFF_test


# In[ ]:


DIFF.isel(month=6).plot()


# In[ ]:


diff_ngp = DIFF_test.where(mask==1)


# In[ ]:


CRU_test.isel(time=8).plot()


# In[ ]:


wrf_test.plot()


# In[9]:


ngp = DIFF.where(mask==1)
test = ngp.stack(z=('lat','lon'))
#
season_values = test.groupby('month').apply(lambda x: x.dropna(dim='z'))


# In[ ]:


diff_ngp.isel(month=8).plot()


# In[21]:


plt.rcParams.update({'font.size': 22})
month = ['N','D','J','F','M','A','M','J','J','A','S']
fig, ax = plt.subplots(ncols=1)
fig.set_dpi(400)
fig.set_size_inches((13,7))
fig.suptitle('Percent Difference WRF-CRU')
pos = np.array(range(len(season_values))) + 1
plt.boxplot(season_values, positions=pos)
plt.xticks([1, 2, 3,4,5,6,7,8,9,10,11], month)
ax.axhline(1)
plt.ylabel('Percent Change (%)')
plt.ylim((-150,150))

#ax.set_ylabel('Precip Difference (mm)')
plt.savefig('/Users/gbromley/Dropbox/Montana_Climate_Project/NGP Modeling Paper/Control_Diagnostics/12km_boxplot_precip.png',bbox_inches='tight')


# In[20]:


plt.rcParams.update({'font.size': 12})
#create figure
cb_min = -6
cb_max = 6
cols = ['#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de','#4393c3','#2166ac','#053061']
cus_cols = cols[::-1]
levs = [-150,-125,-100,-75,-50,-25,0,25,50,75,100,125,150]
#np.linspace(cb_min, cb_max, len(cus_col))
fig = plt.figure(1,figsize=(13,7), dpi=400.0)
#create projection
projection = ccrs.LambertConformal(central_longitude=-105,central_latitude=45,standard_parallels=[50,40])
ax1 = plt.subplot(2,2,1, projection = projection)

cb = plt.contourf(DIFF.lon,DIFF.lat,DIFF[[1,2,3]].mean(dim='month').values,transform=ccrs.PlateCarree(),levels=levs,cmap='BrBG', extend='both')
ax1.set_extent([ext_e, ext_w, ext_s, ext_n])
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')
ax1.add_feature(states_provinces, edgecolor='black',linewidth=0.2)
ax1.add_feature(cfeature.COASTLINE)
ax1.add_feature(cfeature.BORDERS)
shape_feature = ShapelyFeature(Reader('/Users/gbromley/Dropbox/Montana_Climate_Project/Study_Area/NGP_Study_Area/Study_Area_08_01_17.shp').geometries(),crs=ccrs.PlateCarree(), facecolor='none',edgecolor='black')
ax1.add_feature(shape_feature)
ax1.title.set_text('DJF')
at = AnchoredText("a",
                  prop=dict(size=8), frameon=True,
                  loc=2,
                  #backgroundcolor = 'lightgray'
                  )
ax1.add_artist(at)

# *must* call draw in order to get the axis boundary used to add ticks:
fig.canvas.draw()

# Define gridline locations and draw the lines using cartopy's built-in gridliner:
xticks = [-130,-120,-110, -100, -90, -80]
yticks = [30, 40, 50, 60]
ax1.gridlines(xlocs=xticks, ylocs=yticks, linewidth=0)

# Label the end-points of the gridlines using the custom tick makers:
ax1.xaxis.set_major_formatter(LONGITUDE_FORMATTER) 
ax1.yaxis.set_major_formatter(LATITUDE_FORMATTER)
pf.lambert_xticks(ax1, xticks)
pf.lambert_yticks(ax1, yticks)
ax1.xaxis.label.set_visible(False)
ax1.yaxis.label.set_visible(False)


ax2 = plt.subplot(2,2,2, projection = projection)

plt.contourf(DIFF.lon,DIFF.lat,DIFF[[4,5,6]].mean(dim='month').values,transform=ccrs.PlateCarree(),levels=levs,cmap='BrBG', extend='both')

ax2.set_extent([ext_e, ext_w, ext_s, ext_n])
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')
ax2.add_feature(states_provinces, edgecolor='black',linewidth=0.2)
ax2.add_feature(cfeature.COASTLINE)
ax2.add_feature(cfeature.BORDERS)
ax2.add_feature(shape_feature)
bt = AnchoredText("b",
                  prop=dict(size=8), frameon=True,
                  loc=2,
                  #backgroundcolor = 'lightgray'
                  )
ax2.add_artist(bt)
ax2.set_title('MAM')
#ax2.title.set_visible(False)

# *must* call draw in order to get the axis boundary used to add ticks:
fig.canvas.draw()

# Define gridline locations and draw the lines using cartopy's built-in gridliner:
xticks = [-130,-120,-110, -100, -90, -80]
yticks = [30, 40, 50, 60]
ax2.gridlines(xlocs=xticks, ylocs=yticks, linewidth=0)

# Label the end-points of the gridlines using the custom tick makers:
ax2.xaxis.set_major_formatter(LONGITUDE_FORMATTER) 
ax2.yaxis.set_major_formatter(LATITUDE_FORMATTER)
pf.lambert_xticks(ax2, xticks)
pf.lambert_yticks(ax2, yticks)
ax2.xaxis.label.set_visible(False)
ax2.yaxis.label.set_visible(False)



ax3 = plt.subplot(2,2,3, projection = projection)

plt.contourf(DIFF.lon,DIFF.lat,DIFF[[7,8,9]].mean(dim='month').values,transform=ccrs.PlateCarree(),levels=levs,cmap='BrBG', extend='both')
#ax = plt.axes(projection=ccrs.LambertConformal())

ax3.set_extent([ext_e, ext_w, ext_s, ext_n])
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')
ax3.add_feature(states_provinces, edgecolor='black',linewidth=0.2)
ax3.add_feature(cfeature.COASTLINE)
ax3.add_feature(cfeature.BORDERS)
ax3.add_feature(shape_feature)
ct = AnchoredText("c",
                  prop=dict(size=8), frameon=True,
                  loc=2,
                  #backgroundcolor = 'lightgray'
                  )
ax3.add_artist(ct)
ax3.set_title('JJA')

# *must* call draw in order to get the axis boundary used to add ticks:
fig.canvas.draw()

# Define gridline locations and draw the lines using cartopy's built-in gridliner:
xticks = [-130,-120,-110, -100, -90, -80]
yticks = [30, 40, 50, 60]
ax3.gridlines(xlocs=xticks, ylocs=yticks, color='black', linewidth = 0.0)

# Label the end-points of the gridlines using the custom tick makers:
ax3.xaxis.set_major_formatter(LONGITUDE_FORMATTER) 
ax3.yaxis.set_major_formatter(LATITUDE_FORMATTER)
pf.lambert_xticks(ax3, xticks)
pf.lambert_yticks(ax3, yticks)
ax3.xaxis.label.set_visible(False)
ax3.yaxis.label.set_visible(False)



'''
ax4 = plt.subplot(2,2,4, projection = projection)

plt.contourf(spatial_trend.lon,spatial_trend.lat,spatial_trend[3,:,:].values,transform=ccrs.PlateCarree(),levels=levs,cmap='RdBu_r', extend='both')
#ax = plt.axes(projection=ccrs.LambertConformal())
pvals[3,:,:].plot.contourf(axes=ax1,transform=ccrs.PlateCarree(),color='none',edgecolor='black',hatches=["..."],alpha=0.,add_colorbar = False)
ax4.set_extent([ext_e, ext_w, ext_s, ext_n])
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')
ax4.add_feature(states_provinces, edgecolor='black',linewidth=0.2)
ax4.add_feature(cfeature.COASTLINE)
ax4.add_feature(cfeature.BORDERS)
ax4.add_feature(shape_feature)
dt = AnchoredText("d",
                  prop=dict(size=8), frameon=True,
                  loc=2,
                  #backgroundcolor = 'lightgray'
                  )
ax4.add_artist(dt)
ax4.set_title('SON')
fig.subplots_adjust(top=0.9,bottom=0.1,left=0.25,right=0.75,hspace=0.1,wspace=0.1)
#fig.suptitle('Temperature Trends 1970-2015')
cax = fig.add_axes((0.76, 0.12, 0.03, 0.76))
col_bar = fig.colorbar(cb,cax=cax)
col_bar.set_label('$^\circ$C / Decade',fontsize=10)

# *must* call draw in order to get the axis boundary used to add ticks:
fig.canvas.draw()

# Define gridline locations and draw the lines using cartopy's built-in gridliner:
xticks = [-130,-120,-110, -100, -90, -80]
yticks = [30, 40, 50, 60]
ax4.gridlines(xlocs=xticks, ylocs=yticks, linewidth=0)

# Label the end-points of the gridlines using the custom tick makers:
ax4.xaxis.set_major_formatter(LONGITUDE_FORMATTER) 
ax4.yaxis.set_major_formatter(LATITUDE_FORMATTER)
pf.lambert_xticks(ax4, xticks)
pf.lambert_yticks(ax4, yticks)
ax4.xaxis.label.set_visible(False)
ax4.yaxis.label.set_visible(False)
'''

fig.subplots_adjust(top=0.9,bottom=0.1,left=0.25,right=0.75,hspace=0.2,wspace=0.3)
#fig.suptitle('Precipitation Trends 1970-2015')
cax = fig.add_axes((0.76, 0.12, 0.03, 0.76))
col_bar = fig.colorbar(cb,cax=cax)
col_bar.set_label('Change (%)',fontsize=14)

plt.savefig('/Users/gbromley/Dropbox/Montana_Climate_Project/NGP Modeling Paper/Control_Diagnostics/12km_seasonal_precip.png',bbox_inches='tight')
plt.show()


# In[13]:


month[6]


# In[19]:


month = ['October','November','December','January','February','March','April','May','June','July','August','September']
plt.rcParams.update({'font.size': 12})
month_num = 8
#create figure
cb_min = -6
cb_max = 6
cols = ['#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de','#4393c3','#2166ac','#053061']
cus_cols = cols[::-1]
levs = [-150,-125,-100,-75,-50,-25,0,25,50,75,100,125,150]
#np.linspace(cb_min, cb_max, len(cus_col))
fig = plt.figure(1,figsize=(13,7), dpi=400.0)
#create projection
projection = ccrs.LambertConformal(central_longitude=-105,central_latitude=45,standard_parallels=[50,40])
ax1 = plt.subplot(1,1,1, projection = projection)

cb = plt.contourf(DIFF.lon,DIFF.lat,DIFF[[month_num]].mean(dim='month').values,transform=ccrs.PlateCarree(),levels=levs,cmap='BrBG', extend='both')
ax1.set_extent([ext_e, ext_w, ext_s, ext_n])
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')
ax1.add_feature(states_provinces, edgecolor='black',linewidth=0.2)
ax1.add_feature(cfeature.COASTLINE)
ax1.add_feature(cfeature.BORDERS)
shape_feature = ShapelyFeature(Reader('/Users/gbromley/Dropbox/Montana_Climate_Project/Study_Area/NGP_Study_Area/Study_Area_08_01_17.shp').geometries(),crs=ccrs.PlateCarree(), facecolor='none',edgecolor='black')
ax1.add_feature(shape_feature)
ax1.title.set_text(month[month_num])
at = AnchoredText("a",
                  prop=dict(size=8), frameon=True,
                  loc=2,
                  #backgroundcolor = 'lightgray'
                  )
ax1.add_artist(at)

# *must* call draw in order to get the axis boundary used to add ticks:
fig.canvas.draw()

# Define gridline locations and draw the lines using cartopy's built-in gridliner:
xticks = [-130,-120,-110, -100, -90, -80]
yticks = [30, 40, 50, 60]
ax1.gridlines(xlocs=xticks, ylocs=yticks, linewidth=0)

# Label the end-points of the gridlines using the custom tick makers:
ax1.xaxis.set_major_formatter(LONGITUDE_FORMATTER) 
ax1.yaxis.set_major_formatter(LATITUDE_FORMATTER)
pf.lambert_xticks(ax1, xticks)
pf.lambert_yticks(ax1, yticks)
ax1.xaxis.label.set_visible(False)
ax1.yaxis.label.set_visible(False)

fig.subplots_adjust(top=0.9,bottom=0.1,left=0.25,right=0.75,hspace=0.2,wspace=0.2)
#fig.suptitle('Precipitation Trends 1970-2015')
cax = fig.add_axes((0.76, 0.12, 0.03, 0.76))
col_bar = fig.colorbar(cb,cax=cax)
col_bar.set_label('Change (%)',fontsize=12)



