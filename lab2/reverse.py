#!/usr/bin/env python

def reverse_i(my_list):
    new_list = list()
    for item in range(len(my_list)):
        new_list.append(my_list.pop())
    return new_list


def reverse_r(my_list):
    if len(my_list) == 1:
        return [my_list.pop()]
    else:
        return [my_list[-1]] + reverse_r(my_list[:-1])


if __name__ == '__main__':
    print("Testing Functions...")
    print("List: range(10)")
    print("Expected Result: {0}".format(list(reversed(range(10)))))
    print "sum_i result: {0}".format(list(reverse_i(range(10))))
    print "sum_r result: {0}".format(reverse_r(range(10)))
