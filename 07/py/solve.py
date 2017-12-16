#!/usr/bin/env python3

import re
from statistics import median
import sys


class StrNode():
    def __init__(self, line):
        m = re.match(r'([a-z]+) \(([0-9]+)\)', line)
        self.name = m.groups()[0]
        self.weight = int(m.groups()[1])

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

    def calc_cum_weight(self):
        self.cum_weight = self.weight
        if len(self.children) > 0:
            for c in self.children:
                self.cum_weight += c.calc_cum_weight()

        return self.cum_weight


def read_input(fname):
    with open(fname, 'r') as f:
        return f.read().splitlines()


def build_nodes(node_lines):
    nodes = []
    for nl in node_lines:
        nodes.append(StrNode(nl))

    return nodes


def build_lazy_tree(str_nodes):
    leaves = [x for x in str_nodes if x.children is None]
    nodes  = [x for x in str_nodes if x.children is not None]

    tree = TreeNode(nodes[0].name, nodes[0].weight)
    nodes.pop(0)

    while len(nodes) > 0:
        for n in nodes:
            if tree.name in n.children:
                tmp = tree
                tree = TreeNode(n.name, n.weight)
                tree.add_child(tmp)
                break
        else:
            return tree


def get_str_node(name, str_nodes):
    for sn in str_nodes:
        if sn.name == name:
            return sn


def build_tree_rec(name, str_nodes):
    sn = get_str_node(name, str_nodes)

    tree = TreeNode(name, sn.weight)
    if sn.children is not None:
        for c in sn.children:
            tree.add_child(build_tree_rec(c, str_nodes))

    return tree


def print_tree(tree, lvl=0):
    node_str = ''
    for i in range(2*lvl):
        node_str += ' '

    node_str += tree.name + ': ' + str(tree.cum_weight)
    if len(tree.children) > 0:
        node_str += ': ('
        for c in tree.children:
            node_str += str(c.cum_weight) + ' '
        node_str += ')'

    for c in tree.children:
        print_tree(c, lvl+1)


def find_fault_leaf(tree, fault=None):
    if len(tree.children) > 0:
        if len(tree.children) > 2:
            cw = []
            for c in tree.children:
                cw.append(c.cum_weight)

            tw = median(cw)
            for c in tree.children:
                if c.cum_weight != tw:
                    return find_fault_leaf(c, tw - c.cum_weight)
            return tree.weight + fault
        else:  # two childs
            if tree.children[0].cum_weight + fault == tree.children[1].cum_weight:
                return find_fault_leaf(tree.children[0], fault)
            elif tree.children[1].cum_weight + fault == tree.children[0].cum_weight:
                return find_fault_leaf(tree.children[1], fault)
            else:
                return tree.weight + fault
    else:  # leaf
        return tree.weight + fault


def solve_2(tree):
    tree.calc_cum_weight()

    return find_fault_leaf(tree)


def main():
    node_lines = read_input('../input/nodes.dat')
    nodes = build_nodes(node_lines)

    tree = build_lazy_tree(nodes)
    print("Answer 1: '%s'" % tree.name)

    tree = build_tree_rec(tree.name, nodes)
    weight_diff = solve_2(tree)
    print("Answer 2: %d" % weight_diff)

    return True


if __name__ == '__main__':
    sys.exit(not main())
