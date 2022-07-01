#!/usr/bin/python3
# -*- mode: python; coding: utf-8 -*-

import collections


def bfs(start, exits):
    """Breadth-first search.

    >>> g = {0:[1,3], 1:[2,5], 2:[], 3:[4,5], 4:[], 5:[]}
    >>> list(bfs([0], g.get))
    [0, 1, 3, 2, 5, 4]

    >>> list(bfs([1], g.get))
    [1, 2, 5]

    >>> list(bfs([1,3], g.get))
    [1, 3, 2, 5, 4]
    """
    visited = set(start)
    q = collections.deque(start)
    while q:
        node = q.popleft()
        yield node
        for e in exits(node):
            if e in visited:
                continue
            q.append(e)
            visited.add(e)


def dfs(start, exits):
    """Depth-first search.

    >>> g = {0:[1,3], 1:[2,5], 2:[], 3:[4,5], 4:[], 5:[]}
    >>> list(dfs([0], g.get))
    [0, 1, 2, 5, 3, 4]

    >>> list(dfs([1], g.get))
    [1, 2, 5]

    >>> list(dfs([1,3], g.get))
    [1, 2, 5, 3, 4]
    """
    visited = set(start)
    q = list(reversed(start))
    while q:
        node = q.pop()
        yield node
        for e in reversed(exits(node)):
            if e in visited:
                continue
            q.append(e)
            visited.add(e)


if __name__ == '__main__':
    # Run the doctest tests.
    import doctest
    import diseaz.algo.graph
    doctest.testmod(diseaz.algo.graph)
