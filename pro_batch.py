# coding=utf-8
import os

def write_batch(_site_path):
    ls = []
    ls.append('$BATCH(RICE)')
    ls.append('! Command Line : C:\DSSAT47\DSCSM047.EXE RICER047 B DSSBatch.v47')
    ls.append('! QING/NUIST')
    ls.append('@FILEX                                                                                        TRTNO     RP     SQ     OP     CO')

    _rix_list = []
    dirs = os.listdir(_site_path)
    for i in dirs:
        if os.path.splitext(i)[1] == ".RIX":
            _rix_list.append(_site_path + i)
    _rix_list.sort()

    for i in xrange(len(_rix_list)):
        ls.append('%-94s    1      1      0      0      0' % _rix_list[i])


    fname = _site_path + 'DSSBatch.v47'
    with open(fname, 'w') as fo:
        fo.write('\r\n'.join(ls))

    print 'Finised write DSSBatch.v47.'

