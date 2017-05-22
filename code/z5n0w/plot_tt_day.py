from matplotlib import pyplot

from os import remove, getcwd
import platform

import numpy
import pandas

from multiprocessing import Pool

if platform.system() == "Windows":
    dataset_path = str(getcwd()) + "\\training\\"
else:
    dataset_path = "./training/"

def main():
    file = dataset_path + "links (table 3).csv"
    temp = pandas.read_csv(file)
    link_list = temp['link_id']


    file = "sum_link.csv"
    csv_data = pandas.read_csv(file)

    color_list = ["#ff0000", "#ff8000", "#ffff00", "#00ff00", "#0000ff", "#00ffff", "#8000ff"]
    x = numpy.arange(0, 72, 1)

    for link in link_list:
        pyplot.figure(link)
        for i in range(7):
            temp = csv_data[(i*72):((i+1)*72)]
            y = temp[str(link)]
            pyplot.plot(x, y, color = color_list[i])
    pyplot.show()

if __name__ == "__main__":
    main()