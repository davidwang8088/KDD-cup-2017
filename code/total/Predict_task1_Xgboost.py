# -*- coding: utf-8 -*-
"""
Code for prediction
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
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
# train = pd.read_csv('..\..\\data_pre\\table3456_train_task1.csv').set_index(['intersection_id','tollgate_id','time_window'])
# test = pd.read_csv('..\..\\data_pre\\table3456_test_task1.csv').set_index(['intersection_id','tollgate_id','time_window'])
train = pd.read_csv('..\..\\data_pre\\table34567_train_task1.csv').set_index(['intersection_id','tollgate_id','time_window'])
test = pd.read_csv('..\..\\data_pre\\table34567_test_task1.csv').set_index(['intersection_id','tollgate_id','time_window'])
X_train = train.drop('avg_travel_time',axis=1).values
X_test = test.drop('avg_travel_time',axis=1).values
y = train.avg_travel_time.values

def main():
    # # 使用grid search寻找最佳参数
    # param_grid = {
    #     'colsample_bytree':np.linspace(0.1,0.3, 10),
    #     'gamma':np.linspace(0.0,0.1, 10),
    #     'learning_rate':np.linspace(0.01,0.05, 10),
    #     'max_depth':range(5,15),
    #     'min_child_weight':np.linspace(1, 2, 10),
    #     'n_estimators':range(1000, 10000, 10),
    #     'reg_alpha':np.linspace(0.8, 0.99, 10),
    #     'reg_lambda':np.linspace(0.5, 0.7, 10),
    #     'subsample':np.linspace(0.1, 0.3, 10),
    #     'seed':range(40, 50),
    #     'silent':range(1, 10)
    # }

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

    # # 使用Grid search寻找最佳参数
    # regr = GridSearchCV(regr, param_grid=param_grid, cv=5, verbose=2, n_jobs=4,
    #                            scoring=score, error_score=0, refit=True)

    # 训练，预测
    regr.fit(X_train, y)
    # print regr.best_params_
    # print regr.best_score_
    test = pd.read_csv('..\..\\data_pre\\table34567_test_task1.csv').set_index(['intersection_id','tollgate_id','time_window'])
    test['avg_travel_time'] = regr.predict(X_test)
    test = test.reset_index()
    test = test[['intersection_id','tollgate_id','time_window','avg_travel_time']]
    test.head()

    # 保存结果
    test = test.sort_values(['intersection_id','tollgate_id'])
    test.to_csv('..\..\\result\\xgboost_task1_sorted.csv', index=False)

if __name__ == "__main__":
    main()