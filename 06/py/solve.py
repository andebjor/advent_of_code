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
            return (len(seen), seen, mem.banks)

        seen.append(mem.banks[:])

        mem.reallocate()


def solve_2(banks, repeated):
    ind = banks.index(repeated)
    return len(banks) - ind


def main():
    banks = read_input('../input/banks.dat')

    (n_cycles, seen, repeated) = solve_1(banks)
    print("Answer 1: %d" % n_cycles)

    print("Answer 2: %d" % solve_2(seen, repeated))

    return True


if __name__ == '__main__':
    sys.exit(not main())
