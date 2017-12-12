#!/usr/bin/env python3

import sys


def read_input(fname):
    with open(fname, 'r') as f:
        return f.read().strip().split(',')


def categorize(coord_list):
    ret = {
        'n': 0,
        's': 0,
        'ne': 0,
        'nw': 0,
        'se': 0,
        'sw': 0,
    }

    for c in coord_list:
        ret[c] += 1

    return ret


def optmize(steps):
    if steps['ne'] > steps['sw']:
        steps['ne'] -= steps['sw']
        steps['sw'] = 0
    else:
        steps['sw'] -= steps['ne']
        steps['ne'] = 0

    if steps['nw'] > steps['se']:
        steps['nw'] -= steps['se']
        steps['se'] = 0
    else:
        steps['se'] -= steps['nw']
        steps['nw'] = 0

    if steps['n'] > steps['s']:
        steps['n'] -= steps['s']
        steps['s'] = 0
    else:
        steps['s'] -= steps['n']
        steps['n'] = 0

    if steps['sw'] > 0 and steps['se'] > 0:
        if steps['sw'] > steps['se']:
            steps['sw'] -= steps['se']
            steps['s'] += steps['se']
            steps ['se'] = 0
        else:
            steps['se'] -= steps['sw']
            steps['s'] += steps['sw']
            steps ['sw'] = 0


    return steps


def main():
    coords = read_input('../input/coords.dat')
    steps = categorize(coords)
    steps = optmize(steps)

    print('Answer 1: %s' % str(steps['sw'] + steps['s']))

    return True


if __name__ == '__main__':
    sys.exit(not main())
