#!/usr/bin/env python


def gcd(num1, num2):
    if num1 == 0 or num2 == 0:
        return False
    if num1 == num2:
        return num1
    if num1 > num2:
        return gcd(num1-num2, num2)
    return gcd(num1, num2-num1)


if __name__ == '__main__':
    print("Testing Functions...")
    print("Values: 108, 45")
    print("Expected Result: {0}".format(9))
    print "gcd result: {0}".format(gcd(108, 45))
