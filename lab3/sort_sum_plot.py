#!/usr/bin/env python

import timeit
import matplotlib.pyplot as plt
import random


def plot_sort_sum():
    size_array = [1, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6]
    list_arr = []
    sort_time_list = []
    sum_time_list = []

    for i in range(len(size_array)):
        pop_list = range(1, int(size_array[i]) + 1)
        rand_list = random.sample(pop_list, len(pop_list))
        list_arr.append(rand_list)
        sort_time_list.append(timeit.Timer(lambda: sorted(list_arr[i])).timeit(number=1))
        sum_time_list.append(timeit.Timer(lambda: sum(list_arr[i])).timeit(number=1))

    plt.semilogx(size_array, sort_time_list, label='sorted function')
    plt.semilogx(size_array, sum_time_list, label='sum function')
    plt.grid(True)
    plt.title("Function Timing")
    plt.xlabel("List Size")
    plt.ylabel("Execution Time")
    plt.legend()

    plt.show()


if __name__ == '__main__':
    plot_sort_sum()
