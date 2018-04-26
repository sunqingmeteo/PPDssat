# coding=utf-8
import os

def pro_summary()
# read Summary.OUT, yield and stage day
if os.path.exists(_run_dir + '/Summary.OUT'):
    with open (_run_dir + '/Summary.OUT', 'r') as f:
        summary = f.readlines()
    print type(summary),len(summary)

    # sim and obs
    _ADAT_sim  = []
    _MDAT_sim  = []
    _yield_sim = []


    