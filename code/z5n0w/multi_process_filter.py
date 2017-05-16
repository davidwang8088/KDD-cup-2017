#coding:utf-8

from os import remove

import numpy
import pandas
from datetime import datetime

from multiprocessing import Pool

def sum_link_time(data, file_name,  process_num, this_process):
    target = gen_sum_l_table()
    for i in range(this_process,len(travel_seq),process_num):  #逐一读取 travel_seq
        for ii in range(len(travel_seq[i])):
            temp = travel_seq[i][ii].split('#')
            str1 = str(temp[0]) + '_time'
            str2 = str(temp[0]) + '_count'
            table_index = datetime2index(temp[1])
#            print(str(table_index) + " ", end = "")
            target.loc[table_index, str1] += float(temp[2])
            target.loc[table_index, str2] += 1
    target.to_csv(file_name, index = False)
    print(str(file_name) + " done!")

def gen_sum_l_table():
    csv_data = pandas.read_csv('./training/links (table 3).csv')
    link_list = csv_data['link_id']
    table_columns = []
    for i in link_list:
        table_columns.append(str(i) + '_time')
        table_columns.append(str(i) + '_count')

    table = pandas.DataFrame(data = float(0), index = range(7*72), columns = table_columns)
    return table

def gen_avg_l_table():
    csv_data = pandas.read_csv('./training/links (table 3).csv')
    link_list = csv_data['link_id']
    table_columns = []
    for i in link_list:
        table_columns.append(str(i))
    table = pandas.DataFrame(data = float(0), index = range(7*72), columns = table_columns)
    return table

def datetime2index(datetime_str):
    datetime_data = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    day = datetime_data.weekday()
    the_minute = datetime_data.hour * 60 + datetime_data.minute
    for time_w in range(72):
        if the_minute < (time_w + 1) * 20:
            return 72 * day + time_w

if __name__ == "__main__":
    csv_data = pandas.read_csv('./training/trajectories(table 5)_training.csv')
    travel_seq = csv_data['travel_seq'].str.split(';')

    process_num = 4;
    precess_pool = Pool(processes = process_num)

    for i in range(process_num):
        temp_file = "result_" + str(i)
        precess_pool.apply_async(sum_link_time, (travel_seq, temp_file, process_num, i))
        print("process " + str(i) + " start")

    precess_pool.close()
    precess_pool.join()
    print("all done!")

    sum_l_table = gen_sum_l_table()
    for i in range(process_num):
        temp_file = "result_" + str(i)
        csv_data = pandas.read_csv(temp_file)
        remove(temp_file)
        sum_l_table += csv_data

    avg_l_table = gen_avg_l_table()
    csv_data = pandas.read_csv('./training/links (table 3).csv')
    link_list = csv_data['link_id']
    for i in link_list:
        str1 = str(i)
        str2 = str(i) + '_time'
        str3 = str(i) + '_count'
        avg_l_table[str1] = sum_l_table[str2] / sum_l_table[str3]

    avg_l_table.to_csv('result.csv', index = False)
