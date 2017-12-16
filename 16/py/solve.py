#!/usr/bin/env python3

import copy
import sys


class Dance():
    def __init__(self, length):
        self._vec = list(range(length))

    def make_move(self, mtype):
        if mtype.is_spin:
            self._spin(mtype.a1)
            return
        if mtype.is_swap:
            self._swap(mtype.a1, mtype.a2)
            return
        if mtype.is_partner:
            self._partner(mtype.a1, mtype.a2)
            return

        raise ValueError('Illegal move')

    def as_str(self):
        ret = ''
        for c in self._vec:
            ret += chr(c + ord('a'))

        return ret

    def _spin(self, num):
        end = self._vec[-num:]
        start = self._vec[0:len(self._vec)-num]

        end.extend(start)
        self._vec = end

    def _swap(self, p1, p2):
        tmp = self._vec[p1]
        self._vec[p1] = self._vec[p2]
        self._vec[p2] = tmp

    def _partner(self, p1, p2):
        self._swap(self._vec.index(p1), self._vec.index(p2))


class Action():
    def __init__(self, str_repr):
        self.is_spin = False
        self.is_swap = False
        self.is_partner = False

        if str_repr[0] == 's':
            self.is_spin = True
            self.a1 = int(str_repr[1:])
            return

        if str_repr[0] == 'x':
            self.is_swap = True
            parts = str_repr[1:].split('/')
            self.a1 = int(parts[0])
            self.a2 = int(parts[1])
            return

        if str_repr[0] == 'p':
            self.is_partner = True
            self.a1 = ord(str_repr[1])- ord('a')
            self.a2 = ord(str_repr[3])- ord('a')
            return

        raise ValueError('Unrecognized move')


def read_actions(fname):
    actions = []
    with open(fname, 'r') as f:
        str_actions = f.read().split(',')

    for sa in str_actions:
        actions.append(Action(sa))

    return actions


def solve_1(actions):
    dance = Dance(16)

    for a in actions:
        dance.make_move(a)

    return dance.as_str()


def main():
    actions = read_actions('../input/dance.dat')

    print("Answer 1: '%s'" % solve_1(actions))

    return True


if __name__ == '__main__':
    sys.exit(not main())
