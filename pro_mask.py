#coding=utf-8
from netCDF4 import Dataset
import numpy as np
import numpy.ma as ma

def rice_area_mask(_file_path = './'):
    
    # area, total is 978 girds
    # read rice area mask
    f_area = Dataset(_file_path + '/rice_area_cn.nc', 'r')
    _lat_in = f_area.variables['lat'][:]
    _lon_in = f_area.variables['lon'][:]

    # _area_in missing value is 0
    _area_in = f_area.variables['rice_area_cn2'][_lat_in.tolist().index(34.75):, _lon_in.tolist().index(97.25):]

    _lat_in = _lat_in[_lat_in.tolist().index(34.75):]
    _lon_in = _lon_in[_lon_in.tolist().index(97.25):]

    m = _area_in.shape[0]
    n = _area_in.shape[1]
    _area_in_ones = np.ones((m,n))
    _area_in_mask = np.where(_area_in > 0, _area_in_ones, _area_in)
 
    # read AgMIP mask
    f_agmip = Dataset('/Users/qingsun/GGCM/run_dssat/GFDL_RCP2.6/tasmax_bced_1960_1999_gfdl-esm2m_historical_1951-1960.nc4', 'r')
    _lat_agmip = f_agmip['lat'][:]
    _lon_agmip = f_agmip['lon'][:]
    # _tasmax missing value = 1.e+20
    _tasmax = f_agmip['tasmax'][0, _lat_agmip.tolist().index(max(_lat_in)):(_lat_agmip.tolist().index(min(_lat_in))+1), _lon_agmip.tolist().index(min(_lon_in)):(_lon_agmip.tolist().index(max(_lon_in))+1)]

    _area_mask = np.where(_tasmax == _tasmax.fill_value, 0, _tasmax)
    _area_mask = np.where(_area_mask == 1.0e20, 0, _area_mask)
    _area_mask = np.where(_area_mask != 0, 1, _area_mask)
    _rice_mask = np.where(_area_mask == 0, _area_mask, _area_in_mask)
    _rice_mask = np.where(_rice_mask < 0, 0, _rice_mask)

    # write to nc file 
    f_mask = Dataset(_file_path + '/rice_mask_cn.nc', 'w')
    lat_out = f_mask.createDimension('lat', len(_lat_in))
    lon_out = f_mask.createDimension('lon', len(_lon_in))
    #time_out = f_mask.createDimension('time', None)
    
    f_mask.createVariable('lat', 'f', ('lat',))
    f_mask.createVariable('lon', 'f', ('lon',))
    #f_mask.createVariable('time', np.int32, ('time',))
    f_mask.createVariable('rice_mask', np.int32, dimensions=('lat', 'lon',), fill_value=0)

    # Global Attributes
    f_mask.description = 'Qing/NUIST created 2018-05'
    f_mask.source = 'IRRI and AgMIP rice mask'

    f_mask.variables['lat'][:] = _lat_in
    f_mask.variables['lon'][:] = _lon_in
    f_mask.variables['rice_mask'][:] = _rice_mask

    f_mask.close()

    _lat_lon = []
    _area = []
    for i in xrange(len(_lat_in)):
        for j in xrange(len(_lon_in)):
            _area.append(_area_in[i,j] / 1000 / 1000)
            _lat_lon.append([_lat_in[i], _lon_in[j]])

    return _lat_lon, _area    

_lat_lon, _area = rice_area_mask('/Users/qingsun/GGCM/mask_rice/')

