# KDD-cup-2017
Include:
1. Origin data
2. code for data preprocessing, data visulazation, model and training
3. some example code for testing

## 必装模块
xgboost：windows10 64位安装教程（https://www.zybuluo.com/Johnnywong/note/757972），其他系统可按照官网直接安装
其余模块安装对应系统版本，xgboost官网：http://xgboost.readthedocs.io/en/latest/build.html

## Useage
1. 使用code\Data_preprocessing.ipynb,对表格3，4，5，6进行预处理，在data_pre文件夹生成以table3456开头的4个csv文件；
2. 使用code\Data_preprocessing2.ipynb,对表格3，4，5，6，7进行预处理，在data_pre文件夹生成以table34567开头的4个csv文件；
3. 使用code\Data_combine.ipynb，对上述得到的两个版本的8个csv文件进行合并，生成4个csv文件；
4. 使用code\Prediction.ipynb进行预测，对第三步得到的csv文件进行预测，得到提交的文件；

## 本次使用的特征是
