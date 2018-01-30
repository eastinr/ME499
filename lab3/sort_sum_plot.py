#!/usr/bin/env python

import timeit
import matplotlib.pyplot as plt
import random
import numpy as np


def plot_sort_sum():
    size_array = [1, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6]
    list_arr = []
    for i in size_array:
        list_arr.append(random.sample(xrange(i), i))
        t = timeit.timeit(sorted(list_arr[-1]))
        print t

if __name__ == '__main__':
    plot_sort_sum()
