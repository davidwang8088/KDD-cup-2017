
# 在这个repo提供的思路就是数据工程+决策树/线性回归方法

## 1.pandas数据设置新的索引  
data.Frame.set_index('列的labael')  
[pandas.DataFrame.set_index()](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.set_index.html)

## 2.pandas聚类数据
DataFrame.groupby()

## 3.数据预处理:在对业务背景理解基础上,从数据中提取并组织特征  
* 在这个程序中,前期大量的工作在处理数据,这也算是时空数据,包括静态道路拓扑,动态的每段道路车流入信息等.      
* __关键是提取特征,并组合这些特征__
* 这可能是真正的数据挖掘在干的事情.

## 4.提取特征之后,选择了相对简单的线性回归,决策树等方法进行预测   


