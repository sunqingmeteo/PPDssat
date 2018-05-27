#coding=utf-8
import numpy as np

def opt_dssat_parameter(_run_dir='./'):
    # Read opt results
    _opt_file = np.loadtxt(_run_dir + '/Opt_Results.csv', dtype=np.str, delimiter=",", skiprows=1)
    _opt_file = np.delete(_opt_file, -1, axis = 1)
    _opt_file = _opt_file.astype(float)

    '''
    _ADAT_r2 =  _opt_file[:,10]
    _ADAT_rmse = _opt_file[:,11]
    _MDAT_r2 = _opt_file[:,16]
    _MDAT_rmse = _opt_file[:,17]
    _yield_r2 = _opt_file[:,22]
    _yield_rmse = _opt_file[:,23]
    '''

    # normalization 
    # input np.array, every col normalization
    m = _opt_file.shape[0]
    n = _opt_file.shape[1]
    _opt_file_normalized = np.zeros(shape=(m,n))
    for i in xrange(n):
        aaa = _opt_file[:,i]
        _max_aaa = np.max(aaa)
        _min_aaa = np.min(aaa)
        _opt_file_normalized[:,i] = (aaa - _min_aaa) / (_max_aaa - _min_aaa)

    _opt_index_list = []

    for i in xrange(m):
        #_opt_index_list.append((_opt_file[i,10] + _opt_file_normalized[i, 11] + _opt_file[i,16] + _opt_file_normalized[i,17]) * 0.5 + (_opt_file[i,22] + _opt_file_normalized[i,23]) * 0.5)
        _opt_index_list.append((_opt_file[i,22] + _opt_file_normalized[i,23]))
    _opt_index = _opt_index_list.index(max(_opt_index_list))
    print _opt_index
    _opt_aaa = _opt_file[_opt_index].tolist()
    while '' in _opt_aaa:
        _opt_aaa.remove('')
    _opt_out = map(float, _opt_aaa)
    #print _opt_out, type(_opt_out)

    ls = []
    ls.append('*RICE GENOTYPE COEFFICIENTS: RICER047 MODEL')
    ls.append(' ')
    ls.append('@VAR#  VAR-NAME........ EXPNO   ECO#    P1   P2R    P5   P2O    G1    G2    G3    G4 PHINT    G5')
    ls.append('!                                        1     2     3     4     5     6     7     8     9    10')
    ls.append('IB0152 JDZ RICE             . IB0001 %5.1f %5.1f %5.1f  %4.1f  %4.1f .0%3d  %4.2f  %4.2f  %4.1f   %3.1f' \
                        % (_opt_out[0], _opt_out[1],_opt_out[2],_opt_out[3],_opt_out[4],_opt_out[5],_opt_out[6],_opt_out[7],_opt_out[8],_opt_out[9]) )



    with open(_run_dir + '/Opt_RICER047.CUL', 'w') as fo:
        fo.write('\r\n'.join(ls))
    print 'Congratulations! Optimization Results: Opt_RICER047.CUL was generated ^_^'


opt_dssat_parameter('/Users/qingsun/GGCM/outs_opt_dssat/run10_r2_without_JD1204/')


