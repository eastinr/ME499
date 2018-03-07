#!/usr/bin/env python

import numpy as np
import sys
import matplotlib.pyplot as plt


def errorcatch(msg, error):
    sys.exit("Program Failed Due To {0}! Try Again...\nError: {1}".format(msg, error))


class Integrator:
    def __init__(self, func, lower_bound, upper_bound, number_of_steps=1000):
        self.func = func
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.number_of_steps = number_of_steps
        try:
            assert self.number_of_steps > 0
            self.step_size = (self.upper_bound - self.lower_bound) / float(self.number_of_steps)
        except (AssertionError, TypeError) as e:
            errorcatch("Bad Inputs", e)
            raise

        self.bins = np.arange(self.lower_bound, self.upper_bound, self.step_size)

    def trapizoidal_rule(self, value):
        return self.step_size * (self.func(value + self.step_size) + self.func(value)) / 2.0

    def get_area(self):
        area_list = map(self.trapizoidal_rule, self.bins)
        return sum(area_list)


def integrate_mc(func, lower_bound, upper_bound, range_tuple, number_of_samples):
    try:
        assert range_tuple[0] < range_tuple[1]
        assert number_of_samples > 0
        area = (upper_bound - lower_bound) * (range_tuple[1] - range_tuple[0])
        random_xdist = np.random.uniform(lower_bound, upper_bound, number_of_samples)
        random_ydist = np.random.uniform(range_tuple[0], range_tuple[1], number_of_samples)
        points = zip(random_xdist, random_ydist)
        good_points = filter(lambda x: abs(func(x[0])) >= abs(x[1]), points)
        positive_values = sum(x[1] > 0 for x in good_points)
        return area * positive_values / float(number_of_samples)
    except (AssertionError, TypeError) as e:
        errorcatch("Bad Inputs", e)
        raise


def integrate(*args):
    try:
        integrator = Integrator(*args)
        return integrator.get_area()
    except (ValueError, TypeError) as e:
        errorcatch("Bad Inputs", e)
        raise


def ploterror(n):
    try:
        assert n > 0
        number_of_points = n
        lower_bound = 0
        upper_bound = 5
        true_value = 156.25
        binsize = np.arange(1, number_of_points)
        y1 = map(lambda n: true_value - integrate(lambda x: x ** 3, lower_bound, upper_bound, n), binsize)
        y2 = map(lambda n: true_value - integrate_mc(lambda x: x ** 3, lower_bound, upper_bound, (0, 156.25), n), binsize)
        plt.plot(binsize, y1, zorder=2)
        plt.plot(binsize, y2, zorder=1)
        plt.legend(['Reimann', 'Monte Carlo'], loc='upper right')
        plt.title('Integration Error')
        plt.xlabel('Number of Points')
        plt.ylabel('Absolute Error')
        plt.show()
    except (AssertionError, TypeError) as e:
        errorcatch("Bad Inputs", e)
        raise


def approximate_pi(n):
    try:
        assert n > 0
        area = 4
        random_xdist = np.random.uniform(-1, 1, n)
        random_ydist = np.random.uniform(-1, 1, n)
        points = zip(random_xdist, random_ydist)
        good_points = filter(lambda x: np.sqrt(x[0]**2 + x[1]**2) <= 1, points)
        return area * len(good_points) / float(n)
    except (AssertionError, TypeError) as e:
        errorcatch("Bad Inputs", e)
        raise

if __name__ == '__main__':
    print "Pi Approximation: {0:.10f}".format(approximate_pi(100000))
    #print integrate_mc(lambda x: x**2, 1, 3, 3, 100)
    ploterror(100)
