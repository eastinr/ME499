#!/usr/bin/env python

from complex import Complex
from math import sqrt

def roots(a, b, c):
    try:
        root1 = (-b + sqrt(b ** 2 - 4 * a * c)) / (2.0 * a)
        root2 = (-b - sqrt(b ** 2 - 4 * a * c)) / (2.0 * a)
    except ValueError:
        c1 = Complex(0, sqrt(-(b ** 2 - 4 * a * c)))
        root1 = (-b + c1) / (2.0 * a)
        root2 = (-b - c1) / (2.0 * a)
    return root1, root2


if __name__ == '__main__':
    root = roots(1, 2, 3)
    print "Testing roots with x^2 + 2x + 3"
    print "Expected result: {0}\nActual result: {1}".format("(-1.0 + 1.41i), (-1.0 - 1.41i)",root)
