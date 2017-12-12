#!/usr/bin/env python3

import re
import sys


def read_input_lines(fname):
    with open(fname, 'r') as f:
        return f.read().splitlines()


def parse_prog(prog_str):
    m = re.match(r'([0-9]+) <-> ([0-9, ]+)', prog_str)
    return (m.groups()[0], m.groups()[1].split(','))


def categorize(pipe_list):
    ret = []
    for prog in pipe_list:
        (p, cons) = parse_prog(prog)
        ret.append(cons)

    return ret


def get_reach(conn, from_ind):
    can_reach = {from_ind: 0}

    while True:  # loop until break
        new_reach = []
        for p in can_reach.keys():  # over all progs reach until now
            if can_reach[p] == 0:   # if 0: not handled
                for n in [int(x) for x in conn[p]]:   # all neighnours to prog p
                    if n not in can_reach:  # add to list if not present
                        new_reach.append(n)
                can_reach[p] = 1
        if len(new_reach) == 0:
            break
        else:
            for n in new_reach:
                can_reach[n] = 0

    return can_reach




def main():
    pipe_lines = read_input_lines('../input/pipes.dat')
    pipe_connections = categorize(pipe_lines)

    reach = get_reach(pipe_connections, 0)

    print('Answer 1: %s' % len(reach.keys()))

    return True


if __name__ == '__main__':
    sys.exit(not main())
