#!/usr/bin/env python


def sum_i(my_list):
    my_sum = 0
    for thing in my_list:
        my_sum += my_list[thing]
    return my_sum


def sum_r(my_list):
    if len(my_list) > 0:
        return my_list.pop() + sum_r(my_list)
    else:
        return 0


if __name__ == '__main__':
    print("Testing Functions...")
    print("List: range(10)")
    print "Expected Result: %d" % sum(range(10))
    print "sum_i result: %d" % sum_i(list(range(10)))
    print "sum_r result: %d" % sum_r(list(range(10)))

