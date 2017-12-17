#!/usr/bin/env python3

import sys


class Spinlock():
    def __init__(self, stride):
        self._vec = [0]
        self._pos = 0
        self._stride = stride + 1

    def insert(self, val):
        self._vec.insert(self._next_pos(), val)

    def get_after(self):
            return self._vec[(self._pos + 1) % len(self._vec)]

    def _next_pos(self):
        self._pos += self._stride
        self._pos %= len(self._vec)

        return self._pos


def solve_1(spinlock, max_val):
    for i in range(1, max_val+1):
        spinlock.insert(i)

    return spinlock.get_after()


def main():
    input = 348
    spinlock = Spinlock(input)

    print("Answer 1: %d" % solve_1(spinlock, 2017))

    return True


if __name__ == '__main__':
    sys.exit(not main())
