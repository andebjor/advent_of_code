#!/usr/bin/env python3

import sys


class Generator():
    def __init__(self, factor, start, modulo):
        self._factor   = factor
        self._previous = start
        self._modulo   = modulo

    def next(self):
        self._previous = (self._previous*self._factor)%2147483647

        if self._previous % self._modulo == 0:
            return self._previous
        else:
            return self.next()


def solve_2(A, B):
    score = 0
    for i in range(5*1000*1000):
        a = A.next()
        b = B.next()

        if (a%65536) == (b%65536):
            score += 1

        if i % 100000 == 0:
            print(i/1000)

    return score


def main():
    A = Generator(16807, 699, 4)
    B = Generator(48271, 124, 8)

    score = solve_2(A, B)
    print("Answer 1: %d" % score)

    return True


if __name__ == '__main__':
    sys.exit(not main())
