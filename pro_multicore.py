# QING SUN/NUIST

import multiprocessing as mp 


def job(x):
    return x*x

def multicore(core_number):
    l = mp.lock()
    pool = mp.Pool(process =core_number) #core number
    res = pool.map(job, range(10))
    print res


if __name__ == '__main__':
    multicore(3)




import time
import numpy as np
# 省略若干...
pCOs = np.linspace(1e-5, 0.5, 10)
pO2s = np.linspace(1e-5, 0.5, 10)
if "__main__" == __name__:
    try:
        start = time.time()
        for i, pO2 in enumerate(pO2s):
            # ...
            for j, pCO in enumerate(pCOs):
                # 针对当前的分压值 pCO, pO2进行动力学求解
                # 具体代码略...
        end = time.time()
        t = end - start
    finally:
        # plot


import time
from multiprocessing import Pool
import numpy as np

pCOs = np.linspace(1e-5, 0.5, 10)
pO2s = np.linspace(1e-5, 0.5, 10)
def task(pO2):
    '''接受一个O2分压，根据当前的CO分压进行动力学求解'''
    # 代码细节省略...
if "__main__" == __name__:
    try:
        start = time.time()
        pool = Pool(process=core_number)    
        tofs = pool.map(task, pCOs)  
        end = time.time()
        t = end - start
    finally:
        # results and plot

