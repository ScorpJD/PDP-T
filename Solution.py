#!/usr/bin/env python
# import pdpt
import networkx as nx


class Solution():
    """"Solution Class.

    This class store all information needed for new solution construction,
    also precompute some methods.

    Attribuetes:
       distance
       request
       path
       minPath
       minDist
    """
    def __init__(self, request=[], path=[], floyd=None, instance=None):
        self.request = request
        self.path = []
        if not floyd:
            self.minPath, self.minDist =\
                    nx.floyd_warshall_predecessor_and_distance(instance.routes)
        else:
            self.minPath, self.minDist = floyd
        self.f()

    def isFeasible(self):
        return bool(self.request)

    def f(self):
        """
        Compute actual objective function value.
        """
        for i in range(len(self.path)):
            if i < len(self.path) - 1:
                self.distance += self.minDist[self.path[i]][self.path[i+1]]
