#!/usr/bin/env python3

import re
import sys


class SendInterupt(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value


class ReceiveInterupt(Exception):
    def __init__(self, register):
        super().__init__()
        self.register = register


class TerminatedInterupt(Exception):
    pass


class Instruction:
    def __init__(self, str_instruction):
        m = re.match(r'([a-z]{3}) ([a-z0-9]) ?([-a-z0-9]+)?', str_instruction)

        operation = m.groups()[0]
        self._operation = operation
        if operation == 'snd' or operation == 'rcv':
            self._op_1 = m.groups()[1]
        else:
            self._op_1 = m.groups()[1]
            self._op_2 = m.groups()[2]

    def apply(self, reg):
        if self._operation == 'rcv':
            raise ReceiveInterupt(self._op_1)

        if self._operation == 'snd':
            raise SendInterupt(reg.get(self._op_1))

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
    def __init__(self, instructions, my_id):
        self._instructions = instructions
        self._register = Register()
        self._stack_pointer = 0

        self._register.set('p', my_id)

    def run(self):
        while True:
            try:
                self._stack_pointer += self._instructions[self._stack_pointer].apply(self._register)
            except (ReceiveInterupt, SendInterupt):
                self._stack_pointer += 1
                raise
            finally:
                if self._stack_pointer < 0 or self._stack_pointer >= len(self._instructions):
                    raise TerminatedInterupt()

    def set_register(self, register, value):
        self._register.set(register, value)


def decode_instructions(str_instructions):
    instructions = []
    for si in str_instructions:
        instructions.append(Instruction(si))

    return instructions


def read_input(fname):
    with open(fname, 'r') as f:
        return f.read().splitlines()


def solve_2(instructions):
    prog0 = Program(instructions, 0)
    prog1 = Program(instructions, 1)

    prog1_nsends = 0
    prog0_sq = []
    prog1_sq = []
    prog0_want_recv = False
    prog1_want_recv = False
    while True:
        # step prog 0
        if prog0 is not None:
            if not prog0_want_recv:
                try:
                    prog0.run()
                except SendInterupt as e:
                    prog0_sq.append(e.value)
                except ReceiveInterupt as e:
                    prog0_want_recv = True
                    prog0_rec_register = e.register
                except TerminatedInterupt:
                    prog0 = None
            elif len(prog1_sq) > 0:
                prog0.set_register(prog0_rec_register, prog1_sq[0])
                prog1_sq = prog1_sq[1:]
                prog0_want_recv = False

        # step prog 1
        if not prog1_want_recv:
            try:
                prog1.run()
            except SendInterupt as e:
                prog1_sq.append(e.value)
                prog1_nsends += 1
            except ReceiveInterupt as e:
                prog1_want_recv = True
                prog1_rec_register = e.register
            except TerminatedInterupt:
                print('exit 1')
                return prog1_nsends
        elif len(prog0_sq) > 0:
            prog1.set_register(prog1_rec_register, prog0_sq[0])
            prog0_sq = prog0_sq[1:]
            prog1_want_recv = False

        if (
                prog0_want_recv and len(prog1_sq) == 0 and
                prog1_want_recv and len(prog0_sq) == 0):
            return prog1_nsends

        if (
                prog0 is None and
                prog1_want_recv and len(prog0_sq) == 0):
            return prog1_nsends


def main():
    str_instructions = read_input('../input/instructions.dat')
    instructions = decode_instructions(str_instructions)

    times = solve_2(instructions)
    print("Answer 2: %d" % times)

    return True


if __name__ == '__main__':
    sys.exit(not main())
