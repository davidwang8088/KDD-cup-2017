# coding:utf-8
import pandas as pd

df = pd.DataFrame({'T': ['2015-12-30 22:10:00.0',
                         '2015-12-30 22:35:00.0',
                         '2015-12-30 22:40:00.0',
                         '2015-12-30 23:40:00.0',
                         '2015-11-30 13:40:00.0',
                         '2015-11-30 13:44:00.0',
                         '2015-11-30 19:54:00.0'],
                   'X': [1, 1, 1, 1, 3, 3, 3],
                   'Y': [2, 2, 2, 2, 5, 5, 5]})
print(df)
df['T'] = pd.to_datetime(df['T'])
print(df)
df = df.set_index(['T'])
print(df)
result = df.groupby([pd.TimeGrouper('15Min'), 'X', 'Y']).size()
print(result)
print(result.reset_index())