#coding:utf-8

import sys

import numpy
import pandas

from datetime import datetime

from multiprocessing import Pool

def sum_link_time(data, target,  process_num, this_process):
    for i in range(this_process,len(travel_seq),process_num):  #逐一读取 travel_seq
        for ii in range(len(travel_seq[i])):
            temp = travel_seq[i][ii].split('#')
            str1 = str(temp[0]) + '_time'
            str2 = str(temp[0]) + '_count'
            table_index = datetime2index(temp[1])
            target.loc[table_index, str1] += float(temp[2])
            target.loc[table_index, str2] += 1

def gen_sum_l_table():
    csv_data = pandas.read_csv('./links (table 3).csv')
    link_list = csv_data['link_id']
    table_columns = []
    for i in link_list.index:
        table_columns.append(str(link_list[i]) + '_time')
        table_columns.append(str(link_list[i]) + '_count')

    table = pandas.DataFrame(data = float(0), index = range(7*72+1), columns = table_columns)
    return table

def gen_avg_l_table():
    csv_data = pandas.read_csv('./links (table 3).csv')
    link_list = csv_data['link_id']
    table_columns = []
    for i in link_list.index:
        table_columns.append(str(link_list[i]))
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
    csv_data = pandas.read_csv('./trajectories(table 5)_training.csv')
    travel_seq = csv_data['travel_seq'].str.split(';')

    process_num = 3;
    precess_pool = Pool(processes = process_num)
    sum_l_table = gen_sum_l_table()
    for i in range(process_num):
        precess_pool.apply_async(sum_link_time, (travel_seq, sum_l_table, process_num, i))
        print("process start")

    precess_pool.close()
    precess_pool.join()

    sum_l_table.to_csv('temp.csv', index = False)
