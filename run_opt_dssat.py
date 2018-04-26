#coding=utf-8
import numpy as np
import random
import subprocess
import os
import time
from compiler.ast import flatten
import pandas as pd

def RMSE(target, prediction, rmse, mse, mae, _variance, _standard_deviation):
    error = []  
    for i in range(len(target)):  
        error.append(target[i] - prediction[i]) 
    squaredError = []  
    absError = []  
    for val in error:  
        squaredError.append(val * val)          #target-prediction   
        absError.append(abs(val))               #AE
    mse  = round(sum(squaredError) / len(squaredError), 2)
    rmse = round(np.sqrt(sum(squaredError) / len(squaredError)),2)
    mae  = round(sum(absError) / len(absError), 2)
    targetDeviation = []  
    targetMean = sum(target) / len(target)       #target mean value  
    for val in target:  
        targetDeviation.append((val - targetMean) * (val - targetMean))
    _variance = round(sum(targetDeviation) / len(targetDeviation), 2)
    _standard_deviation = round(np.sqrt(sum(targetDeviation) / len(targetDeviation)), 2)
    return rmse, mse, mae, _variance, _standard_deviation

def run_dssat(_loop_number, _run_dir='./'):
    for _i_loop in xrange(_loop_number):
        # Step 1: generate random parameters of rice gene type
        P1      = random.randint(120,880)   # radom integer
        P2R     = random.randint(  5,300)
        P5      = random.randint(200,600)
        P2O     = round(random.uniform( 10, 14), 2)
        G1      = random.randint( 37, 80)
        G2      = random.randint( 200, 300)
        G3      = 1.0
        G4      = 1.0
        PHINT   = 83.0
        G5      = 1.0

        _gene_list = []
        _gene_list.append(P1)
        _gene_list.append(P2R)
        _gene_list.append(P5)
        _gene_list.append(P2O)
        _gene_list.append(G1)
        _gene_list.append(G2)
        _gene_list.append(G3)
        _gene_list.append(G4)
        _gene_list.append(G5)
        _gene_list.append(PHINT)
        print _gene_list

        _head_list = []
        _head_list.append('*RICE GENOTYPE COEFFICIENTS: RICER047 MODEL')
        _head_list.append(' ')
        _head_list.append('@VAR#  VAR-NAME........ EXPNO   ECO#    P1   P2R    P5   P2O    G1    G2    G3    G4 PHINT    G5')
        _head_list.append('!                                        1     2     3     4     5     6     7     8     9    10')
        _head_list.append('IB0152 JDZ RICE             . IB0001 %5.1f %5.1f %5.1f  %4.1f  %4.1f .0%3d  %4.2f  %4.2f  %4.1f   %3.1f' \
                            % (P1,P2R,P5,P2O,G1,G2,G3,G4,PHINT,G5))

        with open(_run_dir + '/RICER047.CUL','w') as fo:
            fo.write('\r\n'.join(_head_list))


        # Step 2: run dssat once
        p = subprocess.call(_run_dir + '/dscsm047.exe RICER047 B DSSBatch.v47', shell=True)

        # Step 3: read Summary.OUT, yield and stage day
        if os.path.exists(_run_dir + '/Summary.OUT'):
            with open (_run_dir + '/Summary.OUT', 'r') as f:
                summary = f.readlines()
            print type(summary),len(summary)

            # sim and obs
            _ADAT_sim  = []
            _MDAT_sim  = []
            _yield_sim = []

            for i in xrange(len(summary)-4):
                _ADAT_sim.append(summary[i+4][126:133])
                _MDAT_sim.append(summary[i+4][134:141])
                _yield_sim.append(summary[i+4][167:171])

            _ADAT_obs  = [2012185, 2012185, 2012185, 2012185,
                          2013187, 2013187, 2013187, 2013187,
                          2013186, 2013186, 2013186, 2013186, 2013186, 2013186]
            _MDAT_obs  = [2012211, 2012211, 2012211, 2012211,
                          2013211, 2013211, 2013211, 2013211,
                          2013213, 2013213, 2013213, 2013213, 2013213, 2013213]
            _yield_obs = [ 8793,  6554,  5676,  2967,
                           7246,  6471,  6075,  5250,
                           8119,  7244,  5742,  5344,  5089,  4100]
            _sim = [_ADAT_sim,_MDAT_sim,_yield_sim]
            for i in xrange(len(_sim)):
                _sim[i] = map(float, _sim[i])
            _obs = [_ADAT_obs, _MDAT_obs, _yield_obs]


            # Step 3: Cal minimum loss of stage day and yield
            # input is list[float, float], input-output must be same
            _rmse = []
            mse = []
            mae = []
            _variance = []
            _standard_deviation = []
            n = len(_sim)
            m = len(_sim[0])
            for _n in xrange(n):
                _rmse.append(RMSE( _sim[_n], _obs[_n], _rmse, mse, mae, _variance, _standard_deviation))


            # Step 4: store loss and _gene_list in files.
            _results = []
            _result_gene = ['%5.1f, %5.1f, %5.1f,  %4.1f,  %4.1f, .0%3d,  %4.2f,  %4.2f,  %4.1f,   %3.1f' \
                                % (P1,P2R,P5,P2O,G1,G2,G3,G4,PHINT,G5)]
            _result_rmse = _rmse
            _results.append(_result_gene + _result_rmse)
            _results = flatten(_results)
            _results.append('\r\n')

            ls = []
            for i in xrange(len(_results)):
                ls.append(str(_results[i]))
            with open (_run_dir + 'Optimization_Results.csv','a') as fo:
                fo.write(','.join(ls))

            print 'Finished loop: ', _i_loop+1

def opt_dssat_parameter():
    _opt_file = pd.read_csv(_run_dir + '/Optimization_Results.csv')
    _opt_file = np.array(_opt_file)
    _opt_index = _opt_file[:,20].tolist().index(min(_opt_file[:,20]))
    _opt_out = _opt_file[_opt_index,:].tolist()
    ls = []
    for i in xrange(len(_opt_file[_opt_index,:])):
        ls.append(str(_opt_file[_opt_index,i]))
    with open(_run_dir + '/Opt_gene.csv', 'w') as fo:
        fo.write(','.join(ls))


_opt_head = ' P1, P2R, P5, P2O, G1, G2, G3, G4, PHINT, G5, \
            rmse, mse, mae, _variance, _standard_deviation, \
            rmse, mse, mae, _variance, _standard_deviation, \
            rmse, mse, mae, _variance, _standard_deviation'     #gene(10), _ADAT(5), _MDAT(5), _yield(5)

# Run DSSAT
if os.path.exists('./Optimization_Results.csv'):
    _file_exsit = raw_input("Already have Optimization_Results.csv! Want to delete Optimization_Results.csv? y/n: ")
    if _file_exsit == 'y' or _file_exsit == 'Y':
        os.remove('./Optimization_Results.csv')
    else:
        os.exit()

run_dssat(1000,'/Users/qingsun/GGCM/run_dssat/')
opt_dssat_parameter()