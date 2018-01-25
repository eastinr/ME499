#!/usr/bin/env python


from sensor import *
from null_filter import *
import matplotlib.pyplot as plt

def mean_filter(data):
    filtered = []

    for datum in data[1:-2]:
        mean = sum(data[datum-1:datum+1])/3
        filtered.append(mean)


def median_filter():




if __name__ == '__main__':
    data = generate_sensor_data()

    mean_filtered_data = mean_filter(data)
    median_filtered_data = median_filter(data)