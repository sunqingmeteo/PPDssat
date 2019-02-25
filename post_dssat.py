# coding=utf-8
import os, datetime
import numpy as np 
from netCDF4 import Dataset
from pro_mask import rice_gene_mask


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
    # output: dssat_out_nc,  Data structure: dict, dic['variables'][year][grid]
    #                 each element is one grid in _out_dssat is dictonrary

    dssat_out_nc = {}

    # Loop each dirs, each point
    for dirs_i in xrange(len(_dirs)):
        
        print 'Reading Summary.OUT from directory %s' % _dirs[dirs_i]

        # read summary.out
        try:
            with open(_dirs[dirs_i] + '/Summary.OUT', 'r') as fi:
                summary = fi.readlines()

            # each grid have lat, lon, area, and all year, all yield
            _name_gird_dic = {}

            # Start from SDAT, No.13
            station_name = '%s' % summary[4].split()[7][0:4]
            dssat_out_nc[station_name] = {}
            summary_var_names = summary[3].split()[13:]
            #print len(summary_var_names),summary_var_names

            dssat_out_nc[station_name]['LAT'] = _lat_lon[dirs_i][0]
            dssat_out_nc[station_name]['LON'] = _lat_lon[dirs_i][1]

            for i in xrange(len(summary)-4):
                # Start from SDAT, No.12, [102:106]]=year
                _name_gird_dic[summary[i+4][102:106]] = summary[i+4].split()[12:]                                              
                # in some situation, rice will harvest next year even set last harvest date
                if summary[i+4][102:106] != summary[i+4][126:130]:
                    _name_gird_dic[summary[i+4][102:106]][15] = 0   # ADAT
                    _name_gird_dic[summary[i+4][102:106]][16] = 0   # MDAT
                    _name_gird_dic[summary[i+4][102:106]][20] = 0   # HWAM

            # Start from col 12 SDAT to lat, all are numbers, create blank dic and list 
            
            for _vars in xrange(len(summary_var_names)):            
                dssat_out_nc[station_name][summary_var_names[_vars]] = {}
                for _year in sorted(_name_gird_dic.keys()):
                    if _year.isdigit():
                        dssat_out_nc[station_name][summary_var_names[_vars]][_year] = []
                        #print _year

            dssat_out_nc[station_name]['YEAR'] = []
            for _year in sorted(_name_gird_dic.keys()):
                if _year.isdigit():
                    dssat_out_nc[station_name]['YEAR'].append(_year)
                    # Start from col 12 SDAT to lat, all are numbers
                    for _vars in xrange(len(summary_var_names)):
                        if summary_var_names[_vars] in ['SDAT', 'ADAT', 'PDAT', 'EDAT', 'MDAT', 'HDAT']:
                            dssat_out_nc[station_name][summary_var_names[_vars]][_year].append(round(float(_name_gird_dic[_year][_vars][-3:]),4))
                        else:
                            dssat_out_nc[station_name][summary_var_names[_vars]][_year].append(round(float(_name_gird_dic[_year][_vars]),4))
                    
            # read accumulative active temperature, already sorted by year
            #aat = np.loadtxt(_dirs[dirs_i] + '/act_temp.csv', dtype=np.str, delimiter=",", skiprows=1)
            #aat_list = aat[:,1].tolist()
            #for k in xrange(len(aat_list)):
            #    dssat_out_nc['AAT'].append(round(float(aat_list[k]),2))
        except:
            with open(_dirs[0] + '/Summary.OUT', 'r') as fi:
                summary = fi.readlines()

            # each grid have lat, lon, area, and all year, all yield
            _name_gird_dic = {}

            # Start from SDAT, No.13
            station_name = '%s' % summary[4].split()[7][0:4]
            dssat_out_nc[station_name] = {}
            summary_var_names = summary[3].split()[13:]
            #print len(summary_var_names),summary_var_names

            dssat_out_nc[station_name]['LAT'] = _lat_lon[dirs_i][0]
            dssat_out_nc[station_name]['LON'] = _lat_lon[dirs_i][1]

            for i in xrange(len(summary)-4):
                # Start from SDAT, No.12, [102:106]]=year
                _name_gird_dic[summary[i+4][102:106]] = summary[i+4].split()[12:]                                              
                # in some situation, rice will harvest next year even set last harvest date
                if summary[i+4][102:106] != summary[i+4][126:130]:
                    _name_gird_dic[summary[i+4][102:106]][15] = 0   # ADAT
                    _name_gird_dic[summary[i+4][102:106]][16] = 0   # MDAT
                    _name_gird_dic[summary[i+4][102:106]][20] = 0   # HWAM

            # Start from col 12 SDAT to lat, all are numbers, create blank dic and list 
            
            for _vars in xrange(len(summary_var_names)):            
                dssat_out_nc[station_name][summary_var_names[_vars]] = {}
                for _year in sorted(_name_gird_dic.keys()):
                    if _year.isdigit():
                        dssat_out_nc[station_name][summary_var_names[_vars]][_year] = []
                        #print _year

            dssat_out_nc[station_name]['YEAR'] = []
            for _year in sorted(_name_gird_dic.keys()):
                if _year.isdigit():
                    dssat_out_nc[station_name]['YEAR'].append(_year)
                    # Start from col 12 SDAT to lat, all are numbers
                    for _vars in xrange(len(summary_var_names)):
                        if summary_var_names[_vars] in ['SDAT', 'ADAT', 'PDAT', 'EDAT', 'MDAT', 'HDAT']:
                            dssat_out_nc[station_name][summary_var_names[_vars]][_year].append(round(float(_name_gird_dic[_year][_vars][-3:]),4))
                        else:
                            dssat_out_nc[station_name][summary_var_names[_vars]][_year].append(round(float(_name_gird_dic[_year][_vars]),4))
                    
            # read accumulative active temperature, already sorted by year
            #aat = np.loadtxt(_dirs[dirs_i] + '/act_temp.csv', dtype=np.str, delimiter=",", skiprows=1)
            #aat_list = aat[:,1].tolist()
            #for k in xrange(len(aat_list)):
            #    dssat_out_nc['AAT'].append(round(float(aat_list[k]),2))


    return dssat_out_nc


def write_nc(dssat_out_nc, _mask_path = './', _file_path='./', output_file_name = 'DSSAT_outputs.nc'):
    # Input: dssat_out_nc,  Data structure: dict, dic['variables'][year][grid]

    # Open mask file to get useful variables
    f_area = Dataset(_mask_path + '/Rice_gene_region.nc', 'r')
    _lat_mask = f_area.variables['lat'][:]
    _lon_mask = f_area.variables['lon'][:]
    _mask_in = f_area.variables['region'][:]  # 58 * 76 
    f_area.close()
    
    # Create nc file
    f_nc = Dataset(_file_path + '/' + output_file_name, 'w', format = 'NETCDF4_CLASSIC')
    lat =  f_nc.createDimension('lat',  len(_lat_mask))
    lon =  f_nc.createDimension('lon',  len(_lon_mask))
    time = f_nc.createDimension('time', len(dssat_out_nc['AABB']['YEAR']))

    lats = f_nc.createVariable('lat',  'f',  ('lat',))
    lons = f_nc.createVariable('lon',  'f',  ('lon',))
    times = f_nc.createVariable('time', 'i4', ('time',))

    # NC file input transfer, from station-var-year data to var-year-region(lat, lon)
    _input_nc = {}
    _vars = sorted(dssat_out_nc['AABB'].keys())

    for _vars_num in xrange(len(_vars)):
        
        if _vars[_vars_num] not in ['LAT', 'LON', 'YEAR']: 
            
            print 'Transfering variable: %s' % _vars[_vars_num]
            
            # Create array with 1.0e20
            f_nc.createVariable(_vars[_vars_num], np.float32, dimensions=('time', 'lat', 'lon',), fill_value=1.0e20)
            _empty_array = np.empty((len(dssat_out_nc['AABB']['YEAR']), _mask_in.shape[0],_mask_in.shape[1]), dtype=np.float32)
            _empty_array.fill(1.0e20)

            for stations in sorted(dssat_out_nc.keys()):

                # Find station lat and lon index to find the position of input_nc array 
                _lat_index = _lat_mask.tolist().index(dssat_out_nc[stations]['LAT'])
                _lon_index = _lon_mask.tolist().index(dssat_out_nc[stations]['LON']) 

                #print sorted(dssat_out_nc[stations][_vars[_vars_num]])
                for _year_num in sorted(dssat_out_nc[stations][_vars[_vars_num]]):

                    #print _year_num
                    #print _vars[_vars_num],sorted(dssat_out_nc[stations][_vars[_vars_num]].keys()),_year_num
                    #print dssat_out_nc[stations][_vars[_vars_num]][_year_num]
                    _year_begin = sorted(dssat_out_nc[stations][_vars[_vars_num]].keys())[0]
                    #print _year_begin,dssat_out_nc[stations][_vars[_vars_num]][_year_num]
                    #print type(_year_num),type(dssat_out_nc[stations][_vars[_vars_num]][_year_num][0])
                    #print int(_year_num) - int(_year_begin), _lat_index, _lon_index
                    _empty_array[int(_year_num) - int(_year_begin), _lat_index, _lon_index] = dssat_out_nc[stations][_vars[_vars_num]][_year_num][0]

            _input_nc[_vars[_vars_num]] = _empty_array

    # Write variables to nc file
    f_nc.variables['lat'][:] = _lat_mask
    f_nc.variables['lon'][:] = _lon_mask
    f_nc.variables['time'][:] = np.array(sorted(dssat_out_nc['AABB']['SDAT'].keys()))
    for _vars_out in sorted(_input_nc.keys()):
        f_nc.variables[_vars_out][:] = _input_nc[_vars_out]

    # Global Attributes
    f_nc.description = 'Qing Sun, NUIST, created in %s' % datetime.datetime.now()
    f_nc.source = 'AgMIP climate datasets, PPDSSAT results, https://github.com/sunqingmeteo/PPDssat'

    # Variable Attributes
    times.units = "year"
    times.long_name = "time"
    lats.units = 'degree_north'
    lats.long_name = "latitude"
    lons.units = 'degree_east'
    lons.long_name = "longitude"

    f_nc.close()
   

#######################################################################################
if __name__ == '__main__':

    ##### For NUIST server
    #mask_path = '/nuist/u/home/yangzaiqiang/work/mask_rice/'
    #run_path  = '/nuist/u/home/yangzaiqiang/scratch/run_dssat/'

    ##### For local run
    mask_path = '/Users/qingsun/GGCM/mask_rice/'
    run_path = '/Users/qingsun/GGCM/run_dssat/'
    #dirs = ['/Users/qingsun/Desktop/']

    dirs = read_dirs(run_path)
    print len(dirs)
    

    _lat_lon, _gene_region, plant1, plant2, plant3 = rice_gene_mask(mask_path)


    _out_dssat = read_summary(_lat_lon, dirs)


    output_file_name = 'PPDSSAT_OUT.nc'
    write_nc(_out_dssat, mask_path, run_path, output_file_name)





