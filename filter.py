#coding:utf-8

import numpy
import pandas
from multiprocessing import Pool

from datetime import datetime

import csv

def lt_filter(data, seq, start, end):
    count = start
    for i in range(start, end):
        for ii in range(len(seq[i])):
            temp_seq = seq.append(pandas.Series(data[i][ii], index = [count]))
            seq = temp
            count += 1

if __name__ == "__main__":
    csv_data = pandas.read_csv('./trajectories(table 5)_training.csv')
    temp = csv_data['travel_seq']
    travel_seq = csv_data['travel_seq'].str.split(';')

    full_seq = pandas.Series() #创建用于存放的 Series


    process_num = 4
    part_seq[process_num] = pandas.Series() #创建用于存放的 Series
    process_pool = Pool(processes = process_num)
    record_size = temp.shape[0]
    works = record_size / process_num

    for i in range(0, process_num):
        if i != 3:
            process_pool.apply_async(lt_filter, (travel_seq, part_seq[i], i * works, (i+1) * works))
        else:
            process_pool.apply_async(lt_filter, (travel_seq, part_seq[i], i * works, record_size))

    pool.close()
    pool.join()

    full_seq = part_seq[0]

    temp = pandas.DataFrame(full_seq)
    temp.columns = ['data']
    full_seq = temp['data'].str.split('#')


