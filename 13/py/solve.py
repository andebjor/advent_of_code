#!/usr/bin/env python3

import re
import sys


class FLayer():
    def __init__(self, layer, depth):
        self.layer = layer
        self.depth = depth
        self.pos = 0
        self.go_down = True

    def advance(self):
        if self.go_down:
            if self.pos == self.depth-1:
                self.go_down = False
                self.pos -= 1
            else:
                self.pos += 1
        else:
            if self.pos == 0:
                self.go_down = True
                self.pos += 1
            else:
                self.pos -= 1


class Firewall():
    def __init__(self):
        self.layers = []

    def add_layer(self, fl):
        self._resize_if_needed(fl.layer)
        self.layers[fl.layer] = fl

#      def get_layer(self, i):
#          return self.layers[i]

    def update(self):
        for l in self.layers:
            if l is not None:
                l.advance()

    def catches(self, i):
        if self.layers[i] is not None:
            return self.layers[i].pos == 0
        return False

    def get_length(self):
        return len(self.layers)

    def get_depth(self, i):
        if self.layers[i] is not None:
            return self.layers[i].depth
        print('oops')
        return 0

    def _resize_if_needed(self, max_ind):
        if len(self.layers) <= max_ind:
            self.layers.extend([None] * (max_ind - len(self.layers) + 1))


def read_input_lines(fname):
    with open(fname, 'r') as f:
        return f.read().splitlines()


def configure_firewall(lines):
    firewall = Firewall()
    for l in lines:
        a = l.split(':')

        layer = int(a[0])
        depth = int(a[1])

        firewall.add_layer(FLayer(layer, depth))

    return firewall


def solve_1(firewall):
    severity = 0

    for l in range(firewall.get_length()):
        if firewall.catches(l):
            print('catch at %d' % l)
            print('depth %d' % firewall.get_depth(l))
            severity += l*firewall.get_depth(l)

        firewall.update()

    return severity


def main():
    fireall_lines = read_input_lines('../input/firewall.dat')
    firewall = configure_firewall(fireall_lines)

    severity = solve_1(firewall)
    print('Answer 1: %d' % severity)

    return True


if __name__ == '__main__':
    sys.exit(not main())
