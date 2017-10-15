from igraph import *
from math import *
from heapq import *
from random import *
from collections import deque
from node import *


class Graph(object):

    def __init__(self, N, max_degree):
        self.G = []
        self.N = N
        self.max_degree = max_degree
        self.Gn = []
        self.infected_group = []
        self.root = -1
        self.degsum=0

    # N = size of graph
    def construct_underlying_graph(self):
        # append nodes
        for i in range(0, self.N + 1):
            self.G.append(node(i))
        candidate = [i for i in range(2, self.N + 1)]
        for i in range(1, self.N + 1):
            rand_deg = randint(1, self.max_degree)
            for j in range(i + 1, self.N + 1):
                if (self.G[i].degree < rand_deg) and (j in candidate):
                    self.G[i].ch_append(j)
                    self.G[i].ne_append(j)
                    self.G[i].degree = self.G[i].degree + 1
                    self.G[j].ne_append(i)
                    self.G[j].parent = i
                    self.G[j].degree = self.G[j].degree + 1
                    temp = candidate.index(j)
                    candidate.pop(temp)
        return self.G

    def rootify(self, k):
        for i in self.G[k].neighbor:
                if i != self.Gn[k].parent and i in self.infected_group:
                    self.Gn[i].parent = k
                    self.Gn[i].ne_append(k)
                    self.Gn[k].ne_append(i)
                    self.Gn[k].ch_append(i)
                    self.rootify(i)

    def pick_source(self):
        real_source = randint(1, self.N)
        while len(self.G[source].neighbor)==1:
            real_source=randint(1,N)
        self.G[real_source].infected = True
        return real_source

        # n = max size of infected graph
    def spread_rumor(self, n):
        real_rumor_source = self.pick_source()
        self.infected_group = [real_rumor_source]

        susceptible_group=[]
        for i in self.G[source].neighbor:
            if len(self.G[i].neighbor)!=1:
                susceptible_group.append(i)
        
        num_end = 0  # count the number of end vertices
        true_num = 1  # count the real infected numbers

        for i in range(1, n):
            if (num_end < float(n)):
                ran_index = randint(1, len(susceptible_group)) - 1
                temp = susceptible_group[ran_index]
                self.infected_group.append(temp)
                self.G[temp].infected = True
                if len(self.G[temp].neighbor) == 1:  # if temp is a leaf, end number+1
                    num_end += 1
                for j in self.G[temp].neighbor:
                    if j not in self.infected_group:
                        susceptible_group.append(j)

                pop_item = susceptible_group.index(temp)
                susceptible_group.pop(pop_item)
                true_num += 1  # count the infected number
                # print infected_group

        n = true_num  # reset n

        # Pick a node from infected group as a root
        # Construct Gn as a rooted tree with the root
        #  root_index is from 0~n-1
        root_index = randint(0, len(self.infected_group) - 1)
        root = self.infected_group[root_index]
        self.root = root
        self.Gn = [node(0)]  # Gn is from 1~n   Gn[0] is null vertex

        for i in range(1, self.N + 1):  # Set Gn as large as G, but with uninfected node=0
            if i in self.infected_group:
                self.Gn.append(node(i))
            else:
                self.Gn.append(node(0))

        self.rootify(root)   # change Gn to a rooted tree
        self.child_sum(root)  # compute t^root_v for each node v

        for i in range(1, self.N + 1):  # Set degree of nodes in Gn
            self.Gn[i].degree = len(self.Gn[i].neighbor)

        return real_rumor_source, self.infected_group

    # def return_G(self) :
    #   return self.G

    # function to compute child sum
    def child_sum(self, k):
        temp_sum = 0
        if len(self.Gn[k].children) > 0:
            for i in self.Gn[k].children:
                temp_sum = temp_sum + self.child_sum(i)
                self.Gn[k].descendant_num = 1 + temp_sum
            return 1 + temp_sum
        else:
            self.Gn[k].descendant_num = 1
            return 1

    # function to compute rumor centrality
    def rumor_center1(self, k):
        temp_mul = 1
        if len(self.Gn[k].children) > 0:
            for i in self.Gn[k].children:
                temp_mul = temp_mul * self.rumor_center1(i)
                if k == self.root:
                    self.Gn[k].rc = factorial(10) / (self.Gn[k].descendant_num * temp_mul)
            return self.Gn[k].descendant_num * temp_mul
        else:
            return 1

    def rumor_center2(self, k):
        for i in self.Gn[k].children:
            self.Gn[i].rc = self.Gn[k].rc * (self.Gn[i].descendant_num / (10 - float(self.Gn[i].descendant_num)))
            self.rumor_center2(i)

    def rumor_centrality(self, k):
        self.rumor_center1(k)
        self.rumor_center2(k)
        return self.Gn[k].rc

    # function to sort neighbors according to degree
    def deg_sort(self, i, Reverse):
        return sorted(self.Gn[i].neighbor, key=lambda v: (self.Gn[v].degree, self.Gn[v].descendant_num), reverse=Reverse)

    # function to bfs and dfs
    def bfs(self, source, Type):
            path = []
            q = deque([source])
            possibility = 1
            neighbor_num = 0
            while q:
                    current = q.popleft()
                    path.append(current)
                    true_neighbor=self.G[current].neighbor
                    if(Type == 1):  # nature order
                            temp_neighbor = self.Gn[current].neighbor
                    elif(Type == 2):  # min order
                            temp_neighbor = self.deg_sort(current, False)
                    elif(Type == 3):  # max order
                            temp_neighbor = self.deg_sort(current, True)
                    if neighbor_num==0:
                            neighbor_num=neighbor_num+len(true_neighbor)
                    else:
                            neighbor_num=neighbor_num+len(true_neighbor)-2
                    if neighbor_num != 0:
                            possibility = possibility / float(neighbor_num)
                    # print(possibility)
                    for i in temp_neighbor:
                            if i not in path:
                                    q.append(i)
            return path, possibility

    def dfs(self, Type,k, path=[], possibility=1):
        path.append(k)
        if self.degsum == 0:
            self.degsum += self.G[k].degree
        else:
            self.degsum += self.G[k].degree - 2
        possibility /= float(self.degsum)
        if (Type == 1):  # nature order
            temp_neighbor = self.Gn[k].neighbor
        elif (Type == 2):  # min order
            temp_neighbor = self.deg_sort(k, False)
        elif (Type == 3):  # max order
            temp_neighbor = self.deg_sort(k, True)
        for current in self.Gn[k].neighbor:
            if current not in path:
                path, possibility = self.dfs(current, Type,path, possibility)
        return path, possibility

    def max_deg_search(self, k, path=[], neighbor_heap=[], possibility=1,degsum=0):
        path.append(k)
        if degsum==0:
            self.degsum+=self.G[k].degree
        else:
            degsum+=self.G[k].degree-2
        for i in self.Gn[k].neighbor:
            if i not in path:
                heappush(neighbor_heap, (-self.G[i].degree, -self.Gn[i].descendant_num, i))
        if neighbor_heap:
            possibility = possibility / float(degsum)
            path, possibility = self.max_deg_search((heappop(neighbor_heap))[2], path, neighbor_heap, possibility,degsum)
        return path, possibility

    def min_deg_search(self, k, path=[], neighbor_heap=[], possibility=1,degsum=0):
        path.append(k)
        if degsum==0:
            degsum+=self.G[k].degree
        else:
            degsum+=self.G[k].degree-2
        for i in self.Gn[k].neighbor:
            if i not in path:
                heappush(neighbor_heap, (self.G[i].degree, self.Gn[i].descendant_num, i))
        if neighbor_heap:
            possibility = possibility / float(degsum)
            path, possibility = self.min_deg_search((heappop(neighbor_heap))[2], path, neighbor_heap, possibility,degsum)
        return path, possibility
