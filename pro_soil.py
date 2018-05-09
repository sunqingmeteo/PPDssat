# coding=utf-8
import os, subprocess
import numpy as np

def write_soil(_lat_in, _lon_in, _name_AAAA, _run_path, _site_path):
    with open ('./CHINA_SoilGrids.SOL') as fi:
        _soil = fi.readlines()
 
    # find all line contain "-99 CN"
    _listlatlon = []
    for i in xrange(len(_soil)):
        if ' -99              CN' in _soil[i]:
            _listlatlon.append(_soil[i])

    # test if have duplicate value in list
    #if [True,False][_listlatlon==list(set(_listlatlon))] == True:
    #    print 'Attention! Have duplicate _soil file!'
    #myset = set(_listlatlon)
    # find duplicates very slow of this loop
    #for item in myset:
    #    if _listlatlon.count(item) > 1:
    #        print("the %d has found %d" %(item, _listlatlon.count(item)))

    # lat & lon value
    _lat = []
    _lon = []
    for i in _listlatlon:
        alat = i.split()
        _lat.append(alat[2])
        _lon.append(alat[3])

    # find nearest lat and lon, note: numpy array did not have 'index' command, must convert to list
    _lat_abs = []
    _lon_abs = []
    for i in xrange(len(_lat)):
        _lat_abs.append(abs(float(_lat[i]) - _lat_in))
        _lon_abs.append(abs(float(_lon[i]) - _lon_in))
    _sum_lat_lon = []
    for i in xrange(len(_lat_abs)):
        _sum_lat_lon.append(_lon_abs[i] + _lat_abs[i])
    _latlon_index = _sum_lat_lon.index(min(_sum_lat_lon))
    #print 'The nearest lat and lon index:', _latlon_index, 'lat:', _lat[_latlon_index], 'lon:', _lon[_latlon_index]
    
    #lat
    _find_list = list(_soil[2])
    for i in xrange(len(_soil)):
        if '%s  %s' % (str(_lat[_latlon_index]), str(_lon[_latlon_index])) in _soil[i]:
            _find_str = _soil[i]

    _site_soil_index = _soil.index(_find_str)
    _site_soil = _soil[(_site_soil_index - 2):(_site_soil_index + 9)]

    _site_soil_name = _site_soil[0].split(' ')[0]
    subprocess.call(' ln -sf %sCHINA_SoilGrids.SOL %s/CN.SOL' % (_run_path, _site_path), shell = True)
    print 'Find soil name: %s and linked to %s' % (_site_soil_name[1:], _site_path)

    return _site_soil_name[1:]



    '''
    # write lat lon list to csv
    ls = []
    for _row in xrange(len(_listlatlon)):
        ls.append('%s,' % _listlatlon[_row])
    with open ('./listlatlon.csv','w') as fo:
        fo.write(','.join(ls))
    '''

    '''
    ls =[]
    for i in xrange(len(_site_soil)):
        ls.append(_site_soil[i])
    _line_1_list = list(ls[0])
    print _line_1_list, list(_name_AAAA)
    for i in xrange(len(list(_name_AAAA))):
        _line_1_list[i+1] = list(_name_AAAA)[i]
    ls[0] = ''.join(_line_1_list)

    _fname = _name_AAAA[0:1] + '.SOL'
    with open (_site_path + _fname, 'w') as fo:
        fo.write(''.join(ls))

    print 'Finished create %s in %s' % (_fname, _site_path)
    '''

'''
# JDZ & NJ lat lon
_lat_jdz =  29.18
_lon_jdz = 117.12
_lat_nj =  32.00
_lon_nj = 118.29

# CHINA_SoilGrids.SOL each grid have 13 lines
write_soil(_lat_jdz, _lon_jdz, 'CN.SOL')
'''






