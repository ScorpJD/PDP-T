import numpy as np
import networkx as nx

class Problem:
    def __init__(self, filePath):
        with open(filePath, r) as file:
            self.N = file.readline().split()[0]
            self.x = np.zeros(self.N)
            self.y = np.zeros(self.N)
            for lines in file.read().split('\n'):
                i, x, y, d, _, _, p, d = lines
                self.x[int(i)] = np.float(x)
                self.y[int(i)] = np.float(y)
