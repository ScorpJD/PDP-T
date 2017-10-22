#!/usr/bin/env python
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
        """ Check feasibility of the actual solution

        runtime: O(1)
        additional space: O(1)
        """
        return bool(self.request and self.path)

    def f(self):
        """
        Compute actual objective function value.

        runtime: O(|path|)
        aditional space: O(1)

        Note:
           There are many PDP-T formulation with different objective function,
           like, minimum travel time, if you want to solve a PDP-T problem with
           a distric objective function, change this fuction.
           (runtime and aditional space for this function and many other
            function has a strong objective function dependence.)
        """
        for i in range(len(self.path)):
            if i < len(self.path) - 1:
                self.distance += self.minDist[self.path[i]][self.path[i+1]]
