#!/usr/bin/env python

from math import sqrt

class Complex:

    def __init__(self, real=0, imaginary=0):
        self.re = real
        self.im = imaginary

    def __str__(self):
        sign = '-' if self.im < 0 else '+'
        return "({0} {1} {2}i)".format(self.re, sign, abs(self.im))

    def __repr__(self):
        return self.__str__()

    def add(self, other):
        try:
            return Complex(self.re + other.re, self.im + other.im)
        except:
            return Complex(self.re + other, self.im)

    def mul(self, other):
        try:
            return Complex(self.re * other.re - self.im * other.im, self.re * other.im + self.im * other.re)
        except:
            return Complex(self.re * other, self.im * other)

    def __add__(self, other):
        return self.add(other)

    def __radd__(self, other):
        return self.add(other)

    def __sub__(self, other):
        try:
            return Complex(self.re - other.re, self.im - other.im)
        except:
            return Complex(self.re - other, self.im)

    def __rsub__(self, other):
        try:
            return Complex(other.re - self.re, other.im - self.im)
        except:
            return Complex(other) - self

    def __mul__(self, other):
        return self .mul(other)

    def __rmul__(self, other):
        return self.mul(other)

    def __div__(self, other):
        try:
            real = self.re / float(other)
            imag = self.im / float(other)
            return Complex(real, imag)
        except:
            num = self * ~other
            den = (other * ~other).re
            return num / float(den)

    def __rdiv__(self, other):
        try:
            return (other * ~self) / float((self * ~self).re)
        except:
            return Complex(other / float(self.re), other / float(self.im))

    def __invert__(self):
        return Complex(self.re, -self.im)

    def __neg__(self):
        return Complex(-self.re, -self.im)

    def __abs__(self):
        return sqrt(self.re ** 2 + self.im ** 2)


if __name__ == '__main__':
    a = Complex(1, -2)
    b = Complex(3, 4)
    print "{0} + {1} = {2}".format(a, b, a + b)
    print "{0} + {1} = {2}".format(a, 1, a + 1)
    print "{0} + {1} = {2}".format(1, a, 1 + a)
    print "{0} - {1} = {2}".format(a, b, a - b)
    print "{0} - {1} = {2}".format(a, 1, a - 1)
    print "{0} - {1} = {2}".format(1, a, 1 - a)
    print "{0} * {1} = {2}".format(a, b, a * b)
    print "{0} * {1} = {2}".format(a, 3, a * 3)
    print "{0} * {1} = {2}".format(3, a, 3 * a)
    print "{0} / {1} = {2}".format(a, b, a / b)
    print "{0} / {1} = {2}".format(a, 3, a / 3)
    print "{0} / {1} = {2}".format(3, a, 3 / a)
