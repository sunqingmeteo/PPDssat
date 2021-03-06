# coding=utf-8
# QING SUN/NUIST 2019.03.01
# Main code for serial PPDssat
import os, sys, re, subprocess
import numpy as np

from pro_cli_to_dssat import clm_list, read_clm, write_clm, act_temp
from pro_soil import write_soil
from pro_rix import write_rix
from pro_batch import write_batch
from pro_mask import rice_area_mask, rice_gene_mask
from post_dssat import read_dirs, read_summary, write_nc


# Create single grid path name
def create_name(_latloni, _gen_path = './'):
    #_latloni is number, return is str like 'AAAA'
    _gen_path = os.getcwd() + '/'
    _words = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    aaa = []
    for i in xrange(len(_words)):
        for j in xrange(len(_words)):
            for k in xrange(len(_words)):
                for l in xrange(len(_words)):
                    aaa.append(_words[i]+_words[j] + _words[k] + _words[l])

    _path_full = _gen_path + aaa[_latloni]
    if os.path.exists(_path_full):
        #_file_exsit = raw_input("Already have path: %s! Want to rewrite? y/n: " % _path_full)
        #if _file_exsit == 'y' or _file_exsit == 'Y':
        subprocess.call('rm -rf ' + _path_full, shell = True)
    os.mkdir(_path_full)
    return aaa[_latloni]


def run_dssat_main(_lat_lon, _gene_region, plantday, co2,
                   _begin_year, _end_year, 
                   _climate_path='./', _run_path='./',
                   _dssat_exe='./',    _mask_path='./', _co2_path='./'):

    # Loop each point
    for _latloni in xrange(len(_lat_lon)):
    #for _latloni in xrange(1585,len(_lat_lon)):
        # _lat_lon are list, _lat_lon [lat,lon], _clm_dic is dictionary
        
        # Debug
        #_latloni = 1001

        # Enter run path
        os.chdir(_run_path)

        # create path name
        _name_AAAA = create_name(_latloni)
        _site_path = _run_path + _name_AAAA + '/'

        _lat_in = _lat_lon[_latloni][0]
        _lon_in = _lat_lon[_latloni][1]

        plant_day = plantday[_latloni]
        gene_region = _gene_region[_latloni]

        # write .SOL
        _soil_name = write_soil(_lat_in, _lon_in, _name_AAAA, _run_path, _site_path)

        # create act acc temp file
        #with open (_site_path + 'act_temp.csv', 'a') as fi:
            #fi.write('year, act_acc_temp, act_acc_temp_begin, act_acc_temp_end \r\n')

        _rix_list = []
        # Loop year for .WTH
        for _year in xrange(_begin_year, _end_year+1):
            print 'NOW PROCESSING GRID: %s, YEAR: %s' % (_latloni, _year)
            _list_year = list(str(_year))
            _last_two_num = str(_list_year[2]) + str(_list_year[3])
            _site_name = _name_AAAA + _last_two_num + '01'

            # Find clm list
            _wea_list = clm_list(_year, _climate_path)
            #print _wea_list

            # Read clm vars
            _clm_dic = read_clm(_lat_in, _lon_in, _year, _wea_list, _climate_path)

            # Cal active accumulated temperature, if act_acc_temp less then 5300, next loop
            #act_acc_temp, act_acc_temp_begin, act_acc_temp_end = act_temp(_clm_dic, _year, _site_path)

            # Write clm vars .WTH
            write_clm(_lat_in, _lon_in, _year, co2, _clm_dic, _site_name, _site_path, _co2_path)

            #write .RIX
            _rix_name = write_rix(_year=_year, plant_day=plant_day, gene_region=gene_region, 
                                  _site_name=_site_name, _soil_name=_soil_name, 
                                  _site_path=_site_path, _run_path=_run_path)
            
            _rix_list.append(_rix_name)
        print 'Finished writing all files year between %s and %s.' % (_begin_year, _end_year)
            
        #write DSSBatch.v47
        write_batch(_site_path)

        #link some needed files and run dssat
        _ln_dssat_exe           = subprocess.call('ln -sf %s/dscsm047.exe %s/.' % (_dssat_exe_path, _site_path),                shell=True)
        _ln_dssat_linux         = subprocess.call('ln -sf %s/DSSATPRO.L47 %s/.' % (_run_path, _site_path),                      shell=True)
        _ln_rice_gene           = subprocess.call('ln -sf %s/RICER047.CUL %s' % (_run_path, _site_path),                        shell=True)
        _ln_dssat_model_err     = subprocess.call('ln -sf %s../..//Data/MODEL.ERR %s/.' % (_dssat_exe_path, _site_path),        shell=True)
        _ln_dssat_cde           = subprocess.call('ln -sf %s../../Data/*CDE %s/.' % (_dssat_exe_path, _site_path),              shell=True)
        #print 'Finished linking all files DSSAT needs.'

        # RUN
        _run_dssat              = subprocess.call('cd %s; ./dscsm047.exe RICER047 B DSSBatch.v47' % _site_path,                 shell=True)
        
        #os.exit()

        
if __name__ == '__main__':

    ##### LETS ROCK !!! #####

    # Setting path for PPDssat
    # For NUIST server
    #_climate_path   = '/nuist/u/home/yangzaiqiang/work/RE-ANA-CLM/AgCFSR/'
    _climate_path   = '/nuist/u/home/yangzaiqiang/work/CMIP5/GFDL/rcp2p6/'
    _run_path       = '/nuist/u/home/yangzaiqiang/scratch/run_dssat/'
    _dssat_exe_path = '/nuist/u/home/yangzaiqiang/dssat-csm/Build/bin/'
    _mask_path      = '/nuist/u/home/yangzaiqiang/work/mask_rice/'
    _co2_path       = '/nuist/u/home/yangzaiqiang/work/mask_rice/'

    # For local
    #_climate_path   = '/Users/qingsun/GGCM/run_dssat/GFDL_RCP2.6/'
    #_run_path       = '/Users/qingsun/GGCM/run_dssat/'
    #_dssat_exe_path = '/Users/qingsun/GGCM/dssat-csm/build/bin/'
    #_mask_path      = '/Users/qingsun/GGCM/mask_rice/'
    #_co2_path       = '/Users/qingsun/GGCM/mask_rice/'

    # CO2_RCP == 'FIX' = 380
    #CO2_RCP = ['RCP2.6', 'RCP4.5', 'RCP6.0', 'RCP8.5', 'FIX']
    CO2_RCP = 'RCP2.6'

    #plantpk = ['PK1', 'PK2', 'PK3']
    plantpk = 'PK1'

    run_begin_year = 2020
    run_end_year   = 2099

    ################## SETTING ABOVE ##########################


    # Read mask for lat and lon
    # Mask should be change flexible
    _lat_lon, _gene_region, plantday = rice_gene_mask(_mask_path, plantpk)

    # run main loop
    run_dssat_main(_lat_lon = _lat_lon, _gene_region = _gene_region, plantday = plantday, co2=CO2_RCP,
                   _begin_year = run_begin_year, _end_year = run_end_year, 
                   _climate_path =_climate_path, _run_path = _run_path, 
                   _dssat_exe = _dssat_exe_path, _mask_path=_mask_path, _co2_path=_co2_path)

    
    # Post process Summary.out
    # Using file: post_dssat.py
    dirs = read_dirs(_run_path)
    print 'Total pathes is %s' % (len(dirs))
    if len(dirs) == 1595:
        plantpk = 'PK1'
    elif len(dirs) == 826:
        plantpk = 'PK2'
    elif len(dirs) == 695:
        plantpk = 'PK3'
    else:
        print 'Grid number is not same as any Plant Peak number!'
        os.exit()

    _out_dssat = read_summary(_lat_lon, dirs)

    output_file_name = 'PPDSSAT_OUT_%s_%s_%s_%s.nc' % (CO2_RCP, plantpk, run_begin_year, run_end_year)
    write_nc(_out_dssat, mask_path, run_path, output_file_name)



