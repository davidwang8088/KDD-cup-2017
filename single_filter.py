#coding:utf-8

import sys

import numpy
import pandas

from datetime import datetime

def gen_table():
    csv_data = pandas.read_csv('E:\Competetion\KDD-cup-2017\KDD_OFFICIAL_DATA\dataSets\\training\links (table 3).csv')
    link_list = csv_data['link_id']
    table_columns = []
    for i in link_list.index:
        table_columns.append(str(link_list[i]) + '_time')
        table_columns.append(str(link_list[i]) + '_count')

    table = pandas.DataFrame(data = float(0), index = range(7*72+1), columns = table_columns)
    return table

def datetime2index(datetime_str):
    datetime_data = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    day = datetime_data.weekday()
    the_minute = datetime_data.hour * 60 + datetime_data.minute
    time_w = 0
    for i in range(0, 60 * 24, 20):
        if the_minute < i:
            time_w -= 1
            break
        time_w += 1
    return 72 * day + time_w

if __name__ == "__main__":
    full_table = gen_table()
    csv_data = pandas.read_csv('E:\Competetion\KDD-cup-2017\KDD_OFFICIAL_DATA\dataSets\\training\\trajectories(table 5)_training.csv')
    travel_seq = csv_data['travel_seq'].str.split(';')
    print(full_table.shape[0])
    for i in travel_seq.index:  #逐一读取 travel_seq
#    for i in range(105000,travel_seq.shape[0],10):  #读取 n 行 travel_seq
        for ii in range(len(travel_seq[i])):
            temp = travel_seq[i][ii].split('#')
            str1 = str(temp[0]) + '_time'
            str2 = str(temp[0]) + '_count'
            table_index = datetime2index(temp[1])
            full_table.loc[table_index, str1] += float(temp[2])
            full_table.loc[table_index, str2] += 1
    full_table.to_csv('result.csv')

