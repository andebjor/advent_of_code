#!/usr/bin/env python3

import copy
import sys


class Memory():
    def __init__(self, banks):
        self.banks = banks

    def reallocate(self):
        bank = self.banks.index(max(self.banks))
        num  = self.banks[bank];

        self.banks[bank] = 0;
        for i in range(num):
            self.banks[(i + bank + 1)%len(self.banks)] += 1


def read_input(fname):
    with open(fname, 'r') as f:
        return [int(x) for x in f.read().split('\t')]


def solve_1(banks):
    mem = Memory(banks)

    seen = []
    while True:
        if mem.banks in seen:
            return len(seen)

        seen.append(mem.banks[:])

        mem.reallocate()


def main():
    banks = read_input('../input/banks.dat')

    print("Answer 1: %d" % solve_1(banks))

    return True


if __name__ == '__main__':
    sys.exit(not main())
