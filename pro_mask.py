#coding=utf-8
from netCDF4 import Dataset

def rice_area_mask(_file_path = './'):
    # area, total is 978 girds
    f_area = Dataset(_file_path + '/rice_area_cn.nc', 'r')
    _lat_in = f_area.variables['lat'][:]
    _lon_in = f_area.variables['lon'][:]
    _area_in = f_area.variables['rice_area_cn2'][:]
    
    _lat_lon = []
    _area = []
    for i in xrange(len(_lat_in)):
        if _lat_in[i] <= 35.0:
            for j in xrange(len(_lon_in)):
                if _lon_in[j] >= 97.0:
                    if _area_in[i,j] > 0.0: 
                        _area.append(_area_in[i,j] / 1000 / 1000)
                        _lat_lon.append([_lat_in[i], _lon_in[j]])

    return _lat_lon, _area    

#_lat_lon, _area = rice_area_mask('/Users/qingsun/GGCM/mask_rice/')

