#!/usr/bin/env python3

#  import re
import sys


def read_input(fname):
    with open(fname, 'r') as f:
        return f.read().strip()


def solve_1(stream):
    score = 0
    depth = 0
    in_garbage = False
    i = 0
    while i < len(stream):
        if in_garbage:
            if stream[i] == '>':
                in_garbage = False
                i += 1
                continue

            if stream[i] == '!':
                i += 2
                continue

            i += 1
            continue

        if stream[i] == '<':
            in_garbage = True

            i += 1
            continue

        if stream[i] == '{':
            depth += 1

            i += 1
            continue

        if stream[i] == '}':
            score += depth
            depth += -1

            i += 1
            continue

        i += 1

    return score


def main():
    stream = read_input('../input/stream.dat')

    score = solve_1(stream)
    print("Answer 1: %d" % score)

    return True


if __name__ == '__main__':
    sys.exit(not main())
