#!/usr/bin/env python

import subprocess
import numpy as np
import random


class Simulator:
    def __init__(self, instance_number):
        self.instance = instance_number

    def evaluate(self, waypoints):
        # Verify that the argument is of the correct format
        try:
            assert(isinstance(waypoints, list))
            assert(isinstance(waypoint, tuple) and len(waypoint) == 2 for waypoint in waypoints)
        except AssertionError:
            print "Bad Input Detected!"
            print "Waypoints must be a list of tuples containing two numbers."

        write_to_file("better_waypoints", waypoints)

        # Get the output from the external program
        try:
            output = subprocess.check_output('simulator better_waypoints {0}'.format(self.instance))
        except:
            print "Error getting output from external program!"

        # Get the score from the output and return it as a float
        return get_score(output)


def write_to_file(filename, list):
    try:
        with open(filename, 'w') as f:
            for items in list:
                line = ' '.join([str(item) for item in items]) + '\n'
                f.write(line)
            f.close()
    except:
        print "Error writing waypoints to file!"


def get_score(text):
    try:
        text_list = text.split()
        score = text_list[-1]
        score = float(score[:-1])
        return score
    except:
        print "Error getting the score from the output!"


def find_better_waypoints(n_points=1, steps=100):
    # Printing the initial score
    instance_number = 15
    initial_waypoints = [(-10, -10), (10, 10)]
    s = Simulator(instance_number)
    starting_score = s.evaluate(initial_waypoints)
    print "Initial score from waypoints: {0} is {1}".format(initial_waypoints, starting_score)

    # Finding a better set of waypoints
    print "Finding a better set of waypoints..."
    number_list = np.linspace(-10, 10, steps)
    xgrid, ygrid = np.meshgrid(number_list, np.flip(number_list, 0))
    waypoint_map = zip(xgrid.ravel(), ygrid.ravel())

    waypoints_list = initial_waypoints
    score_list = []
    for waypoint in waypoint_map:
        if waypoint not in waypoints_list:
            new_waypoints = waypoints_list[:]
            new_waypoints.insert(1, waypoint)
            score_list.append(s.evaluate(new_waypoints))
    min_score = min(score_list)
    print "The waypoints {0}\nGave a score of {1}".format(new_waypoints, min_score)


def find_better_waypoints2(points=5):
    # Printing the initial score
    instance_number = 15
    initial_waypoints = [(-10, -10), (10, 10)]
    s = Simulator(instance_number)
    starting_score = s.evaluate(initial_waypoints)
    print "Initial score from waypoints: {0} is {1}".format(initial_waypoints, starting_score)

    # Finding a better set of waypoints
    print "Finding a better set of waypoints..."
    min_score = starting_score
    count = 1
    while True:
        new_waypoints = initial_waypoints[:]
        random_points = [(random.uniform(-10,10), random.uniform(-10,10)) for i in xrange(points)]
        [new_waypoints.insert(1, random_point) for random_point in random_points]
        score = s.evaluate(new_waypoints)
        if score < min_score:
            min_score = score
            print "\nA better score is {0}\nGiven by waypoints:".format(min_score)
            print new_waypoints
            break
        else:
            string = '\rNumber of combination attempted: {0} out of 1000'.format(count)
            print string,
            count = count + 1
            # print count
            if count > 1000:
                print "\nWas not able to find a better value :("
                break




if __name__ == '__main__':
    # find_better_waypoints(1, 10)
    find_better_waypoints2(2)