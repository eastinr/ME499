#!/usr/bin/env python


from sensor import *


def apply_null_filter(data):
    filtered = []
    for datum in data:
        filtered.append(datum)

    return filtered


if __name__ == '__main__':
    data = generate_sensor_data()

    filtered_data = apply_null_filter(data)

    print_sensor_data(data, 'raw')
    print_sensor_data(filtered_data, 'filtered')
