#!/usr/bin/env python

import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt


def optimize_step(func, bounds, n):
    lower_bound = bounds[0]
    upper_bound = bounds[1]
    xvalues = np.linspace(lower_bound, upper_bound, n)
    yvalues = map(func, xvalues)
    yvalues.sort()
    return yvalues[-1]


def optimize_random(func, bounds, n):
    lower_bound = bounds[0]
    upper_bound = bounds[1]
    xvalues = np.random.random_sample(n)
    xvalues = xvalues * (upper_bound - lower_bound) + lower_bound
    yvalues = map(func, xvalues)
    yvalues.sort()
    return yvalues[-1]

def gradient(func, x, h):
    x1 = x - h / 2
    x2 = x + h / 2
    return (func(x2) - func(x1)) / h

def optimize_gradient(func, bounds, epsilon):
    lower_bound = bounds[0]
    upper_bound = bounds[1]
    alpha = 0.001
    xnew = np.mean(bounds)
    stepsize = epsilon * 10
    while stepsize > epsilon and lower_bound < xnew < upper_bound:
        xold = xnew
        xnew = xold + alpha * gradient(func, xold, stepsize)
        stepsize = abs(func(xnew) - func(xold))
    return func(xnew)


def scipy_optimize(f, bounds, n):
    return optimize.minimize_scalar(lambda x: -f(x), bounds=bounds, method='bounded', options={'maxiter': n})


def optimize_gradient_handler(f, bounds, n):
    return optimize_gradient(f, bounds, (bounds[1] - bounds[0]) / (n))


def compare_functions():
    bounds = (-10, 10)
    num = 10
    optimizers = [optimize_step, optimize_random, optimize_gradient_handler, scipy_optimize]
    functions = [quadratic, wiggly]
    xvals = xrange(1, num + 1)
    yvals = np.array([[[optimizer(func, bounds, n+1) for n in xvals] for func in functions] for optimizer in optimizers])
    plt.plot()
    print yvals[0,0,:]


def optimize_md(func, bounds):
    pass


def wiggly(x):
    return np.cos(10 * x - 1) / (x * x + 1)


def quadratic(x):
    return -(2*x**2 + 4*x - 3)


if __name__ == '__main__':
    compare_functions()
    n = 1



    # for n in xrange(num):
    #     yvals2 = []
    #     for func in functions:
    #         yvals1 = []
    #         for optimizer in optimizers:
    #             yvals1.append(optimizer(func, bounds, n+1))
    #
    #         # yvals1.append(optimize_step(func, bounds, n+1))
    #         # yvals1.append(optimize_random(func, bounds, n+1))
    #         # yvals1.append(optimize_gradient(func, bounds, n+1))
    #         # yvals1.append(scipy_optimize(func, bounds, n+1))
    #         yvals2.append(yvals1)
    #     yvals3.append(yvals2)
    # print optimize_gradient(wiggly, bounds, .001)
