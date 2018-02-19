#!/usr/bin/env python

import numpy as np
import pandas as pd
import math as m


def get_data(filename):
    #   Read file into a dataframe
    my_data = pd.read_csv(filename)

#   Look for and remove columns with all zeros
    my_data = my_data.loc[:, (my_data != 0).any(axis=0)]

#   Look for any values that are non-numeric and turn them into NaN
    my_data = my_data.drop(np.array(my_data.columns.values), axis=1).join(my_data.apply(pd.to_numeric, errors='coerce'))

    return my_data


def final_score_stats(my_data):
    final_scores = my_data['Final Score']

    print "Average Score: {0:.2f}".format(final_scores.mean())
    print "Above Average: {0:.2f}%".format((final_scores > final_scores.mean()).mean() * 100)
    print "Median Score: {0:.2f}".format(final_scores.median())
    print "Above Median: {0:.2f}%".format((final_scores > final_scores.median()).mean() * 100)


def hardest_assignment(my_data):
    assignment_names = [col for col in my_data.columns if 'homework' in col.lower()]
    assignments = my_data[assignment_names]
    assignment_percent = assignments.mean() / assignments.max()
    print "Hardest Assignment: {0}".format(assignment_percent.idxmin(axis=1))


def hardest_lab(my_data):
    lab_names = [col for col in my_data.columns if 'lab' in col.lower()]
    labs = my_data[lab_names]
    lab_percent = labs.mean() / labs.max()
    print "Hardest Lab: {0}".format(lab_percent.idxmin(axis=1))


def grade_dist(my_data):
    grade_letter = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']
    letter_bin = []
    for letter in grade_letter:
        letter_bin.append([letter, 0])
    grade_num = [94, 90, 87, 84, 80, 77, 74, 70, 67, 64, 61, 0]

    final_scores = my_data['Final Score']

    for score in final_scores:
        for i in xrange(len(grade_letter)):
            if score > grade_num[i]:
                letter_bin[i][1] += 1
                break
    for i in xrange(len(grade_letter)):
        print "{0}\t{1}".format(letter_bin[i][0], letter_bin[i][1])


def complainers(my_data):
    final_scores = my_data['Final Score']
    grade_num = [94, 90, 87, 84, 80, 77, 74, 70, 67, 64, 61, 0]
    num_of_complainers = 0
    for score in final_scores:
        for num in grade_num:
            if 0 < (num - score) <= 0.5:
                num_of_complainers += 1
    print "{0} students will complain about their grade.".format(num_of_complainers)


def different_grades(my_data):
    final_scores = my_data['Final Score']
    sorted_scores = sorted(final_scores, reverse=True)
    number_of_scores = len(sorted_scores)
    print "A\t{0:.2f}".format(sorted_scores[int(m.ceil(number_of_scores / (1 / 0.1)))])
    print "B\t{0:.2f}".format(sorted_scores[int(m.ceil(number_of_scores / (1 / 0.3)))])
    print "C\t{0:.2f}".format(sorted_scores[int(m.ceil(number_of_scores / (1 / 0.6)))])
    print "D\t{0:.2f}".format(sorted_scores[int(m.ceil(number_of_scores / (1 / 0.9)))])


if __name__ == '__main__':
    filename = "grades.csv"
    my_data = get_data(filename)

    final_score_stats(my_data)
    hardest_assignment(my_data)
    hardest_lab(my_data)
    grade_dist(my_data)
    complainers(my_data)
    different_grades(my_data)
