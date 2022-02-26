# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 13:41:42 2020

@author: rhaghi
"""

import weio
import os
import chaospy as cp
import numpy as np
import matplotlib.pyplot as plt
import pickle
import seaborn as sns
import scipy.stats as st
import statistics as sts
import scipy.fftpack
import scipy.special
import scipy.io as sio
from datetime import date
import time

timestr = time.strftime('%Y%m%d')


#%%

"""
This section modifies a TurbSim template file to the wind speeds
that are required. 6 Seeds from the seed pool are selected.
"""
HH = 90
WindSpdRange = np.array([25])
RandomSeeds =  np.array([915])

TurbSimInputTemp = "..\\TurbSim\\_Template\\HH_UREFmps_SeedNo.inp"
fTurbSimInput = weio.FASTInFile(TurbSimInputTemp)
TurbSimExeFile = "c:\\FAST\\bin\\TurbSim_x64.exe"
TurbSimBatFile = "..\\TurbSim\\"+timestr+'_TurbSimBatFile.bat'
fTurbSimBatFile = open(TurbSimBatFile,"w")


for i in WindSpdRange:
    fTurbSimInput = weio.FASTInFile(TurbSimInputTemp)
    fTurbSimInput['URef'] = i
    for j in RandomSeeds:
        fTurbSimInput['RandSeed1'] = j.astype(int)
        fTurbSimInput['NumGrid_Z'] = int(21)
        fTurbSimInput['NumGrid_Y'] = int(21)
        fTurbSimInput['AnalysisTime'] = int(661)
        TurbSimInputFileName =str(HH)+'m_'+str(i).zfill(2)+'mps_'+str(j.astype(int))+'.inp'
        fTurbSimInput.write("..\\TurbSim\\"+TurbSimInputFileName)
        fTurbSimBatFile.write(TurbSimExeFile+' '+TurbSimInputFileName+'\n')

fTurbSimBatFile.close()
#%%
InflowInputTemp = "..\\Inflow\\_Template\\NRELOffshrBsline5MW_InflowWind_XXmps.dat" 

InflowFileNameList={}
for i in WindSpdRange:
    fInflowInput = weio.FASTInFile(InflowInputTemp)
    fInflowInput['m/s'] = i
    for j in RandomSeeds:
        fInflowInput = weio.FASTInFile(InflowInputTemp)
        BTSFileName =str(HH)+'m_'+str(i).zfill(2)+'mps_'+str(j.astype(int))+'.bts'
        fInflowInput.data[19]['value'] = '"../TurbSim/'+BTSFileName+'"'
        InflowFileName = "NRELOffshrBsline5MW_InflowWind_"+str(i).zfill(2)+'mps_'+str(j.astype(int))+'.dat'
        fInflowInput.write("..\\Inflow\\"+InflowFileName)

#%%
        
HH = 90
#WindSpdRange = np.array([3])
#RandomSeeds =  np.array([294, 459, 522, 915])
SimLength = np.array([600])
DLC = 'DLC12'
WindDir =0
WaveDir = 0
TrasTime = 60;

FASTTemp = "..\\Sims\\_Template\\5MW_NREL_OnShore_Template.fst"
fFASTTemp = weio.FASTInFile(FASTTemp)
FASTExeFile = "c:\\FAST\\bin\\FAST_x64.exe"
FASTBatFile = "..\\Sims\\"+timestr+'_FASTBatFile_25mps_UpdSeeds.bat'
fFASTBatFile = open(FASTBatFile,"w")

FASTTemp = '..\\Sims\\_Template\\5MW_NREL_OnShore_Template.fst'


for i in SimLength:
    #os.chdir('..\\Sims\\DLC12_NREL5MWOnShore_SimLength'+str(i.astype(int))+'s')
    SimFolder = '..\\Sims\\DLC12_NREL5MWOnShore_SimLength'+str(i.astype(int))+'s'
    FASTBatFileFolder = SimFolder+"\\"+timestr+'_FASTBatFile_DLC12_'+str(i.astype(int))+'s'+'25mps_UpdSeeds.bat'
    fFASTBatFileFolder = open(FASTBatFileFolder,"w")
    for j in WindSpdRange:
        for k in RandomSeeds:
            fFASTTemp = weio.FASTInFile(FASTTemp) 
            fFASTTemp['TMax']=i+TrasTime
            fFASTTemp['EDFile']= '"../../'+fFASTTemp['EDFile'][1:]
            fFASTTemp['BDBldFile(1)']='"../../'+fFASTTemp['BDBldFile(1)'][1:]
            fFASTTemp['BDBldFile(2)']='"../../'+fFASTTemp['BDBldFile(2)'][1:]
            fFASTTemp['BDBldFile(3)']='"../../'+fFASTTemp['BDBldFile(3)'][1:]
            fFASTTemp['InflowFile']='"../../Inflow/'+'NRELOffshrBsline5MW_InflowWind_'+str(j).zfill(2)+'mps_'+str(k.astype(int))+'.dat"'
            fFASTTemp['AeroFile']='"../../'+fFASTTemp['AeroFile'][1:]
            fFASTTemp['ServoFile']='"../../'+fFASTTemp['ServoFile'][1:]
            fFASTTemp['TStart'] = TrasTime
            FASTFileName = 'NREL5MWOnShore_'+DLC+'_'+str(j).zfill(2)+'mps_'+str(WindDir).zfill(3)+'_'+str(WindDir).zfill(3)+'_'+str(i)+'s_'+str(k)+'.fst'
            fFASTTemp.write(SimFolder+'\\'+FASTFileName)
            fFASTBatFile.write(FASTExeFile+' '+SimFolder+'\\'+FASTFileName+'\n')
            fFASTBatFileFolder.write(FASTExeFile+' '+FASTFileName+'\n')
    fFASTBatFileFolder.close()

fFASTBatFile.close()
#os.chdir('..\\..\\_PythonCode')