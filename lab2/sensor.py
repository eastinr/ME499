#!/usr/bin/env python


from math import sin
from random import gauss

# Generates data from a fictional sensor, complete with measurement
# noise.
def generate_sensor_data(n=1000, noise=0.05):
    return [sin(x * 0.01) + gauss(0.0, noise) for x in xrange(n)]


# Print some sensor data to a file.
def print_sensor_data(data, filename):
    with open(filename, 'w') as f:
        for i in range(len(data)):
            f.write('{0}\t{1}\n'.format(i, data[i]))
