# coding:utf-8
import pandas as pd
import numpy as np
t4 = pd.read_csv('..\\..\\KDD_OFFICIAL_DATA\dataSets\\training\\routes (table 4).csv')
t5_train = pd.read_csv('..\\..\\KDD_OFFICIAL_DATA\dataSets\\training\\trajectories(table 5)_training.csv')

ids = []
for i in range(t4.shape[0]):
    toll = t4.loc[i]['tollgate_id']
    inter = t4.loc[i]['intersection_id']
    ids.append([inter, toll])

# 存储所有的路径
paths = []
for p in t4['link_seq']:
    p = p.split(',')
    for path in p:
        if path not in paths:
            paths.append(path)
# 建立路径列
t5_pre = t5_train
for path in paths:
    t5_pre[path] = 0

# 读入travel_seq并写入时间
import time
time1 = time.time()
for i, row in t5_pre.iterrows():
    path_seq = t5_pre.loc[i]['travel_seq'].split(';')
    for path in path_seq:
        path_s = path.split('#')
        # print float(path_s[2])
        t5_pre.loc[i, path_s[0]] = float(path_s[2])
time2 = time.time()
print t5_pre.head()
print 'It takes %f seconds.' % (time2 - time1)
t5_pre.to_csv('..\..\\data_pre\\table_path.csv')
