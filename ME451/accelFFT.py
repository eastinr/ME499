#!/usr/bin/env python

import csv
import numpy as np
import matplotlib.pyplot as plt
from readArduino import readArduino

#filename = "ZaccelLPF150hz.csv"
filename = '/home/robert/PycharmProjects/ME499/Zaccel1.csv'
#readArduino(filename, 9600, 20)
my_data = np.genfromtxt(filename, delimiter=',')


my_data_raw = my_data[:, 1]
my_data_filtered = my_data[:, 2]
time_data = my_data[:, 0]

fy = np.fft.fft(my_data_raw)
dt = (time_data[-1]-time_data[1])/len(time_data)/1000.0
n = time_data.size
freq = np.fft.fftfreq(n, d=dt)
x = np.fft.fftshift(freq)
y = np.fft.fftshift(abs(fy))

fy2 = np.fft.fft(my_data_filtered)
dt2 = (time_data[-1]-time_data[1])/len(time_data)/1000.0
n2 = time_data.size
freq2 = np.fft.fftfreq(n2, d=dt2)
x2 = np.fft.fftshift(freq2)
y2 = np.fft.fftshift(abs(fy2))

plt.subplot(221)
plt.plot(x, y)
plt.xlim([0,20])


plt.subplot(222)
plt.plot(x2,y2)
plt.xlim([0,20])

plt.subplot(223)
plt.plot(xrange(len(my_data_raw)), my_data_raw)
plt.xlim([0,1000])

plt.subplot(224)
plt.plot(xrange(len(my_data_filtered)), my_data_filtered)
plt.xlim([0,1000])


plt.show()
