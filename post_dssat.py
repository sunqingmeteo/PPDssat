# coding=utf-8
import os
import time
import numpy as np 
from netCDF4 import Dataset


def rice_mask(_file_path = './'):
    # output: _lat_lon: list number[(lat, lon),]
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

    f_area.close()

    return _lat_lon


def read_dirs(_path = './'):
    # output: list
    _dirs = []
    for root,dirs,files in os.walk(_path):
        if 'A' in root:
            _dirs.append(root)
    _dirs.sort()

    return _dirs


def read_summary(_lat_lon, _dirs):
    # input: _lat_lon: list number[(lat, lon),]; dirs: list [str], same index
    # output: Data structure: _out_dssat is list
    #                 each element is one grid in _out_dssat is dictonrary

    _out_dssat = []
    # Loop each dirs, each point
    for dirs_i in xrange(len(_dirs)):

        # each grid have lat, lon, area, and all year, all yield
        _name_gird_dic = _dirs[dirs_i][-4:]
        _name_gird_dic = {}
        _name_gird_dic['LAT']    = _lat_lon[dirs_i][0]
        _name_gird_dic['LON']    = _lat_lon[dirs_i][1]
        #_name_gird_dic['AREA']   = _area[dirs_i]
        _name_gird_dic['YEAR']   = []
        _name_gird_dic['YIELD']  = []
        _name_gird_dic['ADAT']   = []
        _name_gird_dic['MDAT']   = []
        _name_gird_dic['AAT']    = []    # accumulative active temperature
        _name_gird_dic['SDAT']   = []


        # read summary.out
        with open(_dirs[dirs_i] + '/Summary.OUT', 'r') as fi:
            summary = fi.readlines()

        _yield_dic = {}
        _ADAT_dic = {}
        _MDAT_dic = {}
        _SDAT_dic = {}
        for i in xrange(len(summary)-4):
            # year = summary[i+4][102:106]
            if summary[i+4][102:106] == summary[i+4][126:130]:
                _SDAT_dic[summary[i+4][102:106]] = int(summary[i+4][102:109])
                _ADAT_dic[summary[i+4][102:106]] = int(summary[i+4][126:133])
                _MDAT_dic[summary[i+4][102:106]] = int(summary[i+4][134:141])
                _yield_dic[summary[i+4][102:106]] = int(summary[i+4][167:171])
            # in some situation, rice will harvest next year even set last harvest date
            else:
                _SDAT_dic[summary[i+4][102:106]] = int(summary[i+4][102:109])
                _ADAT_dic[summary[i+4][102:106]] = 0
                _MDAT_dic[summary[i+4][102:106]] = 0
                _yield_dic[summary[i+4][102:106]] = 0


        for k in sorted(_yield_dic.keys()):
            _name_gird_dic['YEAR'].append(k)
            _name_gird_dic['YIELD'].append(_yield_dic[k])
        for k in sorted(_ADAT_dic.keys()):
            _name_gird_dic['ADAT'].append(_ADAT_dic[k])
        for k in sorted(_MDAT_dic.keys()):
            _name_gird_dic['MDAT'].append(_MDAT_dic[k])
        for k in sorted(_SDAT_dic.keys()):
            _name_gird_dic['SDAT'].append(_SDAT_dic[k])

        # read accumulative active temperature, already sorted by year
        aat = np.loadtxt(_dirs[dirs_i] + '/act_temp.csv', dtype=np.str, delimiter=",", skiprows=1)
        aat_list = aat[:,1].tolist()
        for k in xrange(len(aat_list)):
            _name_gird_dic['AAT'].append(round(float(aat_list[k]),2))

        _out_dssat.append(_name_gird_dic)  


    return _out_dssat


def write_nc(_out_dssat, _mask_path = './', _file_path='./'):

    # Open mask file to get useful variables
    f_area = Dataset(_mask_path + '/rice_mask_cn.nc', 'r')
    _lat_mask = f_area.variables['lat'][:]
    _lon_mask = f_area.variables['lon'][:]
    _mask_in = f_area.variables['rice_mask'][:]  # 58 * 76 
    f_area.close()
    
    # Create nc file
    f_nc = Dataset(_file_path + '/DSSAT_Results.nc', 'w', format = 'NETCDF4_CLASSIC')
    lat =  f_nc.createDimension('lat',  len(_lat_mask))
    lon =  f_nc.createDimension('lon',  len(_lon_mask))
    time = f_nc.createDimension('time', len(_out_dssat[0]['YEAR']))

    lats = f_nc.createVariable('lat',  'f',  ('lat',))
    lons = f_nc.createVariable('lon',  'f',  ('lon',))
    times = f_nc.createVariable('time', 'i4', ('time',))
    f_nc.createVariable('YIELD', np.float32, dimensions=('time', 'lat', 'lon',), fill_value=0)
    f_nc.createVariable('ADAT',  np.int32,   dimensions=('time', 'lat', 'lon',), fill_value=0)
    f_nc.createVariable('MDAT',  np.int32,   dimensions=('time', 'lat', 'lon',), fill_value=0)
    f_nc.createVariable('SDAT',  np.int32,   dimensions=('time', 'lat', 'lon',), fill_value=0)
    f_nc.createVariable('AAT',   np.float32, dimensions=('time', 'lat', 'lon',), fill_value=0)

    # Global Attributes
    f_nc.description = 'Qing/NUIST created 05/2018'
    f_nc.source = 'AgMIP climate dataset, CERES-Rice results'

    # Variable Attributes
    times.units = "year"
    times.long_name = "time"
    lats.units = 'degree_north'
    lats.long_name = "latitude"
    lons.units = 'degree_east'
    lons.long_name = "longitude"

    #_new_zeros = np.zeros((_mask_in.shape[0],_mask_in.shape[1],len(_out_dssat[0]['YEAR'])),dtype = np.float)
    _yield_o = np.zeros((_mask_in.shape[0],_mask_in.shape[1],len(_out_dssat[0]['YEAR'])),dtype = np.float)
    _ADAT_o  = np.zeros((_mask_in.shape[0],_mask_in.shape[1],len(_out_dssat[0]['YEAR'])),dtype = np.float)
    _MDAT_o  = np.zeros((_mask_in.shape[0],_mask_in.shape[1],len(_out_dssat[0]['YEAR'])),dtype = np.float)
    _SDAT_o  = np.zeros((_mask_in.shape[0],_mask_in.shape[1],len(_out_dssat[0]['YEAR'])),dtype = np.float)
    _AAT_o   = np.zeros((_mask_in.shape[0],_mask_in.shape[1],len(_out_dssat[0]['YEAR'])),dtype = np.float)

    count_dssat = 0
    break_flag=False
    for i in xrange(_mask_in.shape[0]):
        for j in xrange(_mask_in.shape[1]):
            if count_dssat == (len(_out_dssat)-1):
                    break_flag=True
                    break
            if _mask_in[i,j] == 1:
                _yield_o[i,j] = np.array(_out_dssat[count_dssat]['YIELD'])
                _ADAT_o[i,j]  = np.array(_out_dssat[count_dssat]['ADAT'])
                _MDAT_o[i,j]  = np.array(_out_dssat[count_dssat]['MDAT'])
                _SDAT_o[i,j]  = np.array(_out_dssat[count_dssat]['SDAT'])
                _AAT_o[i,j] = np.array(_out_dssat[count_dssat]['AAT'])
                count_dssat += 1
        if break_flag == True:
            break
    _yield_o = _yield_o.transpose(2,0,1)
    _ADAT_o  = _ADAT_o.transpose(2,0,1)
    _MDAT_o  = _MDAT_o.transpose(2,0,1)
    _SDAT_o  = _SDAT_o.transpose(2,0,1)
    _AAT_o = _AAT_o.transpose(2,0,1)

    # Write variables to nc file
    f_nc.variables['lat'][:] = _lat_mask
    f_nc.variables['lon'][:] = _lon_mask
    f_nc.variables['time'][:] = _out_dssat[0]['YEAR']
    f_nc.variables['YIELD'][:] = _yield_o
    f_nc.variables['ADAT'][:] = _ADAT_o
    f_nc.variables['MDAT'][:] = _MDAT_o
    f_nc.variables['SDAT'][:] = _SDAT_o
    f_nc.variables['AAT'][:] = _AAT_o

    f_nc.close()
   

#######################################################################################

mask_path = '/nuist/u/home/yangzaiqiang/work/mask_rice/'
run_path  = '/nuist/u/home/yangzaiqiang/scratch/run_dssat/'

_lat_lon = rice_mask(mask_path)

dirs = read_dirs(run_path)

_out_dssat = read_summary(_lat_lon, dirs)

write_nc(_out_dssat, mask_path, run_path)





