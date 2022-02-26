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
from makewindVeers_main import *
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
WindSpdRange = np.arange(3,26)
RandomSeeds =  np.array([23, 31, 43, 54, 67, 73])

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
        InflowFileName = "NRELOffshrBsline5MW_InflowWind_"+str(i)+'mps_'+str(j.astype(int))+'.dat'
        fInflowInput.write("..\\Inflow\\"+InflowFileName)

#%%
        
HH = 90
WindSpdRange = np.arange(3,26)
RandomSeeds =  np.array([23, 31, 43, 54, 67, 73])
SimLength = np.array([600, 500, 400, 300, 200, 100, 50, 25, 10, 5])
#DLC = 'DLC12'

FASTTemp = "..\\Sims\\_Template\\5MW_NREL_OnShore_Template.fst"
fFASTTemp = weio.FASTInFile(FASTTemp)
FASTExeFile = "c:\\FAST\\bin\\FAST_x64.exe"
FASTBatFile = "..\\Sims\\"+timestr+'_FASTBatFile.bat'
fFASTBatFile = open(FASTBatFile,"w")
FASTTemp = '..\\Sims\\_Template\\5MW_NREL_OnShore_Template.fst'


for i in SimLength:
    os.mkdir('..\\Sims\\DLC12_NREL5MWOnShore_SimLength'+str(i.astype(int))+'s')
    SimFolder = '..\\Sims\\DLC12_NREL5MWOnShore_SimLength'+str(i.astype(int))+'s'
    FASTBatFileFolder = SimFolder+"\\"+timestr+'_FASTBatFile_DLC12_'+str(i.astype(int))+'s'+'.bat'
    fFASTBatFileFolder = open(FASTBatFileFolder,"w")
    for j in WindSpdRange:
        for k in RandomSeeds:
            fFASTTemp = weio.FASTInFile(FASTTemp) 
            fFASTTemp['TMax']=i+60
            fFASTTemp['EDFile']= '"../../'+fFASTTemp['EDFile'][1:]
            fFASTTemp['BDBldFile(1)']='"../../'+fFASTTemp['BDBldFile(1)'][1:]
            fFASTTemp['BDBldFile(2)']='"../../'+fFASTTemp['BDBldFile(2)'][1:]
            fFASTTemp['BDBldFile(3)']='"../../'+fFASTTemp['BDBldFile(3)'][1:]
            fFASTTemp['InflowFile']='"../../Inflow/'+'NRELOffshrBsline5MW_InflowWind_'+str(j)+'mps_'+str(k.astype(int))+'.dat"'
            fFASTTemp['AeroFile']='"../../'+fFASTTemp['AeroFile'][1:]
            fFASTTemp['ServoFile']='"../../'+fFASTTemp['ServoFile'][1:]
            FASTFileName = 'NREL5MWOnShore_'+str(j).zfill(2)+'mps_'+str(i)+'s_'+str(k)+'.fst'
            fFASTTemp.write(SimFolder+'\\'+FASTFileName)
            fFASTBatFile.write(FASTExeFile+' '+SimFolder+'\\'+FASTFileName+'\n')
            fFASTBatFileFolder.write(FASTExeFile+' '+FASTFileName+'\n')
    fFASTBatFileFolder.close()

fFASTBatFile.close()