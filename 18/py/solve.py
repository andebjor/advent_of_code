#!/usr/bin/env python3

import re
import sys


class RecoveredException(Exception):
    pass


class Instruction:
    def __init__(self, str_instruction):
        m = re.match(r'([a-z]{3}) ([a-z0-9]) ?([-a-z0-9]+)?', str_instruction)

        self.is_snd = False

        operation = m.groups()[0]
        self._operation = operation
        if operation == 'snd':
            self.is_snd = True
            self._op_1 = m.groups()[1]
        elif operation == 'rcv':
            self._op_1 = m.groups()[1]
        else:
            self._op_1 = m.groups()[1]
            self._op_2 = m.groups()[2]

    def apply(self, reg):
        if self._operation == 'rcv':
            if reg.get(self._op_1) != 0:
                raise RecoveredException()
            else:
                return 1

        if self._operation == 'snd':
            return 1

        if self._operation == 'set':
            if is_number(self._op_2):
                reg.set(self._op_1, int(self._op_2))
            else:
                reg.set(self._op_1, reg.get(self._op_2))

            return 1

        if self._operation == 'add':
            if is_number(self._op_2):
                reg.increase(self._op_1, int(self._op_2))
            else:
                reg.increase(self._op_1, reg.get(self._op_2))

            return 1

        if self._operation == 'mul':
            if is_number(self._op_2):
                reg.multiply(self._op_1, int(self._op_2))
            else:
                reg.multiply(self._op_1, reg.get(self._op_2))

            return 1

        if self._operation == 'mod':
            if is_number(self._op_2):
                reg.modulus(self._op_1, int(self._op_2))
            else:
                reg.modulus(self._op_1, reg.get(self._op_2))

            return 1

        if self._operation == 'jgz':
            if is_number(self._op_1):
                test_val = int(self._op_1)
            else:
                test_val = reg.get(self._op_1)

            if test_val > 0:
                if is_number(self._op_2):
                    return int(self._op_2)
                else:
                    return reg.get(self._op_2)
            else:
                return 1

        raise ValueError("Unknown operation '%s'" % self._operation)


def is_number(string):
    try:
        int(string)
    except ValueError:
        return False

    return True


class Register:
    def __init__(self):
        self._reg = {}

    def get(self, key):
        if key not in self._reg.keys():
            self._reg[key] = 0

        return self._reg[key]

    def set(self, key, val):
        if key not in self._reg.keys():
            self._reg[key] = 0

        self._reg[key] = val

    def increase(self, key, val):
        if key not in self._reg.keys():
            self._reg[key] = 0

        self._reg[key] += val

    def multiply(self, key, val):
        if key not in self._reg.keys():
            self._reg[key] = 0

        self._reg[key] *= val

    def modulus(self, key, val):
        if key not in self._reg.keys():
            self._reg[key] = 0

        self._reg[key] %= val

    def __str__(self):
        return str(self._reg)


class Program:
    def __init__(self, instructions):
        self._instructions = instructions
        self._register = Register()
        self._stack_pointer = 0
        self._last_played_register = None

    def run(self):
        while True:
            if self._instructions[self._stack_pointer].is_snd:
                self._last_played_register = self._instructions[self._stack_pointer]._op_1

            try:
                self._stack_pointer += self._instructions[self._stack_pointer].apply(self._register)
            except RecoveredException as e:
                if self._register.get(self._last_played_register) != 0:
                    return self._register.get(self._last_played_register)
                else:
                    self._stack_pointer += 1

            if self._stack_pointer < 0 or self._stack_pointer >= len(self._instructions):
                return None


def decode_instructions(str_instructions):
    instructions = []
    for si in str_instructions:
        instructions.append(Instruction(si))

    return instructions


def read_input(fname):
    with open(fname, 'r') as f:
        return f.read().splitlines()


def solve_1(instructions):
    prog = Program(instructions)
    return prog.run()


def main():
    str_instructions = read_input('../input/instructions.dat')
    instructions = decode_instructions(str_instructions)

    recovered = solve_1(instructions)
    print("Answer 1: %d" % recovered)

    return True


if __name__ == '__main__':
    sys.exit(not main())
