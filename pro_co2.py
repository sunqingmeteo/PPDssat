#coding=utf-8
# QING SUN/NUIST
import numpy as np

def read_co2(_year, _file_path = './', CO2_RCP='RCP2.6'):
    # year 1980-2099
    # first line is title
    co2 = np.loadtxt(_file_path + '/CO2_RCP.csv', dtype=np.float, delimiter=",", skiprows=1)
    co2_dic = {}
    co2_dic['YEAR']   = co2[:,0]
    co2_dic['RCP2.6'] = co2[:,1]
    co2_dic['RCP4.5'] = co2[:,2]
    co2_dic['RCP6.0'] = co2[:,3]
    co2_dic['RCP8.5'] = co2[:,4]

    co2_out = co2_dic[CO2_RCP][_year-1980]

    return co2_out


if __name__ == '__main__':
    _co2_path = '/Users/qingsun/GGCM/mask_rice/'
    co2 = read_co2(1980, _co2_path, CO2_RCP='RCP2.6')
    print co2

