# coding=utf-8
from netCDF4 import Dataset
import numpy as np
import time
import calendar
import pandas as pd
from datetime import datetime

def datelist(beginDate, endDate):
# beginDate, endDate is '20160601', must add '', is string
    date_l=[datetime.strftime(x,'%y%j') for x in list(pd.date_range(start=beginDate, end=endDate))]
    return date_l


# not use 'hur_agmerra_1980-2010.nc4', 'tas_agmerra_1980-2010.nc4', 'hurtmax_agmerra_1980-2010.nc4'
wea_list = ['pr_agmerra_1980-2010.nc4',     \
            'rsds_agmerra_1980-2010.nc4',   \
            'tasmax_agmerra_1980-2010.nc4', \
            'tasmin_agmerra_1980-2010.nc4', \
            'wind_agmerra_1980-2010.nc4']

# lon is x 720, lat is y 360
f1 = Dataset('pr_agmerra_1980-2010.nc4','r')
lat = f1.variables['lat'][:]
lon = f1.variables['lon'][:]
# print lat.shape, type(lat)

# JDZ lat lon
_lat1 = 29.180
_lon1 = 117.12

# find nearest lat and lon
_latabs = abs(lat - _lat1)
# numpy array did not have 'index' command, must convert to list
_latindex = _latabs.tolist().index(min(abs(_latabs)))
# print _latindex, lat[_latindex]
_lonabs = abs(lon - _lon1)
_lonindex = _lonabs.tolist().index(min(abs(_lonabs)))
# print _lonindex, lon[_lonindex]


# create time series,  Gregorian date -> Julian date
# _datelist is 'list', need to convert to array then can print .shape
_datelist = datelist('19800101', '20101231')
_datelist = np.array(_datelist)
print 'Date list:', _datelist, _datelist.shape
# _yearnum = _datelist.strftime('%y')   # last two string of year
#                              ('%j')   # day number in the year


# weather var from climate data
# _cli [col, row] _cli = [ [0 for i in xrange(len(wea_list))] for i in xrange(len(_datelist)) ]
#_cli = np.zeros((_datelist.shape,len(wea_list)+1))
#print '_cli.shape:', _cli.shape
#_cli(:, 0) = _datelist(:,0)
for _wea in xrange(len(wea_list)):
    f = Dataset(wea_list[_wea], 'r')
    # exact first strings before '_'
    _var = wea_list[_wea][0:wea_list[_wea].rfind('_', 0, 10)]
    _cli = f.variables[_var][:, _latindex, _lonindex]
    _datelist = np.column_stack((_datelist,_cli))
    print 'Now processing', _var, wea_list[_wea], _cli.shape
print '_datelist', _datelist.shape, type(_datelist)


# UNIT transfer
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


# each lat each lon need write a single file. name rule: IRJD1301.WTH
ls = []
ls.append('*WEATHER : IRJD, CHINA, QING')
ls.append(' ')
ls.append('@ INSI      LAT     LONG  ELEV   TAV   AMP REFHT WNDHT')
ls.append('  IRPI   32.000   118.29    9   16.5  10.3  2.00  2.00')
ls.append(' ')
ls.append('@DATE  RAIN  SRAD  TMAX  TMIN  WIND')
# generally weather data contain 
# hur, hurtmax, pr,     rsds, tas, tasmax, tasmin, wind
#               RAIN,   SRAD,      TMAX,   TMIN,   WIND                                     

# write to ascii file
for _row in xrange(_datelist.shape[0]):
    lt = []
    for _col in xrange(_datelist.shape[1]):
        if _col == 0:
            lt.append('%05d' % _datelist[_row,_col])
        else:
            lt.append('%6.1f' % _datelist[_row,_col])
    ls.append(''.join(lt))
with open('./IRJD8001.WTH','w') as fo:
    fo.write('\r\n'.join(ls))


'''
# NCL script
header  = (/"*WEATHER : IRJD, CHINA, QING",""/)
hlist   = [/header/]

header1 = (/"@ INSI      LAT     LONG  ELEV   TAV   AMP REFHT WNDHT"/)
hlist1  = [/header1/]

header2 = (/"  IRPI   32.000   118.29    9   16.5  10.3  2.00  2.00"/)
hlist2  = [/header2/]

write_table("IRJD1301.WTH", "w", hlist,  "%s")
write_table("IRJD1301.WTH", "a", hlist1, "%s")
write_table("IRJD1301.WTH", "a", hlist2, "%s")
write_table("IRJD1301.WTH", "a", [/""/], "%s")
write_table("IRJD1301.WTH", "a", [/"@DATE","SRAD","TMAX","TMIN","RAIN"/], "%s  %s  %s  %s  %s")
write_table("IRJD1301.WTH", "a", [/f_date, f_srad, f_tmax, f_tmin, f_rain/], "%5.0f%5.1f%5.1f%5.1f%5.1f")


'''



