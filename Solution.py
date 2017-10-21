#!/usr/bin/env python
# import pdpt
import networkx as nx


# TODO Document this shit
class Solution():
    def __init__(self, instance, request=[], path=[], floyd=None):
        self.problem = instance
        self.distance = 0
        self.request = request
        self.path = []
        if not floyd:
            self.minPath, self.minDist =\
                    nx.floyd_warshall_predecessor_and_distance(instance.routes)
        else:
            self.minPath, self.minDist = floyd

    def f(self):
        for i in range(len(self.path)):
            if i < len(self.path) - 1:
                self.distance += self.minDist[self.path[i]][self.path[i+1]]
