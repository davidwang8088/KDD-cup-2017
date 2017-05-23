# -*- coding: utf-8 -*-
"""
Code for prediction
"""
import pandas as pd
import numpy as np
from sklearn.metrics.scorer import make_scorer

# 导入Xgboost
import os
mingw_path = 'C:\Program Files\mingw-w64\\x86_64-6.3.0-posix-seh-rt_v5-rev1\mingw64\\bin'
os.environ['PATH'] = mingw_path + ';' + os.environ['PATH']
import xgboost as xgb

# 定义评分函数
def MAPE(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true))
score = make_scorer(MAPE, greater_is_better=False)


# 导入训练集数据和测试集数据
# train = pd.read_csv('..\..\\data_pre\\table3456_train_task2.csv').set_index(['tollgate_id','time_window','direction'])
# test = pd.read_csv('..\..\\data_pre\\table3456_test_task2.csv').set_index(['tollgate_id','time_window','direction'])
train = pd.read_csv('..\..\\data_pre\\table34567_train_task2.csv').set_index(['tollgate_id','time_window','direction'])
test = pd.read_csv('..\..\\data_pre\\table34567_test_task2.csv').set_index(['tollgate_id','time_window','direction'])
X_train = train.drop('volume',axis=1).values
X_test = test.drop('volume',axis=1).values
y = train.volume.values

def main():
    regr = xgb.XGBRegressor(
                     colsample_bytree=0.2,
                     gamma=0.0,
                     learning_rate=0.02,
                     max_depth=7,
                     min_child_weight=1.5,
                     n_estimators=3000,
                     reg_alpha=0.9,
                     reg_lambda=0.6,
                     subsample=0.2,
                     seed=42,
                     silent=1)

    # 训练，预测
    regr.fit(X_train, y)
    test = pd.read_csv('..\..\\data_pre\\table34567_test_task2.csv').set_index(['tollgate_id','time_window','direction'])
    test['volume'] = regr.predict(X_test)
    test = test.reset_index()
    test = test[['tollgate_id','time_window','direction','volume']]
    test.head()
    test = test.sort_values(['tollgate_id','direction'])
    # 保存结果
    test.to_csv('..\..\\result\\xgboost_task2_ver2.csv', index=False)

if __name__ == "__main__":
    main()