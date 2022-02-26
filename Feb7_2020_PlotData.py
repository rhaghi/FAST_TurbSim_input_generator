# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 13:41:42 2020

@author: rhaghi
"""
from wetb.fatigue_tools.fatigue import eq_load_and_cycles
import weio
import os
import glob
import fnmatch
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
import pandas as pd
#import pydatview 

timestr = time.strftime('%Y%m%d')

#%%
plt.close('all')
df = weio.FASTOutFile('NREL5MWOnShore_DLC12_03mps_000_000_600s_915.outb').toDataFrame()

ax1 = df.plot(x='Time_[s]',y='TwrBsMyt_[kN·m]')
df.plot(x='Time_[s]',y='Wind1VelX_[m/s]', ax = ax1.twinx(),color='red')

#ax2 = ax1.twinx()
#ax1 = df[9600:].plot(x='Time_[s]',y='Wind1VelX_[m/s]')
ax1.legend(loc=3)
#%%
OutbList = []

for file in os.listdir():
    if file.endswith('.outb'):
        OutbList.append(file)
        
#%%
files = list(filter(os.path.isfile, glob.glob('*.outb')))
#files.sort(key=lambda x: os.path.getmtime(x))

#%%

files = os.listdir()
blabla = fnmatch.filter(files,'*_03mps_*.outb')
#%%

files = os.listdir()
outbfilelist = fnmatch.filter(files,'*.outb')
print(os.stat(outbfilelist[85]).st_size)
FileSize = os.stat(outbfilelist[85]).st_size


k=0

for i in range(0,len(outbfilelist)):
    if  os.stat(outbfilelist[i]).st_size != FileSize:
        print(outbfilelist[i])
        outbfilelist[i] = 'zcucamber'
        print(outbfilelist[i])
        k=k+1

if k!=0:
    outbfilelist.sort()
    del outbfilelist[-1*k:]


#%%

def weib(x,lambd,k):
    return (k / lambd) * (x / lambd)**(k - 1) * np.exp(-(x / lambd)**k)

WindSpeed =np.arange(3,26)
#Manual input for now. Should change the naming convention to read it from files.
SimLengthInSec = 5; 
SimLengthInHours = SimLengthInSec/3600
LifeTime = 25;
NoOfSimsForLifeTime = (LifeTime*365*24)/SimLengthInHours
mWohler = 4
Nref = 1e7


WeibScale = 10
WeibShape = 2   

#Watch o
PostProssInputFolder = "../../PostProcessing/Input"
ListFile =PostProssInputFolder+"/"+timestr+"_FLSListFile_"+str(SimLengthInSec).zfill(3)+'s.lst'
fListFile = open(ListFile,"w")

#fListFile.write('This is a test')                              

for i in WindSpeed:
    WindSpeedFiles = fnmatch.filter(outbfilelist,'*_'+str(i).zfill(2)+'mps_*.outb')
    NumberOfSeeds = len(WindSpeedFiles)
    SimsWeightPerWindSpd = NoOfSimsForLifeTime*weib(i,10,2)
    WeightPerSim = SimsWeightPerWindSpd/NumberOfSeeds
    WeightPerSim = round(WeightPerSim,3)
    print(NumberOfSeeds)
    for j in range(0,NumberOfSeeds):
        fListFile.write(WindSpeedFiles[j]+' '+str(WeightPerSim)+'\n')

fListFile.close()
#%%

FatLstFile = pd.read_csv('../../PostProcessing/Input/20200218_FLSListFile_005s.lst',sep=" ", header=None)
FatLstFile.columns = ['FileName','Weight']

FatLoadChannel = 'TwrBsMyt_[kN·m]'
InputDEL = []

for i in range(0,FatLstFile.shape[0]):
    print(i)
    df = weio.FASTOutFile(FatLstFile['FileName'][i]).toDataFrame()
    InputDEL.append((FatLstFile['Weight'][i],df[FatLoadChannel].to_numpy()))
   
DEL = eq_load_and_cycles(InputDEL,m=4,neq=10e7)
print(DEL[0])
