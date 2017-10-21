#!/usr/bin/env python

# import Vehicle
import pdpt
import networkx as nx


def fromfile(path):
    with open(path, 'r') as file:
        N, b = file.readline().split()
        
