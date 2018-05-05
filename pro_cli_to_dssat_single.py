# coding=utf-8
from netCDF4 import Dataset
import numpy as np
import time
import calendar
import pandas as pd
from datetime import datetime
import os
import re

def datelist(beginDate, endDate):
# beginDate, endDate is '20160601', must add '', is string
# ('%y'): last two string of year  ('%j'): day number in the year
    date_l=[datetime.strftime(x,'%y%j') for x in list(pd.date_range(start=beginDate, end=endDate))]
    return date_l


# _datelist is one year, col 0: doy, col 1-5 is climate data
def read_clm(_year, _wea_list, _path='./'): 
    # get files name
    _wea_list = []
    for _root, _dirs, _files in os.walk(file_dir):
        _wea_list.append(_files)
    _wea_list = _wea_list[0]
    
    # get year of files begin and end
    for i in xrange(len(_wea_list)):
        _m_year = re.match('.*_(\d{4})-(\d{4})\.nc4$', _wea_list[i])
        _begin_day = _m_year.group(1) + '0101'
        _end_day   = _m_year.group(2) + '1231'

    # lon is x 720, lat is y 360
    f1 = Dataset(_wea_list[0],'r')
    lat = f1.variables['lat'][:]
    lon = f1.variables['lon'][:]
    f1.close()

    # find nearest lat and lon, note: numpy array did not have 'index' command, must convert to list
    _latabs = abs(lat - _lat_nj)
    _latindex = _latabs.tolist().index(min(abs(_latabs)))
    _lonabs = abs(lon - _lon_nj)
    _lonindex = _lonabs.tolist().index(min(abs(_lonabs)))
    # print _lonindex, lon[_lonindex], _latindex, lat[_latindex]

    # create time series,  Gregorian date -> Julian date, note:_datelist is 'list', need to convert to array then can print .shape
    _datelist_ini = datelist(_begin_day, _end_day)
    _datelist = np.array(_datelist_ini)
    #print 'Date list:', _datelist, _datelist.shape

    # read vars from climate data
    for _wea in xrange(len(_wea_list)):
        f = Dataset(wea_list[_wea], 'r')
        # exact first strings before '_' as variable name
        _var = wea_list[_wea][0:wea_list[_wea].rfind('_', 0, 7)]
        _cli = f.variables[_var][:, _latindex, _lonindex]
        if _cli.shape == np.array(datelist(_begin_day, _end_day)).shape: 
            _datelist = np.column_stack((_datelist,_cli))
            print 'Now processing', _var, wea_list[_wea], _cli.shape
        else:
            print "Attention! climate data structure not the same as date number"
            os.exit()
        f.close()
    print '_datelist', _datelist.shape, type(_datelist)

    # Climate data UNIT transfer
    # DSSAT UNIT                MERRA UNIT
    # SRAD: MJ m-2 day-1        W m-2            1 w m-2 = 0.0864 MJ m-2 day-1
    # TMAX: C TMIN: C           K
    # RAIN: mm day-1            kg m-2 s-1
    # WIND: km d-1              m s-1
    _datelist = _datelist.astype('float64')
    _datelist[:,1] *= 3600 * 24               #pr
    _datelist[:,2] *= 0.0864                  #srad
    _datelist[:,3] -= 273.15                  #tmax
    _datelist[:,4] -= 273.15                  #tmin
    _datelist[:,5] *= 3.6 * 24                #wind

    return _datelist


def write_clm(_lat_in, lon_in, _year, _datelist, _site_name):
    # generally weather data contain 
    # hur, hurtmax, pr,     rsds, tas, tasmax, tasmin, wind
    #               RAIN,   SRAD,      TMAX,   TMIN,   WIND
    ls = []
    ls.append('*WEATHER : ' + _site_name + ', CHINA, GFDL RCP, QING')
    ls.append(' ')
    ls.append('@ INSI      LAT     LONG  ELEV   TAV   AMP REFHT WNDHT')
    ls.append('  IRPI   ' + str(round(_lat_in, 3)) +'   ' + str(_lon_in) + '    9   16.5  10.3  2.00  2.00')
    ls.append(' ')
    ls.append('@DATE  RAIN  SRAD  TMAX  TMIN  WIND')

    # Create JDZ 2013 CK Tmax 30 C, Tmin 25 C from 13180 to 13220. 
    # Generally, JDZ 13198 was grain filling begin Maturity date: 13211
    #_modify_clim_index_bg = _datelist[:, 0].tolist().index(13193)
    #_modify_clim_index_ed = _datelist[:, 0].tolist().index(13211)
    ##print 'Now generate CK climate data. index from: ', _modify_clim_index_bg, 'to', _modify_clim_index_ed
    #for i in xrange(_modify_clim_index_bg, _modify_clim_index_ed):
    #    _datelist[i, 3] = 30.0
    #    _datelist[i, 4] = 25.0    

    # write to ascii file
    for _row in xrange(_datelist.shape[0]):
        lt = []
        for _col in xrange(_datelist.shape[1]):
            if _col == 0:
                lt.append('%05d' % _datelist[_row,_col])
            else:
                lt.append('%6.1f' % _datelist[_row,_col])
        ls.append(''.join(lt))
    with open(_site_name+'.WTH','w') as fo:
        fo.write('\r\n'.join(ls))

    print 'Finished'



# JDZ lat lon
_lat_jdz = 29.180
_lon_jdz = 117.12
_lat_nj =  32.00
_lon_nj = 118.29

_wea_list = ['pr_bced_1960_1999_gfdl-esm2m_rcp2p6_2011-2020.nc4',     \
            'rsds_bced_1960_1999_gfdl-esm2m_rcp2p6_2011-2020.nc4',   \
            'tasmax_bced_1960_1999_gfdl-esm2m_rcp2p6_2011-2020.nc4', \
            'tasmin_bced_1960_1999_gfdl-esm2m_rcp2p6_2011-2020.nc4', \
            'wind_bced_1960_1999_gfdl-esm2m_rcp2p6_2011-2020.nc4']

read_clm('/Users/qingsun/GGCM/run_dssat/GFDL_RCP2.6/', _datelist)
write_clm(_lat_jdz, _lon_jdz, _datelist, 'CNJD1201')
