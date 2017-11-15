import numpy as np
import network as nx
from problem import Problem
from chromosome import Chromosome


# p = Problem("Instance/data/lrc101.txt", 10)
def genetic(P, Ninit):
    population = np.array([Chromosome(np.random.rand(P.N*len(P.G)))
                           for _ in range(Ninit)])
    newGeneration = None
    while not stop(population, newGeneration):
        # Selection TODO: fixit
        population[P.dist.sum()/x.fitness > np.random.rand(population.size)]
        
        
