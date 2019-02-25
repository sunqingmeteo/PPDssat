# coding=utf-8
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import os


def plot_PPDssat(lons, lats, _yield_mask, fig_name, colorbar_label, unit = 'kg ha-1', colors='jet'):
    plt.clf() # Clear old fig, create a new one
    plt.rcParams["font.family"] = "Times New Roman"

    m = Basemap(llcrnrlon=82, llcrnrlat=12, urcrnrlon=140, urcrnrlat=53, 
                projection='lcc', lat_1=33, lat_2=45, lon_0=110, suppress_ticks=True)

    lon, lat = np.meshgrid(lons, lats)
    xi, yi = m(lon, lat)

    # Add Grid Lines
    # lat and lon line
    #m.drawparallels(np.arange(-90., 91., 20.), labels=[1,0,0,0], fontsize=10)
    #m.drawmeridians(np.arange(-180., 181., 40.), labels=[0,0,0,1], fontsize=10)
    m.drawparallels(np.arange(0., 80., 10.), labels=[1,0,0,0], fontsize=10, linewidth=0.0)
    m.drawmeridians(np.arange(70., 140., 10.), labels=[0,0,0,1], fontsize=10,linewidth=0.0)

    # Add Coastlines, States, and Country Boundaries
    #m.drawcoastlines()
    #m.drawlsmask(land_color = "white", ocean_color="deepskyblue")
    #m.drawcountries()
    #m.readshapefile('/Users/qingsun/GGCM/mask_rice/china_basic_map/rivers', 'states', color='royalblue', linewidth=1, drawbounds=True)
    m.readshapefile('/Users/qingsun/GGCM/mask_rice/new_cn_map_shp2014/province','states',drawbounds=True)

    cmap = plt.get_cmap(colors)

    cs = m.contourf(xi, yi, _yield_mask, levels=colorbar_label, cmap=cmap)
    cbar = m.colorbar(cs, location='bottom', pad="10%")
    plt.title(fig_name, fontsize=12, color='black')
    cbar.set_label(unit)
    cbar.set_ticks(colorbar_label)
    cbar.set_ticklabels(tuple(map(str,colorbar_label.tolist())))  

    #plt.title('Rice Yield') 
    plt.savefig(fig_name + '.png', dpi = 300, bbox_inches='tight')
    #plt.show()
#################################### PLOT #####################################

# Read NC file
# meteo_file = "/Users/qingsun/Desktop/pdssat_erai_hist_default_firr_yield_ric_annual_1979_2010.nc4"
meteo_file = '/Users/qingsun/GGCM/run_dssat/PPDSSAT_OUT.nc'

fh = Dataset(meteo_file, mode='r')
_vars = fh.variables.keys()
print _vars

lons = fh.variables['lon'][:]
lats = fh.variables['lat'][:]
time = fh.variables['time'][:].astype('int')
print time

plot_var = 'HWAM'
_var_out = fh.variables[plot_var][:,:,:]
print _var_out.shape
fh.close()


for i in xrange(_var_out.shape[0]):
    fig_name = 'PPDssat_%s_%s' % (plot_var,time[i])
    print 'Plotting %s' % fig_name
    plot_PPDssat(lons, lats, _var_out[i,:,:], fig_name, 
                 colors='jet', unit='Yield (kg/ha)',
                 colorbar_label = np.linspace(0, 15000, 11, dtype = int))








