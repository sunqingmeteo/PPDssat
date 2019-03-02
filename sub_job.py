# coding=utf-8
# QING SUN/NUIST 2019.03.01
# Submit job for PPDssat
import os, sys, re, subprocess
import numpy as np

def string_switch(filename, original_str, target_str,s=1):
    # s = 1 is only replace first origin_str
    # s = g is replace all origin_str in file
    with open(filename, "r") as f:
        lines = f.readlines()
 
    with open(filename, "w") as f_w:
        n = 0
        if s == 1:
            for line in lines:
                if original_str in line:
                    line = line.replace(original_str,target_str)
                    f_w.write(line)
                    n += 1
                    print 'Modified string to %s' % (target_str)    
                    break
                f_w.write(line)
                n += 1
            for i in range(n,len(lines)):
                f_w.write(lines[i])
        elif s == 'g':
            for line in lines:
                if original_str in line:
                    line = line.replace(original_str,target_str)
                f_w.write(line)


'''
################## SETTING SECTION ###############################
# Setting pathes for PPDssat
# For NUIST server run
_climate_path_base   = '/nuist/u/home/yangzaiqiang/work/CMIP5/GFDL/rcp8p5/'
_run_path_base       = '/nuist/u/home/yangzaiqiang/scratch/run_dssat5/'

#CO2_RCP = ['RCP2.6', 'RCP4.5', 'RCP6.0', 'RCP8.5', 'FIX']
CO2_RCP = 'RCP8.5'

#plantpk = ['PK1', 'PK2', 'PK3']
plantpk = 'PK1'

run_begin_year = 2020
run_end_year   = 2099

_dssat_exe_path = '/nuist/u/home/yangzaiqiang/dssat-csm/Build/bin/'
_mask_path      = '/nuist/u/home/yangzaiqiang/work/mask_rice/'
_co2_path       = '/nuist/u/home/yangzaiqiang/work/mask_rice/'
################## SETTING BEFORE ###############################
'''

if "__main__" == __name__:

    # SETTING 4 vars in run_mpi_dssat.py: _climate_path, _run_path, CO2_RCP, plantpk
    _climate_data_list   = ['GFDL', 'HADGEM', 'IPSL', 'MIROC', 'NORESM']
    _plantpk_list        = ['PK1', 'PK2', 'PK3']
    #_co2_list            = ['RCP2.6', 'RCP4.5', 'RCP6.0', 'RCP8.5', 'FIX']
    _co2_list            = ['RCP2.6', 'RCP4.5', 'RCP6.0', 'RCP8.5']
    _rcps_list           = ['rcp2p6', 'rcp4p5', 'rcp6p0', 'rcp8p5']

    _climate_path = '/nuist/u/home/yangzaiqiang/work/CMIP5/'
    _scrath = '/nuist/u/home/yangzaiqiang/scratch/'
    run_begin_year = 2020
    run_end_year   = 2099

    _climate_data = 'NORESM'
    for _plantpk in _plantpk_list:
        for i in xrange(len(_co2_list)):
        #for _rcps in _rcps_list:

            # Create run path 
            _run_path = '%s/%s_%s_%s_%s_%s' % (_scrath, _climate_data, str.upper(_rcps_list[i]), run_begin_year, run_end_year, _plantpk)
            if os.path.exists(_run_path):
                os.exit("Directory is already exist!!!")
            else:
                os.mkdir(_run_path)
                print 'Create dir %s' % (_run_path)

            # Enter run path
            os.chdir(_run_path)

            _ln_run_dssat = subprocess.call('cp -r /nuist/u/home/yangzaiqiang/scratch/run_dssat/* %s/.' % (_run_path), shell=True)
            _cp_ppdssat   = subprocess.call('cp -r /nuist/u/home/yangzaiqiang/scratch/PPDssat %s/.' % (_run_path), shell=True)
            string_switch('%s/PPDssat/run_mpi_dssat.py' % (_run_path), 
                          "_climate_path   = '/nuist/u/home/yangzaiqiang/work/CMIP5/GFDL/rcp2p6/'", 
                          "_climate_path   = '/nuist/u/home/yangzaiqiang/work/CMIP5/%s/%s/'" % (_climate_data, _rcps_list[i]),
                          )
            string_switch('%s/PPDssat/run_mpi_dssat.py' % (_run_path), 
                          "_run_path       = '/nuist/u/home/yangzaiqiang/scratch/run_dssat/'", 
                          "_run_path       = '%s/'" % (_run_path),
                          )
            string_switch('%s/PPDssat/run_mpi_dssat.py' % (_run_path), 
                          "CO2_RCP = 'RCP2.6'", 
                          "CO2_RCP = '%s'" % (_co2_list[i]),
                          )
            string_switch('%s/PPDssat/run_mpi_dssat.py' % (_run_path), 
                          "plantpk = 'PK1'", 
                          "plantpk = '%s'" % (_plantpk),
                          )

            # Create job script and submit it.
            job_content = ['#!/bin/bash\n',
                           '\n',
                           '#PBS -N job_PPDSSAT\n',
                           '#PBS -q Longtime\n',
                           '#PBS -l nodes=1:ppn=28\n',
                           '#PBS -l walltime=100:00:00\n',
                           '\n',
                           'cd %s/PPDssat/\n' % (_run_path),
                           'python run_mpi_dssat.py\n',
                           ]

            with open('%s/job_PPDSSAT.sh' % (_run_path), 'w') as f:
                f.writelines(job_content)

            submit_job = subprocess.call('qsub %s/job_PPDSSAT.sh' % (_run_path), shell=True)
            print "Submitted PPDSSAT job of %s" % (_run_path)




