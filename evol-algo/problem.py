import numpy as np
import networkx as nx
import random


class Problem:
    def __init__(self, filePath, Ntr):
        with open(filePath, 'r') as file:
            self.N = int(file.readline().split()[0])
            self.transfer = [int(self.N*random.random()) for i in range(Ntr)]
            X = []
            Y = []
            D = []
            I = []
            for lines in file.read().split('\n'):
                if lines:
                    i, x, y, _, _, _, _, _, d = lines.split()
                    I.append(int(i))
                    X.append(np.float(x))
                    Y.append(np.float(y))
                    D.append(int(d))
            X = np.array(X)
            Y = np.array(Y)
            self.dist = np.abs(X - Y.reshape(Y.size, 1))
            self.G = nx.from_numpy_matrix(self.dist)
            self.request = dict(zip(I, D))

    def draw(self):
        nx.draw(self.G)
