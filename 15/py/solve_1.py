#!/usr/bin/env python3

import sys


class Generator():
    def __init__(self, factor, start):
        self._factor   = factor
        self._previous = start

    def next(self):
        self._previous = (self._previous*self._factor)%2147483647
        return self._previous


def solve_1(A, B):
    score = 0
    for i in range(40*1000*1000):
        a = A.next()
        b = B.next()

        if (a%65536) == (b%65536):
            score += 1

        if i % 1000000 == 0:
            print(i/1000)

    return score


def main():
    A = Generator(16807, 699)
    B = Generator(48271, 124)

    score = solve_1(A, B)
    print("Answer 1: %d" % score)

    return True


if __name__ == '__main__':
    sys.exit(not main())
