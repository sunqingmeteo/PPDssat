#coding=utf-8
import os
import matplotlib as plt

def read_summary(_path):
    summary = []
    if os.path.exists(_path + '/Summary.OUT'):
        with open (_path + '/Summary.OUT', 'r') as f:
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


# every year plot 1 fig
# plot average yield one line
# plot 
def plot():
