#!/usr/bin/env python

import sys
import string


def take_arg():
    arg_num = len(sys.argv) - 1
    if arg_num != 2:
        print "Number of arguments given was: {0}".format(arg_num)
        print "Must supply exactly two arguments!"
        print "Please Try Again..."
    else:
        set1 = get_text(sys.argv[1])
        set2 = get_text(sys.argv[2])

        words_only_in_1 = set1.difference(set2)
        words_only_in_2 = set2.difference(set1)
        words_in_both = set1.intersection(set2)

        print "Only in {0}: {1}".format(sys.argv[1], len(words_only_in_1))
        print "Only in {0}: {1}".format(sys.argv[2], len(words_only_in_2))
        print "Both files: {0}".format(len(words_in_both))


def get_text(filename):
    text = []
    with open(filename, "r") as f:
        for line in f:
            text.extend(line.lower().translate(None, string.punctuation).split())

    word_set = set(text)

    print "Words in {0}".format(filename)
    print "\tTotal Words: {0}".format(len(text))
    print "\tUnique words: {0}".format(len(word_set))

    return word_set


if __name__ == '__main__':
    take_arg()