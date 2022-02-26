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
import pyts.io.read as pytsbts
#import pydatview 


timestr = time.strftime('%Y%m%d')

#%%