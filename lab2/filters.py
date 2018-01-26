#!/usr/bin/env python


from sensor import *
from null_filter import *
import numpy as n
import matplotlib.pyplot as plt


def mean_filter(data, num=3):
    cumsum = n.cumsum(data)
    cumsum[num:] = cumsum[num:] - cumsum[:-num]
    return cumsum[num - 1:] / num


def median_filter(data, num=3):
    filtered = []
    for datum in range(len(data)-2):
        median = n.median(data[datum:datum+2])
        filtered.append(median)
    return filtered


if __name__ == '__main__':
    data = n.array(generate_sensor_data())

    mean_filtered_data = mean_filter(data, 5)
    median_filtered_data = median_filter(data, 200)

    x1 = range(len(mean_filtered_data))
    x2 = range(len(median_filtered_data))
    y1 = mean_filtered_data
    y2 = median_filtered_data

    raw_plt = plt.scatter(range(len(data)), data, s=1)
    plt.title("Raw Data")
    plt.show()
    mean_plt = plt.scatter(x1, y1, s=1)
    plt.title("Mean Filtered Data")
    plt.show()
    med_plt = plt.scatter(x2, y2, s=1)
    plt.title("Median Filtered Data")
    plt.show()

    print_sensor_data(data, 'raw')
    print_sensor_data(mean_filtered_data, 'mean')
    print_sensor_data(mean_filtered_data, 'median')