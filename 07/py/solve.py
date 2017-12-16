#!/usr/bin/env python3

import re
import sys


class StrNode():
    def __init__(self, line):
        m = re.match(r'([a-z]+) \(([0-9]+)\)', line)
        self.name = m.groups()[0]
        self.weight = m.groups()[1]

        if '->' in line:
            m = re.search(r'-> ([a-z, ]+)', line)
            self.children = m.groups()[0].split(', ')
        else:
            self.children = None

    def __str__(self):
        ret = 'name: %s\n' % self.name
        ret = '%sweight: %s\n' % (ret, self.weight)
        if self.children is not None:
            ret = '%s   ' % ret
            for c in self.children:
                ret = '%s%s, ' % (ret, c)
            ret = '%s\n' % ret

        return ret


class TreeNode():
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.children = []

    def add_child(self, child):
        self.children.append(child)


def read_input(fname):
    with open(fname, 'r') as f:
        return f.read().splitlines()


def build_nodes(node_lines):
    nodes = []
    for nl in node_lines:
        nodes.append(StrNode(nl))

    return nodes


def build_tree(str_nodes, lazy=True):
    leaves = [x for x in str_nodes if x.children is None]
    nodes  = [x for x in str_nodes if x.children is not None]

    tree = TreeNode(nodes[0].name, nodes[0].weight)
    nodes.pop(0)

    if lazy:
        while len(nodes) > 0:
            for n in nodes:
                if tree.name in n.children:
                    tmp = tree
                    tree = TreeNode(n.name, n.weight)
                    tree.add_child(tmp)
                    break
            else:
                return tree

    else:
        raise NotImplementedError('cannot build full tree')


def main():
    node_lines = read_input('../input/nodes.dat')
    nodes = build_nodes(node_lines)
    tree = build_tree(nodes)

    print("Answer 1: %s" % tree.name)

    return True


if __name__ == '__main__':
    sys.exit(not main())
