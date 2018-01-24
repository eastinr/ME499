#!/usr/bin/env python


def gcd(num1, num2):
    if num1 == 0 or num2 == 0:
        return False
    if num1 == num2:
        return num1
    if num1 > num2:
        return gcd(num1-num2, num2)
    return gcd(num1, num2-num1)


