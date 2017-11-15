import numpy as np
import networkx as nx
# import problem
# import nucleosome


class Chromosome:
    def __init__(self, nucList=np.array([]), gen=np.array([]), problem=None):
        self.N = problem.N
        if nucList.size:
            self.sol = amap(lambda x: x.sol, nucList)
            self.key = amap(lambda x: x.key, nucList)
            self.gen = self.key.flatten()
            self.path = amap(lambda x: x.path, nucList)
        else:
            self.gen = gen
            self.key = gen.reshape(self.N, int(len(gen)/self.N))
            self.sol = self.reconstruct()
            self.path = self.pathConstruction()
        self.floyd = nx.floyd_warshall_predecessor_and_distance(problem.G)
        self.fitness = np.inf
        self.fit()

    def reconstruct(self):
        pos = 1
        sol = np.array(self.key, copy=True)
        if self.N == 1:
            for i in range(len(sol)):
                if sol[i]:
                    sol[i] = pos
                    pos += 1
        else:
            for i in range(sol.shape[0]):
                pos = 1
                for j in range(sol.shape[1]):
                    if sol[i][j]:
                        sol[i][j] = pos
                        pos += 1
        return sol.astype(int)

    def pathConstruction(self):
        path = list(self.sol)
        for i in range(len(path)):
            path[i] = path[i].argsort()[(path[i] == 0).sum():] + 1
        return np.array(path)

    def fit(self):
        self.fitness = np.inf


def amap(func, *args):
    args = np.broadcast(None, *args)
    res = np.array([func(*arg[1:]) for arg in args])
    shape = args.shape + res.shape[1:]
    return res.reshape(shape)
