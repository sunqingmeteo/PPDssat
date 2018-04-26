# coding=utf-8
# latlon.csv contains all grid of lat lon, lon is x 720, lat is y 360
from netCDF4 import Dataset
import numpy as np


f1 = Dataset('./GFDL_RCP2.6/pr_bced_1960_1999_gfdl-esm2m_historical_1950.nc4','r')
lat = f1.variables['lat'][:]
lon = f1.variables['lon'][:]
f1.close()

print type(lat),lat.shape

ls = []
ls.append('lat,lon')
for i in xrange(len(lat)):
    for j in xrange(len(lon)):
        ls.append(str(lat[i]) + ',' + str(lon[j]))

with open('latlon.csv','w') as fo:
    fo.write('\n'.join(ls))



# choose selected grid contains double cropping rice







#with open('latlon_mask.csv','w') as foo:
#    foo.write('\n'.join(ls))
