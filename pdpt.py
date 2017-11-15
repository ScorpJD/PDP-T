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
        solution      (Solution): The problem current solution
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
        self.solution = None

################################### Solver ###################################

# # # # # # # # # # # # # # Constructive methods # # # # # # # # # # # # # # #

    def GRASP(self, function, k, maxIter, sol=None, **karg):
        """ Functional GRASP Meta heuristic

        This GRASP method is based on the original GRASP meta heuristic
        by Feo and Resende (1989).

        Runtime: O(maxIter)*O_{function}(sol)
        Additional space: O(1)

        Parameters:
           function  (lambda term): the original function.
           k                    (): GRASP parameter
           maxIter           (Int): maximum number of iterations
           sol                  (): initial solution

        TODO: check this method
        """
        soli = []
        for i in range(maxIter):
            soli.append(function(Sol=sol, **karg))  # NOTE: Need to be fix
        if 0 < k and k < maxIter:  # NOTE: Try Catch!
            return soli[random.randint(k)]

    def route_insert(self, S, v, a):
        """Find the optimal placement

        uses brute force search to find the optimal placement to insert the
        actions in a into the schedule S_v

        Runtime: O(n^3)
        Aditional space: O(n)

        Parameters:
           S
           V
           a
        """
        Sol = S.path[self.vehicles.index(v)]
        actMin = math.inf
        for i in range(len(Sol)):
            for j in range(i, len(Sol)):
                b = Sol[:i] + [a[0]] + Sol[i:j] + [a[1]] + Sol[j:]
                actCost = self.cost(b)
                if actCost < actMin:
                    Soli = b
                    actMin = actCost
        return Soli, actMin

    '''
    NOTE: Now there are a functional GRASP method.

    def GRASP_route_insert(self, S, v, a, k):
        """Find the optimal placement

        Find the optimal placement to insert the actions in `a` into the
        schedule `S` for the vehicle `v`, using brute froce with GRASP meta
        heuristic with coefficient `k`.

        Runtime: O(n^3)
        Additiona space: O(n)

        Parameters:
            S
            V
            a
            k
        """
        Sol = S.path[self.vehicles.index(v)]
        Soli = []
        for i in range(len(Sol)):
            for j in range(i, len(Sol)):
                b = Sol[:i] + [a[0]] + Sol[i:j] + Sol[j:]
                Soli.append((b, self.cost(b)))
        Soli.sort(key=lambda x: x[1])
        return Soli[random.randint(k)]
    '''

    def greedy_nt(self):
        """Solve PDP problem

        In the greedy approach, we iterate through every item m and vehicle v,
        insert the PICKUP(m) and DELIVER(m) actions into S^v at the points of
        lowest cost without rearranging the other actions. We then choose the
        vehicle/item pair (v, m) which increases the cost c(S) the least, and
        assign item m to vehicle v with the previously discovered best action
        insertion points. We repeat the process of greedily assigning items to
        vehicles until no unassigned items remain

        Runtime: O(|request|^2*|vehicles|*n^3)
        Additional space: O(|request|)
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

    def PARA(self, req, Sol):
        """ Solve PDP

        This constructive heuristic operates in a parallel and
        greedy way to insert a request. The initial solution Sol = {r (a)}
        is consisting of a single route containing only the starting point
        and the ending point of each route ( r (a) = {o1, o2}). Requests
        are then successively introduced into the tour of a vehicle
        offering the minimal increase of the cost of transport. If no
        vehicle can satisfy a request because of the non compliance with
        constraints (vehicle capacity, time windows, etc.), a new route is
        created to welcome the considered request.

        Runtime: O()
        Additional space: O()

        Parameters:
            req  ():
            sol  ():
        """
        costR = math.inf
        route = []
        for r in Sol.path:
            A = self.bestInsertion(r)
            if A < costR:
                costR = A
                route = r
            if costR != math.inf:
                bestInsertion = 2, 4
                route.insert(bestInsertion[0], req[0])
                route.insert(bestInsertion[1], req[1])
            else:
                rh = []
                costR, pos = self.bestInsetion(r, rh)
                rh.insert(costR, pos)
                Sol.path.append(rh)

    def TRANSSHIPMENT(self, R, Sol, T, MaxIter):
        """Add transferships to a PDP solution

        At each iteration, the transshipment heuristic is used to improve
        the PDP solution and obtain a solution to the PDPT. From the
        current PDP solution, each request (i, i+n) ∈ R; is removed from
        the solu- tion. Then, (i, i+n) is split into two different requests
        (i, et) and (st, i + n), where et and st are the inbound/outbound
        doors of a transshipment point t ∈ T. The best reinsertion cost of
        (i, i+n) in the solution is computed. The best insertion cost to
        insert (i, et) following by insertion of (st, i + n) in the solution
        is computed. The cost to insert (st, i+n) following by the insertion
        of (i, et) at their best position is computed. Between the three
        possibilities, the insertion or the reinsertions offering the
        minimum cost is performed.

        Runtime:
        Additional space:

        Parameters:
           R    ():
           Sol  ():
           T    ():
        """
        Tsol = Sol
        Tbest = Sol.f()
        for r in R:
            sol1 = Sol; sol1.path.remove(r)
            for t in T:
                sol2 = sol1; sol3 = sol1
                sol2 = self.PARA(r, sol2)
                sol3 = self.PARA((r[0], t), sol3) + self.PARA((t, r[1]), sol3)
                cost = min(sol2.f(), sol3.f())
                if Tbest > cost:
                    Tbest = cost
                    Tsol = sol2 if sol2.f() < sol3.f() else sol3
            Sol = Tsol
        return Tsol

        sol = Solution(floyd=self.floyd)
        sol1 = Solution(floyd=self.floyd)
        sol.distance = math.inf
        for i in range(MaxIter):
            for req in self.request:
                sol1 = self.PARA(req, sol1)
            sol1 = self.TRANSSHIPMENT(R, sol1, self.transfer_points)
            if sol1.f() < sol.f():
                sol = sol1
            sol1 = Solution(floyd=self.floyd)
        return sol

    def MULTISTART(self, MaxIter, lamb, seed=None, GRASP=False, k=0):
        """ Solve PDPT
        An hybrid because it combines several techniques and methods
        issued from different meta- heuristics such as: path relinking,
        variable neighbour-hood descent. Base on [1].
        Runtime:
        Additional Space:
        Parameters:
          MaxIter  ():
          seed     ():
          GRASP    ():
          k        ():
        References:
          [1] Takoudjou, R. T., Deschamps, J., & Dupas, R. (2012).
              A hybrid multistart heuristic for the pickup and delivery
              problem with and without transshipment. 9th International
              Conference on Modeling, Optimization & SIMulation.
        """
        Pool = None; Sol = None; Sol1 = None
        Sol1.distance = math.inf
        for i in range(MaxIter):
            for i in self.request:
                Sol1 = self.PARA((i, i+n), Sol1)
            if i < lamb:
                Pool.append(Sol1)
            self.UPDATE(Pool, Sol1)
            Sol1 = self.TRASSHIPMENT(i, Sol1, T)
            if Sol1.distance < Sol.distance:
                Sol = Sol1
            Sol1 = None
        return Sol

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
