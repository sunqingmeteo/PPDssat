#coding=utf-8
from netCDF4 import Dataset

def rice_area_mask(_file_path = './'):

    f_area = Dataset(_file_path + '/rice_mask_cn.nc', 'r')
    _lat_in = f_area.variables['lat'][:]
    _lon_in = f_area.variables['lon'][:]
    _mask_in = f_area.variables['rice_mask'][:]
    
    _lat_lon = []
    _area = []
    for i in xrange(len(_lat_in)):
        for j in xrange(len(_lon_in)):
            if _mask_in[i,j] == 1:
                _lat_lon.append([_lat_in[i], _lon_in[j]])

    return _lat_lon

#_lat_lon, _area = rice_area_mask('/Users/qingsun/GGCM/mask_rice/')
