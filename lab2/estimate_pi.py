#!/usr/bin/env python


from math import factorial
from math import sqrt
from math import pi


def approx_sum(k):
    return factorial(4 * k) * (1103 + 26390 * k) / (factorial(k)**4 * 396**(4 * k))


def estimate_pi():
    summation = 0
    k = 0

    while True:
        series = approx_sum(k)
        summation += series
        k += 1
        if series < 1e-15:
            break

    return 1 / (2 * sqrt(2) / 9801 * summation)


if __name__ == '__main__':
    print("Testing Function estimate_pi...")
    print("Expected Result: {0}".format(pi))
    print("estimate_pi Results: {0}".format(estimate_pi()))
