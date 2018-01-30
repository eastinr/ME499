#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np


def get_sample_sum():
    samples = np.random.uniform(0.0, 1.0, 10)
    return samples.sum()

def plot_histo():
    my_list = []
    for i in range(10000):
        my_list.append(get_sample_sum())

    plt.hist(my_list, 100)
    plt.title("Uniform Distribution Sampling")
    plt.xlabel("Sample Bins")
    plt.ylabel("Occurrences")
    plt.show()

if __name__ == '__main__':
    plot_histo()