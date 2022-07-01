#!/usr/bin/python3
# -*- mode: python; coding: utf-8 -*-

"""Topological sorting."""

from diseaz.algo.error import Error

import collections


class CycleError(Error):
    pass


class _NodeInfo(object):
    def __init__(self):
        self.n_parents = 0
        self.children = []

    def __repr__(self):
        return '{{n:{s.n_parents}, c:{s.children}}}'.format(s=self)


def sort(edges):
    """Topologically sort a list of nodes given edges (parent, child).

    Return a list of the elements in dependency order (parent before children).

    >>> sort([(1,2), (3,5), (4,6), (1,3), (1,4), (1,6), (2,4)])
    [1, 2, 3, 4, 5, 6]

    >>> sort([(1,2), (1,3), (2,4), (3,4), (5,6), (4,5)])
    [1, 2, 3, 4, 5, 6]

    >>> sort([(1,2), (2,3), (3,2), (2, 4)])
    Traceback (most recent call last):
    diseaz.algo.topsort.CycleError: ([1], [(2, 3), (2, 4), (3, 2)])

    >>> sort([(1, 2), (2, 3), (3, 4), (5, 6), (6, 5), (5, 3)])
    Traceback (most recent call last):
    diseaz.algo.topsort.CycleError: ([1, 2], [(3, 4), (5, 6), (5, 3), (6, 5)])
    """
    nodes = collections.defaultdict(_NodeInfo)
    for parent, child in edges:
        nodes[parent].children.append(child)
        nodes[child].n_parents += 1

    results = [k for k, v in nodes.items() if not v.n_parents]
    for r in results:
        p_node = nodes.pop(r)
        for c in p_node.children:
            c_node = nodes[c]
            c_node.n_parents -= 1
            if not c_node.n_parents:
                results.append(c)

    if nodes:
        cs = [(parent, child) for parent in nodes for child in nodes[parent].children]
        raise CycleError(results, cs)

    return results


if __name__ == '__main__':
    # Run the doctest tests.
    import doctest
    import diseaz.algo.topsort
    doctest.testmod(diseaz.algo.topsort)
