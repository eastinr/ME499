#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    # names = ['piddelay0.csv','piddelay1.csv', 'piddelay10.csv', 'piddelay100.csv', 'piddelay1000.csv', 'piddelay5000.csv']
    names = ['pidsin.csv','bangbangsin.csv']
    data = [np.genfromtxt(name, delimiter=',', skip_header=1, skip_footer=1) for name in names]
    for i, name in enumerate(names):
        npdata = np.array(data[i])
        plt.plot(npdata[:,0], npdata[:,1], label=name)
        # plt.title(name)
        plt.xlim([9000, 11000])
        plt.ylim([500, 800])
    xvals = npdata[:,0]
    yvals = map(lambda x: 750*np.cos(2*np.pi*0.1*x), xvals / 1000.0)
    plt.plot(xvals, yvals, label='Sine Wave')
    plt.title("Sin Wave")
    plt.legend()
    plt.show()