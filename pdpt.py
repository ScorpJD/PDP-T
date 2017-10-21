#!/usr/bin/env python

from vehicle import Vehicle
import networkx as nx
import matplotlib.pyplot as plt
from Solution import Solution
import math
import random


class PDPT:
    """Pickup and delivery with Transfers Class.

    This class has the PDPT model.

    Attribuetes:
        N                  (int): The total numbers of vehicles in the instance
        time               (int): The actual time.
        vehicles          (list): List of problem vehicles
        transfer_points  (tuple): Transfer Points
        requests          (dict): The Problem request
        origins          (tuple): The origin point for each request
        destinations     (tuple): The destination point for each request
        routes        (nx.Graph): The Graph with all the posible routes
    """

    def __init__(self, number_of_vehicles=0, deposts=[], limit=[],
                 transfer_points=(), requests={}, graph=None):
        """init method for PDPT class

        This method construct an PDPT instance

        Parameters:
            number_of_vehicles  (int): The total numbers of vehicles in the
                                       instance.
            deposts            (list): The vehicles initial position, must have
                                       a length of N
            transfer_points   (tuple): Transfer Points
            requests           (dict): The Problem request
            graph          (nx.Graph): The Graph with all the posible routes
        """
        self.N = number_of_vehicles
        self.time = 0
        self.vehicles = []
        for i in range(self.N):
            self.vehicles.append(Vehicle(deposts))
        self.transfer_points = transfer_points
        self.requests = requests
        self.origins = tuple(requests.keys())
        self.destinations = tuple(requests.values())
        self.routes = graph
        self.floyd = nx.floyd_warshall_predecessor_and_distance(self.routes)

################################### Solver ###################################

# # # # # # # # # # # # # # Constructive methods # # # # # # # # # # # # # # #

    def cost(self, path):
        c = 0
        for i in range(len(path)-1):
            c += self.floyd[1][path[i]][path[i+1]]
        return c

    def GRASP(self, function, k, maxIter, sol=None):
        for i in range(maxIter):
            sol = self.funtion(sol, k)
        return sol

    def route_insert(self, S, v, a):
        """
        uses brute force search to find the optimal placement to insert the
        actions in a into the schedule S_v
        """
        Sol = S.path[self.vehicles.index(v)]
        actMin = math.inf
        for i in range(len(Sol)):
            for j in range(i, len(Sol)):
                b = Sol[:i] + [a[0]] + Sol[i:j] + [a[1]] + Sol[j:]
                if self.cost(b) < actMin:
                    Soli = b
                    actMin = self.cost(b)
        return Soli, actMin

    def GRASP_route_insert(self, S, v, a, k):
        """
        Find the optimal placement to insert the actions in `a` into the
        schedule `S` for the vehicle `v`, using brute froce with GRASP meta
        heuristic with coefficient `k`.
        """
        Sol = S.path[self.vehicles.index(v)]
        Soli = []
        for i in range(len(Sol)):
            for j in range(i, len(Sol)):
                b = Sol[:i] + [a[0]] + Sol[i:j] + Sol[j:]
                Soli.append((b, self.cost(b)))
        Soli.sort(key=lambda x: x[1])
        return Soli[random.randint(k)]

    def greedy_nt(self):
        """
        In the greedy approach, we iterate through every item m and vehicle v,
        insert the PICKUP(m) and DELIVER(m) actions into S^v at the points of
        lowest cost without rearranging the other actions. We then choose the
        vehicle/item pair (v, m) which increases the cost c(S) the least, and
        assign item m to vehicle v with the previously discovered best action
        insertion points. We repeat the process of greedily assigning items to
        vehicles until no unassigned items remain
        """
        S = Solution(floyd=self.floyd)
        S.path = self.request
        A = []
        while len(A) < len(self.request):
            actMin = math.inf
            So = []
            m = ()
            V = None
            for a in self.request:
                if a in A:
                    continue
                else:
                    for v in self.vehicles:
                        s, c = self.route_insert(S, v, a)
                        if c < actMin:
                            actMin = c; So = s; m = a; V = v
            S.path = self.route_insert(So, V, m)
            A = A.append(m)
        return S

    def GRASP_greedy_nt(self, k):
        S = Solution(floyd=self.floyd)
        S.path = self.request
        A = []
        while len(A) < len(self.request):
            Soli = []
            m = ()
            for a in self.request:
                if a in A:
                    continue
                else:
                    for v in self.vehicles:
                        s, c = self.route_insert(S, v, a)
                        Soli.append((c, s, v, a))
            Soli.sort(key=lambda x: x[0])
            index = random.randint(k)
            S.path = self.route_insert(*Soli[index][1:])
            A = A.append(Soli[index][-1])
        return S

    def MULTISTART(self, MaxIter, seed=None, GRASP=False, k=0):
        def PARA(req, sol):
            costR = math.inf
            route = []
            for r in sol.path:
                # The cost of the best insertion of req in r
                if A < costR:
                    costR = A
                    route = r
            if costR != math.inf:
                bestInsertion = 2, 4
                route.insert(bestInsertion[0], req[0])
                route.insert(bestInsertion[1], req[1])
            else:
                rh = []
                costR = 2  # insertion cost of req in rh
                # insert req at the best slot in rh
                sol.path.append(rh)

        def TRANSSHIPMENT(R, Sol, T):
            Tsol = Sol
            Tbest = Sol.f()
            for r in R:
                sol1 = Sol; sol1.path.remove(r)
                for t in T:
                    sol2 = sol1; sol3 = sol1
                    sol2 = PARA(r, sol2)
                    sol3 = PARA((r[0], t), sol3) + PARA((t, r[1]), sol3)
                    cost = min(sol2.f(), sol3.f())
                    if Tbest > cost:
                        Tbest = costnnnn
                        Tsol = sol2 if sol2.f() < sol3.f() else sol3
                Sol = Tsol
            return Tsol
        sol = Solution(floyd=self.floyd)
        sol1 = Solution(floyd=self.floyd)
        sol.distance = math.inf
        for i in range(MaxIter):
            R = random.shuffle(self.requests)
            for req in R:
                sol1 = PARA(req, sol1)
            sol1 = TRANSSHIPMENT(R, sol1, self.transfer_points)
            if sol1.f() < sol.f():
                sol = sol1
            sol1 = Solution(floyd=self.floyd)
        return sol

    def solve(self, method=None, solution=None):
        """solver for PDPT instance

        Parameters:
            method      (str): the solution method
            solution  (tuple): initial solution

        Return:
            * Moves Matrix
            * total distance
        """

        return eval("{f}(solution=solution)".format(f=method))


################################## FrontEnd ##################################

    def __str__(self):
        self.show()
        return '''This PDPT instance
        must to solve: {rq}
        The route trasfer points are {tra}
        '''.format(n=self.N, rq=self.requests,
                   tra=self.transfer_points)

    def show(self, pos=None, save=False):  # TODO print graph
        positions = list(map(lambda x: x.position, self.vehicles))
        cact = list(set(self.routes.nodes()) - set(positions))
        if not pos:
            pos = nx.spring_layout(self.routes)
        nx.draw_networkx_nodes(self.routes, pos,
                               nodelist=cact,
                               node_size=500)
        nx.draw_networkx_nodes(self.routes, pos,
                               nodelist=positions,
                               node_size=500, node_color='g')
        nx.draw_networkx_edges(self.routes, pos, width=3)
        nx.draw_networkx_labels(self.routes, pos, font_size=15,
                                font_family='sans-serif')
        plt.pppppppaxis('off')
        if save:
            name = input()
            plt.savefig(name + ".png")
        plt.show()
    # def pretty_print(self, solution = None, method = ):  TODO print_solution
