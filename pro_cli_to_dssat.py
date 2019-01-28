# coding=utf-8
from netCDF4 import Dataset
import numpy as np
import time
import calendar
import pandas as pd
from datetime import datetime
import os
import re
from date_cal import daysBetweenDates, isLeapYear


def datelist(beginDate, endDate):
# beginDate, endDate is '20160601', must add '', is string
# ('%y'): last two string of year  ('%j'): day number in the year
    date_l=[datetime.strftime(x,'%y%j') for x in list(pd.date_range(start=beginDate, end=endDate))]
    return date_l


def clm_list(_year, _climate_path = './'):
    _clm_list = []
    for _root,_dirs,_files in os.walk(_climate_path):
        _clm_list.append(_files)
    _clm_list = _clm_list[0]
    _clm_list.sort()

    # Find file names of selected year, 1951-2099
    _clm_year_list = []
    for _clmi in xrange(len(_clm_list)):
        _m_year = re.match('.*_(\d{4})-(\d{4})\.nc4$', _clm_list[_clmi])
        if _m_year:
            _clm_year_bg = _m_year.group(1)
            _clm_year_ed = _m_year.group(2)
            _clm_year_list.append([_clm_year_bg, _clm_year_ed])
    #print _clm_year_list

    _clm_fine_year_list = []
    for _clm_year_group in xrange(len(_clm_year_list)):
        if _year in xrange(int(_clm_year_list[_clm_year_group][0]), int(_clm_year_list[_clm_year_group][1]) +1):
            #print _clm_year_list[_clm_year_group][0], _clm_year_list[_clm_year_group][1]
            #print _clm_year_group
            _clm_fine_year_list.append(_climate_path + _clm_list[_clm_year_group])
    return _clm_fine_year_list


# _datelist is one year, col 0: doy, col 1-5 is climate data
def read_clm(_lat_in, _lon_in, _year, _wea_list, _climate_path='./'):
    # create time series,  Gregorian date -> Julian date, note:_datelist is 'list', need to convert to array then can print .shape
    _begin_day = str(_year) + '0101'
    _end_day = str(_year) + '1231'
    _datelist = datelist(_begin_day, _end_day)

    _nctime_bg = daysBetweenDates(1860,1,1,_year,1,1)
    if isLeapYear(_year):
        _nctime_ed = _nctime_bg + 366
    else:
        _nctime_ed = _nctime_bg + 365
    #print _nctime_bg, _nctime_ed

    # read vars from climate data
    _var_list = ['pr', 'rsds', 'tasmax', 'tasmin', 'wind']
    _var_trans = {'pr': 'RAIN', 
                  'tasmax': 'TMAX',
                  'tasmin': 'TMIN',
                  'rsds': 'SRAD',
                  'wind': 'WIND'}
    _clm_dic = {}
    _clm_dic['DATE'] = _datelist
    for _wea in xrange(len(_wea_list)):
        f = Dataset(_wea_list[_wea], 'r')
        _time = f.variables['time'][:]
        _time = _time.astype(np.int64)
        _nctime_bg_index = int(_time.tolist().index(_nctime_bg))
        _nctime_ed_index = int(_time.tolist().index(_nctime_ed))

        # find nearest lat and lon, note: numpy array did not have 'index' command, must convert to list
        _lat = f.variables['lat'][:]
        _lon = f.variables['lon'][:]
        _latabs = abs(_lat - _lat_in)
        _latindex = _latabs.tolist().index(min(abs(_latabs)))
        _lonabs = abs(_lon - _lon_in)
        _lonindex = _lonabs.tolist().index(min(abs(_lonabs)))
        
        #exact var name
        for i in _var_trans.keys():
            if i in _wea_list[_wea]:
                _var = i
        #print _wea_list[_wea], _var, _nctime_bg_index, _nctime_ed_index
        _clm_var = f.variables[_var][_nctime_bg_index:_nctime_ed_index, _latindex, _lonindex]
        _clm_var = _clm_var.astype('float64')

        # Climate data UNIT transfer
        # DSSAT UNIT                MERRA UNIT
        # RAIN: mm day-1            kg m-2 s-1
        # SRAD: MJ m-2 day-1        W m-2            1 w m-2 = 0.0864 MJ m-2 day-1
        # TMAX: C TMIN: C           K
        # WIND: km d-1              m s-1
        if _var == 'pr':
            _clm_var *= 3600 * 24 
        if _var == 'rsds':
            _clm_var *= 0.0864 
        if _var == 'tasmax':
            _clm_var -= 273.15
        if _var == 'tasmin':
            _clm_var -= 273.15
        if _var == 'wind':
            _clm_var *= 3.6 * 24 
       
        #print _clm_var.shape, np.array(datelist(_begin_day, _end_day)).shape 
        if _clm_var.shape == np.array(datelist(_begin_day, _end_day)).shape: 
            _clm_dic[_var_trans[_var]] = _clm_var.tolist()
            #_datelist = np.column_stack((_datelist,_clm_var))
            #print 'Now processing', _var, _wea_list[_wea], _clm_var.shape
        else:
            print "Attention! climate data days number not the same as date number"
            os.exit()
        f.close()
    print 'Finished reading climate data in %s' % _climate_path

    return _clm_dic


# active accumulated temperature,
# input: _clm_dic dictionary number for one year; output number for one year
def act_temp(_clm_dic, _year, _site_path = './'):
    _tmean = []
    for i in xrange(len(_clm_dic['TMAX'])):
        _tmean.append((_clm_dic['TMAX'][i] + _clm_dic['TMIN'][i]) / 2)
    
    # find index where tmean is lower than 10C
    _index_list = []
    _index_list.append(0)
    for i in xrange(len(_tmean)):
        if _tmean[i] < 10.0:
            _index_list.append(i)
    if isLeapYear(_year):
        _index_list.append(366)
    else:
        _index_list.append(365)

    # cal every act acc temp and find the max one, the max one which is act acc temp
    _act_temp_list = []
    act_acc_temp_begin_list = []
    act_acc_temp_end_list = []
    for i in xrange(len(_index_list) - 1):
        if _index_list[i+1] - _index_list[i] > 30:
            _act_temp_list.append(sum(_tmean[_index_list[i]:_index_list[i+1]]))
            act_acc_temp_begin_list.append(_index_list[i])
            act_acc_temp_end_list.append(_index_list[i+1])
    act_acc_temp = max(_act_temp_list)
    act_acc_temp_begin = act_acc_temp_begin_list[_act_temp_list.index(max(_act_temp_list))]
    act_acc_temp_end = act_acc_temp_end_list[_act_temp_list.index(max(_act_temp_list))]

    # write act acc temp to another file
    with open (_site_path + 'act_temp.csv', 'a') as fo:
        fo.write('%d, %s, %s, %s \r\n' % (_year, act_acc_temp, act_acc_temp_begin, act_acc_temp_end))

    return act_acc_temp, act_acc_temp_begin, act_acc_temp_end



def write_clm(_lat_in, _lon_in, _year, _clm_dic, _site_name, _site_path):
    # generally weather data contain 
    # hur, hurtmax, pr,     rsds, tas, tasmax, tasmin, wind
    #               RAIN,   SRAD,      TMAX,   TMIN,   WIND
    ls = []
    ls.append('*WEATHER : %s, CHINA, QING' % _site_name)
    ls.append(' ')
    ls.append('@ INSI      LAT     LONG  ELEV   TAV   AMP REFHT WNDHT')
    ls.append('  %s   %6.3f  %7.3f    9   16.5  10.3  2.00  2.00' % (_site_name[0:4], _lat_in, _lon_in))
    ls.append(' ')
    
    _sorted_var= '@'   
    for i in sorted(_clm_dic.keys()):
        _sorted_var += '%s  ' % i
    ls.append(_sorted_var) 
    
    # Create JDZ 2013 CK Tmax 30 C, Tmin 25 C from 13180 to 13220. 
    # Generally, JDZ 13198 was grain filling begin Maturity date: 13211
    #_modify_clim_index_bg = _datelist[:, 0].tolist().index(13193)
    #_modify_clim_index_ed = _datelist[:, 0].tolist().index(13211)
    ##print 'Now generate CK climate data. index from: ', _modify_clim_index_bg, 'to', _modify_clim_index_ed
    #for i in xrange(_modify_clim_index_bg, _modify_clim_index_ed):
    #    _datelist[i, 3] = 30.0
    #    _datelist[i, 4] = 25.0 

    # write to ascii file
    for i in xrange(len(_clm_dic['DATE'])):
        if  _clm_dic['RAIN'][i] is None:
            _clm_dic['RAIN'][i] = _clm_dic['RAIN'][i-1]
        if  _clm_dic['SRAD'][i] is None:
            _clm_dic['SRAD'][i] = _clm_dic['SRAD'][i-1]
        if  _clm_dic['TMAX'][i] is None:
            _clm_dic['TMAX'][i] = _clm_dic['TMAX'][i-1]
        if  _clm_dic['TMIN'][i] is None:
            _clm_dic['TMIN'][i] = _clm_dic['TMIN'][i-1]
        if  _clm_dic['WIND'][i] is None:
            _clm_dic['WIND'][i] = _clm_dic['WIND'][i-1]
        ls.append('%s%6.1f%6.1f%6.1f%6.1f%6.1f' % (_clm_dic['DATE'][i], _clm_dic['RAIN'][i], _clm_dic['SRAD'][i], _clm_dic['TMAX'][i], _clm_dic['TMIN'][i], _clm_dic['WIND'][i]))

    fname = _site_path + _site_name + '.WTH'
    with open(fname,'w') as fo:
        fo.write('\r\n'.join(ls))

    print 'Finished write %s.WTH in %s' % (_site_name, _site_path)


'''
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
'''


