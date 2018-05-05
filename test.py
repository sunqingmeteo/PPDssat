# coding=utf-8
from netCDF4 import Dataset
import numpy as np
import os
'''
f = Dataset('/Users/qingsun/GGCM/run_dssat/GFDL_RCP2.6/pr_bced_1960_1999_gfdl-esm2m_historical_1951-1960.nc4', 'r')
    # exact first strings before '_' as variable name
_time = f.variables['time'][:]
_nctime_bg = 33237
_nctime_ed = 33240
_nctime_bg_index = int(np.where(_time == _nctime_bg)[0])
_nctime_ed_index = int(np.where(_time == _nctime_ed)[0])
_cli = f.variables['pr'][_nctime_bg_index:_nctime_ed_index, :, :]

print _cli.shape, _nctime_bg_index, _nctime_ed_index
'''



'''
a = os.getcwd()
print a, type(a)


def create_name(_latloni, _gen_path = './'):
    _gen_path = os.getcwd()
    #_latloni is number
    _words = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    aaa = []
    for i in xrange(len(_words)):
        for j in xrange(len(_words)):
            for k in xrange(len(_words)):
                for l in xrange(len(_words)):
                    aaa.append(_words[i]+_words[j] + _words[k] + _words[l])
    _name = aaa[_latloni]
    os.mkdir(_gen_path + '/' + _name)


_latloni = 3
create_name(_latloni)
'''


year = 1980

a = list(str(year))
b = str(a[2])+str(a[3])
print b
