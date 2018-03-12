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
    x1 = x - h / 2.0
    x2 = x + h / 2.0
    return (func(x2) - func(x1)) / h


def linesearch(func, x, a, p, gradient):
    tau = .5
    t = .5 * gradient
    while func(x) - func(x + a * p) >= a * t:
        a *= tau
    return a


def optimize_gradient(func, bounds, epsilon):
    lower_bound = bounds[0]
    upper_bound = bounds[1]
    xnew = (lower_bound + upper_bound) / 2.0
    step = epsilon
    while True:
        xold = xnew
        grad = gradient(func, xnew, epsilon)
        if grad == 0:
            break
        direction = grad / abs(grad)
        step = linesearch(func, xnew, step, direction, grad)
        xnew += step * direction
        if abs(func(xnew) - func(xold)) < epsilon or lower_bound > xnew > upper_bound:
            break
    return func(xnew)


def scipy_optimize(f, bounds, n):
    return f(optimize.minimize_scalar(lambda x: -f(x), bounds=bounds, method='bounded').x)


def optimize_gradient_handler(f, bounds, n):
    return optimize_gradient(f, bounds, (bounds[1] - bounds[0]) / float(10 * n))


def compare_functions(num=100, min_points=3):
    bounds = (-10, 10)
    wigglymax = .990289437034
    quadmax = 5.0
    optimizers = [optimize_step, optimize_random, optimize_gradient_handler, scipy_optimize]
    optimizer_names = ["step", "random", "gradient", "scipy"]
    functions = [quadratic, wiggly]
    func_names = ["Quadratic Function", "Wiggly Function"]
    func_maxs = [quadmax, wigglymax]
    xvals = xrange(min_points, num + min_points)
    yvals = np.array([[[optimizer(func, bounds, n+min_points) for n in xvals] for func in functions] for optimizer in optimizers])
    for findex, funcname in enumerate(func_names):
        yvals[:, findex, :] = abs(yvals[:, findex, :] - func_maxs[findex])
        for index, name in enumerate(optimizer_names):
            plt.plot(xvals, yvals[index, findex, :], label=name)

        plt.legend()
        plt.title(funcname)
        plt.ylabel("Error")
        plt.xlabel("Number of Evaluations")
        plt.show()


def md_gradient(func, values, steps):
    values1 = [value - step / 2.0 for value, step in zip(values, steps)]
    values2 = [value + step / 2.0 for value, step in zip(values, steps)]
    return [(func(*values1) - func(*values2)) / float(step) for step in steps]


def optimize_md(func, bounds_list):
    epsilon = 0.001
    values = [(bounds[0] + bounds[1]) / 2.0 for bounds in bounds_list]
    steps = np.full(np.shape(values), epsilon)
    while True:
        old_values = values
        gradients = md_gradient(func, values, steps)
        directions = [gradient / float(abs(gradient)) for gradient in gradients]
        taus = np.full(np.shape(values), 0.5)
        ts = taus * gradients
        while func(*values) - func(*(values + steps * directions)) >= max(steps * ts):
            steps *= taus
        # for index, step in enumerate(steps):
        #     while func(*values) - func(*(values + steps * directions)) >= step * 0.5 * gradients[index]:
        #         step *= 0.5
        values += steps * directions
        if abs(func(*values) - func(*old_values)) < epsilon:
            break
    return tuple(values)


def wiggly(x):
    return np.cos(10 * x - 1) / float(x * x + 1)


def quadratic(x):
    return -(2*x**2 + 4*x - 3)


def md_function(x, y):
    return -(np.sin(x + y) + (x - y)**2 - 1.5*x + 2.5 * y + 1)


if __name__ == '__main__':
    compare_functions(1000)
    print optimize_md(md_function, [(-1.5, 4), (-3, 4)])
