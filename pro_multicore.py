# QING SUN/NUIST

import multiprocessing as mp 


def job(x):
    return x*x

def multicore():
    l = mp.lock()
    pool = mp.Pool(process =3) #core number
    res = pool.map(job, range(10))
    print res


if __name__ == '__main__':
    multicore()
