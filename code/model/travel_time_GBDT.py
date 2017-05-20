# -*- coding: utf-8 -*-
"""
Created on Tue May 16 09:54:12 2017
###KDDCup 2017赛题 task1###
使用XGBoost算法，制造特征
@team: GDUTDatamining
@author: johnnywong
"""
import os
mingw_path = 'C:\Program Files\mingw-w64\\x86_64-6.3.0-posix-seh-rt_v5-rev1\mingw64\\bin'
os.environ['PATH'] = mingw_path + ';' + os.environ['PATH']
import numpy as np
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt



