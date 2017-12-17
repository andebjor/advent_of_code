#!/usr/bin/env python3

import re
import sys

class Instruction:
    def __init__(self, str_instruction):
        m = re.match(r'(\w+) (inc|dec) ([-0-9]+) if ([\w]+) ([<>=!]+) ([-0-9]+)', str_instruction)

        self._target         = m.groups()[0]
        is_increase          = (m.groups()[1] == 'inc')
        if is_increase:
            self._amount     = int(m.groups()[2])
        else:
            self._amount     = -int(m.groups()[2])
        self._check_register = m.groups()[3]
        self._check_operator = m.groups()[4]
        self._check_value    = int(m.groups()[5])

    def apply(self, reg):
        check_val = reg.get(self._check_register)

        if self._check_operator == '<':
            if not (check_val < self._check_value):
                return
        elif self._check_operator == '>':
            if not (check_val > self._check_value):
                return
        elif self._check_operator == '>=':
            if not (check_val >= self._check_value):
                return
        elif self._check_operator == '<=':
            if not (check_val <= self._check_value):
                return
        elif self._check_operator == '==':
            if not (check_val == self._check_value):
                return
        elif self._check_operator == '!=':
            if not (check_val != self._check_value):
                return
        else:
            raise ValueError("Unknown operator '%s'" % self._check_operator)

        reg.increase(self._target, self._amount)

    def __str__(self):
        return "Increase '%s' if '%s' %s %d" % (self._target,
                                                self._check_register,
                                                self._check_operator,
                                                self._check_value)



class Register:
    def __init__(self):
        self._reg = {}

    def get(self, key):
        if key not in self._reg.keys():
            self._reg[key] = 0

        return self._reg[key]

    def increase(self, key, val):
        if key not in self._reg.keys():
            self._reg[key] = 0

        self._reg[key] += val

    def get_max(self):
        return max(self._reg.values())

    def __str__(self):
        return str(self._reg)



def decode_instructions(str_instructions):
    instructions = []
    for si in str_instructions:
        instructions.append(Instruction(si))

    return instructions


def read_input(fname):
    with open(fname, 'r') as f:
        return f.read().splitlines()


def solve_1(instructions):
    reg = Register()

    for i in instructions:
        i.apply(reg)

    return reg.get_max()


def main():
    str_instructions = read_input('../input/instructions.dat')
    instructions = decode_instructions(str_instructions)

    print("Answer 1: %d" % solve_1(instructions))

    return True


if __name__ == '__main__':
    sys.exit(not main())
