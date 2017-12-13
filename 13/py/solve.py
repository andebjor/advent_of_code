#!/usr/bin/env python3

import copy
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


def solve_1(firewall, abort_on_catch=False):
    severity = 0

    for l in range(firewall.get_length()):
        if firewall.catches(l):
            severity += l*firewall.get_depth(l)
            if abort_on_catch:
                return severity

        firewall.update()

    return severity


def solve_2(firewall):
    delay = 0
    while True:
        if not firewall.catches(0):
            severity = solve_1(copy.deepcopy(firewall), abort_on_catch=True)
            if severity == 0:
                return delay

        delay += 1
        firewall.update()

        if delay%100 == 0:
            print(delay)


def main():
    firewall_lines = read_input_lines('../input/firewall.dat')
    firewall = configure_firewall(firewall_lines)

    severity = solve_1(copy.deepcopy(firewall))
    print('Answer 1: %d' % severity)

    delay = solve_2(copy.deepcopy(firewall))
    print('Answer 2: %d' % delay)

    return True


if __name__ == '__main__':
    sys.exit(not main())
