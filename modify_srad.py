#coding=utf-8
# Only for some specific sunlight hours
# No need for run PPDssat
import os

def modify_srad(_site_path='./'):
    _wth_list = []
    dirs = os.listdir(_site_path)
    for i in dirs:
        if os.path.splitext(i)[1] == ".WTH":
            _wth_list.append(_site_path + i)

    print _wth_list

    for i in xrange(len(_wth_list)):
        with open (_wth_list[i]) as fi:
            _content = fi.readlines()

        _wth_data= {}
        
         _head= _content[5].split()
        for j in xrange(len(_content[6:])):
            srad = _content[j+6].split()[2]
            if srad == '0.0':
                srad = '5.0'
            
if __name__ == '__main__':

    modify_srad('/Users/qingsun/GGCM/run_dssat/')
