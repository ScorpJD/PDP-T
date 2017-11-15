import numpy as np
import network as nx
from problem import Problem
from chromosome import Chromosome


# p = Problem("Instance/data/lrc101.txt", 10)
def genetic(P, Ninit):
    initlPopulation = [np.random.rand(P.N*len(P.G)) for _ in range(Ninit)]
