#!/usr/bin/env python

# import Vehicle
import pdpt
import networkx as nx


def fromfile(path):
    with open(path, 'r') as file:
        N = int(file.readline())
        deposts = list(map(int, file.readline().split()))
        limit = tuple(map(int, file.readline().split()))
        transfer_points = tuple(map(int, file.readline().split()))
        Nrequest = int(file.readline())
        requests = {}
        for i in range(Nrequest):
            ox, ex, wx = map(int, file.readline().split())
            aux = ex, wx
            if ox in requests:
                requests[ox].append(tuple(aux))
            else:
                requests[ox] = [tuple(aux)]
        file.readline()
        graph = file.read().split("\n")
        graph = nx.nx.parse_edgelist(graph, nodetype=int,
                                     data=(('weight', float),))
    return pdpt.PDPT(number_of_vehicles=N,
                     deposts=deposts, limit=limit,
                     transfer_points=transfer_points,
                     requests=requests, graph=graph)


example = fromfile(path="example.pdpt")
print(example)
