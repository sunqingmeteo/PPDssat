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


def rice_gene_mask(_file_path = './', plantpk='PK1'):

    _f = Dataset(_file_path + '/Rice_gene_region.nc', 'r')
    _lat = _f.variables['lat'][:]
    _lon = _f.variables['lon'][:]
    _region = _f.variables['region'][:]
    _f.close()
    
    _f = Dataset(_file_path + '/RiceAtlas_calendar_new.nc', 'r')
    _lat_in = _f.variables['lat'][:]
    _lon_in = _f.variables['lon'][:]
    _plant1 = _f.variables['PLANTPK1'][:]
    _plant2 = _f.variables['PLANTPK2'][:]
    _plant3 = _f.variables['PLANTPK3'][:]
    _f.close()

    _lat_lon = []
    _gene_region =[]
    plantday = []

    if plantpk == 'PK1':
        for i in xrange(len(_lat)):
            for j in xrange(len(_lon)):
                # First use gene region mask
                if _region[i,j] > 0.0:
                    # Second use rice calendar mask
                    if _plant1[i,j] > 0.0:
                        _lat_lon.append([_lat[i], _lon[j]])
                        _gene_region.append(_region[i,j])
                        plantday.append(_plant1[i,j])
    elif plantpk == 'PK2':
        for i in xrange(len(_lat)):
            for j in xrange(len(_lon)):
                # First use gene region mask
                if _region[i,j] > 0.0:
                    # Second use rice calendar mask
                    if _plant2[i,j] > 0.0:
                        _lat_lon.append([_lat[i], _lon[j]])
                        _gene_region.append(_region[i,j])
                        plantday.append(_plant2[i,j])
    elif plantpk == 'PK3':
        for i in xrange(len(_lat)):
            for j in xrange(len(_lon)):
                # First use gene region mask
                if _region[i,j] > 0.0:
                    # Second use rice calendar mask
                    if _plant3[i,j] > 0.0:
                        _lat_lon.append([_lat[i], _lon[j]])
                        _gene_region.append(_region[i,j])
                        plantday.append(_plant3[i,j])
    else:
        print 'Choose plant peak day from PK1, PK2 or PK3'
        os.exit()

    print 'Total grid number for China domain is %s' % (len(plantday))

    return _lat_lon, _gene_region, plantday


if __name__ == '__main__':
    #_lat_lon = rice_area_mask('/Users/qingsun/GGCM/mask_rice/')
    _lat_lon, _gene_region, plantday = rice_gene_mask('/Users/qingsun/GGCM/mask_rice/', plantpk='PK3')
    print len(_lat_lon)

