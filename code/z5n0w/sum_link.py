#coding:utf-8

from os import remove, getcwd
import pandas
from datetime import datetime
from multiprocessing import Pool

dataset_path = str(getcwd()) + "\github\KDD_OFFICIAL_DATA\dataSets\\training\\"

def sum_link_time(data, file_name,  process_num, this_process):
    target = gen_sum_l_table()

    for i in range(this_process,len(data),process_num):  #逐一读取 travel_seq
        for ii in range(len(data[i])):
            temp = data[i][ii].split('#')
            str1 = str(temp[0]) + '_time'
            str2 = str(temp[0]) + '_count'
            table_index = datetime2index(temp[1])
            target.loc[table_index, str1] += float(temp[2])
            target.loc[table_index, str2] += 1
    target.to_csv(file_name, index = False)
    print(str(file_name) + " done!")

def gen_sum_l_table():
    file = dataset_path + "links (table 3).csv"
    csv_data = pandas.read_csv(file)
    link_list = csv_data['link_id']
    table_columns = []
    for i in link_list:
        table_columns.append(str(i) + '_time')
        table_columns.append(str(i) + '_count')

    table = pandas.DataFrame(data = float(0), index = range(7*72), columns = table_columns)
    return table

def gen_avg_l_table():
    file = dataset_path + "links (table 3).csv"
    csv_data = pandas.read_csv(file)
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

def main():
    file = dataset_path + "trajectories(table 5)_training.csv"
    csv_data = pandas.read_csv(file)
    travel_seq = csv_data['travel_seq'].str.split(';')

    process_num = 4
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
    file = dataset_path + "links (table 3).csv"
    csv_data = pandas.read_csv(file)
    link_list = csv_data['link_id']
    for i in link_list:
        str1 = str(i)
        str2 = str(i) + '_time'
        str3 = str(i) + '_count'
        avg_l_table[str1] = sum_l_table[str2] / sum_l_table[str3]

    avg_l_table.to_csv('sum_link.csv', index = False)

if __name__ == "__main__":
    main()