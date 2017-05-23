# -*- coding: utf-8 -*-
"""
Code for prediction
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.metrics.scorer import make_scorer
from sklearn.linear_model import Lasso

# 定义评分函数
def MAPE(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true))
score = make_scorer(MAPE, greater_is_better=False)


# 导入训练集数据和测试集数据
# train = pd.read_csv('..\..\\data_pre\\table3456_train_task1.csv').set_index(['intersection_id','tollgate_id','time_window'])
# test = pd.read_csv('..\..\\data_pre\\table3456_test_task1.csv').set_index(['intersection_id','tollgate_id','time_window'])
train = pd.read_csv('..\..\\data_pre\\table34567_train_task2.csv').set_index(['tollgate_id','time_window','direction'])
test = pd.read_csv('..\..\\data_pre\\table34567_test_task2.csv').set_index(['tollgate_id','time_window','direction'])
X_train = train.drop('volume',axis=1).values
X_test = test.drop('volume',axis=1).values
y = train.volume.values

def main():
    # 使用grid search寻找最佳参数
    # Lasso 回归
    param_grid = {
     'alpha':np.linspace(0.001, 0.1, 1000)
    }
    grid_search = GridSearchCV(Lasso(),param_grid=param_grid,cv=5, verbose=2,n_jobs =4,
                              scoring=score,error_score=0,refit=True)

    # 训练，预测
    grid_search.fit(X_train, y)
    print grid_search.best_params_
    print grid_search.best_score_
    test = pd.read_csv('..\..\\data_pre\\table34567_test_task2.csv').set_index(['tollgate_id','time_window','direction'])
    test['volume'] = grid_search.predict(X_test)
    test = test.reset_index()
    test = test[['tollgate_id','time_window','direction','volume']]
    test.head()

    # 保存结果
    test.to_csv('..\..\\result\\Lasso_task2.csv', index=False)

if __name__ == "__main__":
    main()