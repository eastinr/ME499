#!/usr/bin/env python

from math import pi
import unittest
import pytest


class Circle:

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return pi * self.radius ** 2

    def diameter(self):
        return self.radius * 2

    def perimeter(self):
        return pi * 2 * self.radius


class Rectangle:

    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.width + self.length)


class Complex:

    def __init__(self, real=0, imaginary=0):
        self.re = real
        self.im = imaginary

    def __str__(self):
        if self.im < 0:
            return "({0} - {1})".format(self.re, abs(self.im))
        else:
            return "({0} + {1})".format(self.re, abs(self.im))


class CodeTester(unittest.TestCase):

    def test_Circle_Area(self):
        radius = 1.2
        self.assertTrue(self.Class_tester(Circle.area, pi * radius ** 2, radius))

    def test_Circle_Perimeter(self):
        radius = 1.2
        self.Class_tester(Circle.perimeter, 2 * pi * radius, radius)

    def test_Rectangle_Area(self):
        self.Class_tester(Rectangle.area, 3 * 4, 3, 4)


    def test_Rectangle_Perimeter(self):
        self.Class_tester(Rectangle.perimeter, 2 * (3 + 4), 3, 4)


    def Class_tester(self, func, estimated_value, *class_args):
        test_class = func.im_class
        class_name = test_class.__name__
        func_name = func.__name__
        temp_class = test_class(*class_args)
        test_value = func(temp_class)

        print "\nTesting {0}.{1} using {0}({2})...".format(class_name, func_name, class_args)
        print "Returned Value: {0}\t\tExpected Value: {1}".format(test_value, estimated_value)

        if not self.assertEqual(test_value, estimated_value):
            return True
        return False

if __name__ == '__main__':
    unittest.main(Verbosity=2)