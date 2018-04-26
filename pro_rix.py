#coding=utf-8

# random fname word <====> fixed lat and lon
# _year & _site_name -> from climate data input file
def write_rix(_year, _site_name, _soil_name, _site_path):
    _rix_name      = _site_name + '.RIX' # file name

    # open file, _in_dssat is list and each element is str
    with open ('/Users/qingsun/GGCM/run_dssat/EXAMPLE_RICE.RIX') as fi:
        _in_dssat = fi.readlines()

    # begin to mofidy .RIX
    _in_dssat[0]   = '*EXP.DETAILS: ' + _site_name + 'RI CHINA QING/NUIST \r\n'
    _in_dssat[8]   = _site_name + '\r\n'
    _in_dssat[22]  = ' 1 %s0001 %s   -99     0 DR000     0     0 00000 L      200  %s UNKNOWN\r\n' % (_site_name[0:4], _site_name, _soil_name)
    _in_dssat[28]  = ' 1 ' + str(_year)[-2:] + '001   -99   -99   -99  -99\r\n'
    _in_dssat[34]  = ' 1    RI ' + str(_year)[-2:] + '089   300   -99     1     1   -99     0     0     0   100    15 UNKNOWN\r\n'
    _in_dssat[49]  = ' 1 %s092 %s099   999   125     T     H    26     0     5     0    48    23     5     0                        test1\r\n' % (str(_year)[-2:], str(_year)[-2:])
    _in_dssat[55]  = ' 1 ' + str(_year)[-2:] + '171 IR003    40\r\n'
    _in_dssat[56]  = ' 1 ' + str(_year)[-2:] + '185 IR003    60\r\n'
    _in_dssat[57]  = ' 1 ' + str(_year)[-2:] + '199 IR003    20\r\n'
    _in_dssat[58]  = ' 1 ' + str(_year)[-2:] + '222 IR003    20\r\n'
    _in_dssat[59]  = ' 1 ' + str(_year)[-2:] + '229 IR003    40\r\n'
    _in_dssat[60]  = ' 1 ' + str(_year)[-2:] + '254 IR003    60\r\n'
    _in_dssat[64]  = ' 1 ' + str(_year)[-2:] + '141 FE005 AP018     1   104    90    90   -99   -99   -99 -99\r\n'
    _in_dssat[65]  = ' 1 ' + str(_year)[-2:] + '147 FE005 AP018     1    81   -99   -99   -99   -99   -99 -99\r\n'
    _in_dssat[66]  = ' 1 ' + str(_year)[-2:] + '176 FE005 AP018     1    81   -99    90   -99   -99   -99 -99\r\n'
    _in_dssat[70]  = ' 1 ' + str(_year)[-2:] + '001   -99   -99   -99   -99   -99   -99   -99   -99 -99\r\n'
    _in_dssat[74]  = ' 1 ' + str(_year)[-2:] + '001   -99   -99 -99\r\n'
    _in_dssat[78]  = ' 1 ' + str(_year)[-2:] + '001 A   0 A   0 A   0 A   0 A 0.0 A   0 A   0 A   0 \r\n'
    _in_dssat[82]  = ' 1 ' + str(_year)[-2:] + '211 GS014     H     A   -99   -99 Rice\r\n'
    _in_dssat[86]  = ' 1 GE              1     1     S ' + str(_year)[-2:] + '001  2150 CERES-RICE JDZ, QING      RICER\r\n'
    _in_dssat[98]  = ' 1 PL          ' + str(_year)[-2:] + '001 ' + str(_year)[-2:] + '364    40   100    30    40    10\r\n'
    _in_dssat[106] = ' 1 HA              0 ' + str(_year)[-2:] + '360   100     0\r\n'

    # output RIX files
    with open (_site_path + _rix_name, 'w') as fo:
        fo.write(''.join(_in_dssat))

    print 'Finished RIX file %s in %s' % (_rix_name, _site_path)

    return _rix_name

