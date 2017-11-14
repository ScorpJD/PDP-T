import numpy as np
import networkx as nx

class Nucleosome:
    def __init__(self, sol = None, key = None):
        self.sol = self.reconstruct(sol, len(key))
        self.key = self.randkey(sol, key)
        self.path = self.sol[self.sol>0].argsort()[::-1]

    def reconstruct(self, sol, key):
        if sol.size:
            return np.array(sol)
        pos = 1
        sol = np.array(key, copy=True)
        for i in range(len(sol)):
            if sol[i]:
                sol[i] = pos
                pos += 1
        return sol.astype(int)

    def randkey(self, sol, key):
        if key:
            return key
        return (sol != 0)*4*np.exp(-sol)/(1 + np.exp(-x))**2
