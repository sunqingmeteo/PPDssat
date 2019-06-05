# PPDassat
Pre- Post- process for DSSAT-Python

First add:
Qing/NUIST 04/26/2018

Author: Qing Sun

College of Applied Meteorology,

Nanjing University of Information Science & Technology (NUIST)

This a python I/O for writing and reading files of DSSAT input and output.

This is an open source code.
Only for research and study use.
Detail procedure will be written later on.


Add detail 2019.02.20:

Data needed:
1. Soil data (Such as SoilGrids data: CHINA_SoilGrids.SOL)
2. Climate data
        solar radiation
        precipatation
        wind
        tmax
        tmin
        tmean
3. Rice planting mask (Such as rice_mask_cn.nc)
4. RIX file (Such as EXAMPLE_RICE.RIX)
5. ALL .CDE files
6. DSSAT setting file for Linux/Mac: DSSATPRO.L47
7. Batch run file: DSSBatch.v47


Pathes are needed:
1. climate data path
2. Dssat run path 
3. Dssat executable file path 
4. Crop mask path 


File description:
Main run file: run_dssat_main.py
Post process file: post_dssat.py
Read mask from: pro_mask.py

No use and delete:
latlon.py
modify_srad.py


Update: 2018.12.21
update post process to read all Summary.OUT then write to .nc file.


Update: 2019.02.20
1. Clear some redundancy code.
   Add some detail note in some files.

2. Fix read future climate data index error.
   Update climate list read code.

3. Expand domain from south China to whole China.
   Add rice calendar from RiceAtlas.
   Add rice regional genetype and mask.
   Add CO2 subroutine.

4. Need to modify:
        a. change date from 1900s to 2000s in /dssat-csm/Utilities/DATES.for
                Line 81 and Line 578.
        b. add heat stress function in /CERES-Rice/RI_Grosub.for

Update: 2019.02.25
1. Add python mpi run file:run_mpi_dssat.py
   Note: only can be run in one cpu for multi-core.

2. Deploy in NUIST server and fix small bugs.

3. Add post process in main code.














