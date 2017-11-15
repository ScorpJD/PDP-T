import numpy as np
import networkx as nx

class Nucleosome:
    def __init__(self, sol=np.array([]), key=np.array([])):
        self.sol = self.reconstruct(sol, key)
        self.key = self.randkey(key)
        self.path = np.argsort(self.sol)[(self.sol==0).sum():] + 1
    
    def reconstruct(self, sol, key):
        if sol.any():
            return sol
        pos = 1
        sol = np.array(key, copy=True)
        for i in range(len(sol)):
            if sol[i]:
                sol[i] = pos
                pos += 1
        return sol.astype(int)
            
    def randkey(self, key):
        if key.size:
            return key
        return (self.sol != 0)*4*np.exp(-self.sol)/(1 + np.exp(-self.sol))**2    

