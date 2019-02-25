#coding=utf-8
from netCDF4 import Dataset

def rice_area_mask(_file_path = './'):

    # For south China
    #f_area = Dataset(_file_path + '/rice_mask_cn.nc', 'r')

    # For whole China domain
    f_area = Dataset(_file_path + '/rice_area_cn.nc', 'r')
    _lat_in = f_area.variables['lat'][:]
    _lon_in = f_area.variables['lon'][:]
    _mask_in = f_area.variables['rice_area_cn2'][:]
    f_area.close()

    _lat_lon = []
    for i in xrange(len(_lat_in)):
        for j in xrange(len(_lon_in)):
            if _mask_in[i,j] > 0.0:
                _lat_lon.append([_lat_in[i], _lon_in[j]])
    print 'Total grid number for China domain is %s' % (len(_lat_lon))

    return _lat_lon


def rice_gene_mask(_file_path = './'):

    _f = Dataset(_file_path + '/Rice_gene_region.nc', 'r')
    _lat = _f.variables['lat'][:]
    _lon = _f.variables['lon'][:]
    _region = _f.variables['region'][:]
    _f.close()
    
    _f = Dataset(_file_path + '/RiceAtlas_calendar.nc', 'r')
    _lat_in = _f.variables['lat'][:]
    _lon_in = _f.variables['lon'][:]
    _plant1 = _f.variables['PLANTPK1'][:]
    _plant2 = _f.variables['PLANTPK2'][:]
    _plant3 = _f.variables['PLANTPK3'][:]
    _f.close()

    _lat_lon = []
    _gene_region =[]
    plant1 = []
    plant2 = []
    plant3 = []
    for i in xrange(len(_lat)):
        for j in xrange(len(_lon)):
            # First use gene region mask
            if _region[i,j] > 0.0:
                # Second use rice calendar mask
                if _plant1[i,j] > 0.0:
                    _lat_lon.append([_lat[i], _lon[j]])
                    _gene_region.append(_region[i,j])
                    plant1.append(_plant1[i,j])
                    plant2.append(_plant2[i,j])
                    plant3.append(_plant3[i,j])

    print 'Total grid number for China domain is %s' % (len(_lat_lon))

    return _lat_lon, _gene_region, plant1, plant2, plant3


if __name__ == '__main__':
    #_lat_lon = rice_area_mask('/Users/qingsun/GGCM/mask_rice/')
    _lat_lon, _gene_region, plant1, plant2, plant3 = rice_gene_mask('/Users/qingsun/GGCM/mask_rice/')

