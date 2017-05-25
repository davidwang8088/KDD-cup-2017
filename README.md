# KDD-cup-2017
Include:
1. Origin data
2. code for data preprocessing, data visulazation, model and training
3. some example code for testing

## 必装模块
xgboost：windows10 64位安装教程（https://www.zybuluo.com/Johnnywong/note/757972），其他系统可按照官网直接安装
其余模块安装对应系统版本，xgboost官网：http://xgboost.readthedocs.io/en/latest/build.html

## Useage

ipynb：
1. 使用code\total\Data_preprocessing.ipynb,对表格3，4，5，6进行预处理，在data_pre文件夹生成以table3456开头的4个csv文件；
2. 使用code\total\Data_preprocessing2.ipynb,对表格3，4，5，6，7进行预处理，在data_pre文件夹生成以table34567开头的4个csv文件；
3. 使用code\total\EDA.ipynb，对表格进行数据探索；
4. 使用code\total\Prediction.ipynb进行预测，对第三步得到的csv文件进行预测，得到提交的文件；

py：
1. 直接运行可直接得到结果，分别采用了Xgboost和Lasso回归，结果存储在result文件夹里面
