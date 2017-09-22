from igraph import *
from math import *
from heapq import *
from random import *
from collections import deque

# irregular, d is the max degree for the nodes
d = 3
# Size of G : |G|=N
N = 50  # step
# Size of Infection Group G_n
n = 10
# a global variable that can increase every search call, calculate sum of
# degree
degsum = 0

# function to root the tree


def rootify(k):
    for i in G[k].neighbor:
        if i != Gn[k].parent and i in infected_group:
            Gn[i].ne_append(k)
            Gn[k].ne_append(i)
            if Gn[i].parent == 0:
                Gn[i].parent = k
                Gn[k].ch_append(i)
                rootify(i)


def rootify2(k):
    for i in Gr[k].neighbor:
        if i != Gr[k].parent:
            Gr[i].parent = k
            Gr[k].ch_append(i)
            rootify2(i)
# mst functions to simplify the infected graph as minimum spanning tree
# elimate the nodes with degree 2


def record_edges(k):
    Gn[k].visited = 1
    for i in G[k].neighbor:
        if i in infected_group:
            if Gn[i].visited == 0:
                heappush(edge_heap, (1, (i, k)))
                record_edges(i)


# mst standard functions
p = dict()


def find(x):
    if x == p[x]:
        return x
    else:
        p[x] = find(p[x])
        return p[x]


def union(x, y):
    p[find(x)] = find(y)


def add_edge(length, v1, v2):
    print(v1, v2, length)
    if length == 1:
        Gr[v1].ne_append(v2)
        Gr[v2].ne_append(v1)

    elif length == 2:
        Gr.append(node(len(Gr)))
        Gr[v1].ne_append(len(Gr) - 1)
        Gr[len(Gr) - 1].ne_append(v1)
        Gr[v2].ne_append(len(Gr) - 1)
        Gr[len(Gr) - 1].ne_append(v2)
    else:
        Gr.append(node(len(Gr)))
        Gr[v1].ne_append(len(Gr) - 1)
        Gr[len(Gr) - 1].ne_append(v1)
        while length > 2:
            Gr.append(node(len(Gr)))
            Gr[len(Gr) - 1].ne_append(len(Gr) - 2)
            Gr[len(Gr) - 2].ne_append(len(Gr) - 1)
            length = length - 1
        Gr[v2].ne_append(len(Gr) - 1)
        Gr[len(Gr) - 1].ne_append(v2)


def kruskal():
    for i in infected_group:
        p[i] = i
    while(edge_heap):
        length, (v1, v2) = heappop(edge_heap)
        if find(v1) != find(v2):
            union(v1, v2)
            # print("addedge",v1,v2)
            add_edge(length, v1, v2)
        else:
            print("cant union", v1, v2)
# function to compute child sum


def child_sum(k):
    temp_sum = 0
    if len(Gr[k].children) > 0:
        for i in Gr[k].children:
            temp_sum = temp_sum + child_sum(i)
        Gr[k].descendant_num = 1 + temp_sum
        return 1 + temp_sum
    else:
        Gr[k].descendant_num = 1
        return 1

# function to compute rumor centrality


def rumor_center1(k):
    temp_mul = 1
    if len(Gr[k].children) > 0:
        for i in Gr[k].children:
            temp_mul = temp_mul * rumor_center1(i)
            if k == root:
                Gr[k].rc = factorial(n) / (Gr[k].descendant_num * temp_mul)
        return Gr[k].descendant_num * temp_mul
    else:
        return 1


def rumor_center2(k):
    for i in Gr[k].children:
        Gr[i].rc = Gr[k].rc * (Gr[i].descendant_num /
                               (n - float(Gr[i].descendant_num)))
        rumor_center2(i)

# function to sort neighbors according to degree


def deg_sort(i, Reverse):
    return sorted(Gn[i].neighbor, key=lambda v: (Gn[v].degree, Gn[v].descendant_num), reverse=Reverse)

# function to bfs and dfs


def bfs(source, Type):
    path = []
    q = deque([source])
    possibility = 1
    neighbor_num = 0
    while q:
        current = q.popleft()
        path.append(current)
        true_neighbor = G[current].neighbor
        if(Type == 1):  # nature order
            temp_neighbor = Gn[current].neighbor
        elif(Type == 2):  # min order
            temp_neighbor = deg_sort(current, False)
        elif(Type == 3):  # max order
            temp_neighbor = deg_sort(current, True)
        if neighbor_num == 0:
            neighbor_num = neighbor_num + len(true_neighbor)
        else:
            neighbor_num = neighbor_num + len(true_neighbor) - 2
        if neighbor_num != 0:
            possibility = possibility / float(neighbor_num)
        # print(current,G[current].degree,Gn[current].degree,neighbor_num,possibility)
        for i in temp_neighbor:
            if i not in path:
                q.append(i)
    return path, possibility


def dfs(source, path=[], possibility=1):
    path.append(source)
    global degsum
    if degsum == 0:
        degsum += G[source].degree
    else:
        degsum += G[source].degree - 2
    possibility /= float(degsum)
    # print(possibility)
    for current in Gn[source].neighbor:
        if current not in path:
            path, possibility = dfs(current, path, possibility)
    return path, possibility


# function for heurisitic1
def min_deg_search(source, path=[], neighbor_heap=[], possibility=1, degsum=0):
    path.append(source)
    if degsum == 0:
        degsum += G[source].degree
    else:
        degsum += G[source].degree - 2
    for i in Gn[source].neighbor:
        if i not in path:
            heappush(neighbor_heap, (G[i].degree, Gn[i].descendant_num, i))
    if neighbor_heap:
        possibility = possibility / float(degsum)
        # print(possibility)
        # print(neighbor_heap)
        path, possibility = min_deg_search(
            (heappop(neighbor_heap))[2], path, neighbor_heap, possibility, degsum)
    return path, possibility


def max_deg_search(source, path=[], neighbor_heap=[], possibility=1, degsum=0):
    path.append(source)
    if degsum == 0:
        degsum += G[source].degree
    else:
        degsum += G[source].degree - 2
    for i in Gn[source].neighbor:
        if i not in path:
            heappush(neighbor_heap, (-G[i].degree, -Gn[i].descendant_num, i))
    if neighbor_heap:
        possibility = possibility / float(degsum)
        # print(possibility)
        # print(neighbor_heap)
        path, possibility = max_deg_search(
            (heappop(neighbor_heap))[2], path, neighbor_heap, possibility, degsum)
    return path, possibility


def get_max_p(type):
    max_p = 0
    max_path = []
    for i in infected_group:
        if type == 1:
            global degsum
            degsum = 0
            temppath, p = dfs(i, path=[], possibility=1)
        elif type == 2:
            temppath, p = bfs(i, 1)
        elif type == 3:
            temppath, p = bfs(i, 2)
        elif type == 4:
            temppath, p = bfs(i, 3)
        elif type == 5:
            temppath, p = max_deg_search(
                i, path=[], neighbor_heap=[], possibility=1)
        else:
            temppath, p = min_deg_search(
                i, path=[], neighbor_heap=[], possibility=1)

        if p > max_p:
            max_p = p
            max_path = temppath
    return max_path, max_p
# define minimum spanning tree to transfer the graph with cycle to tree


# Class of node with number,children,parent,state,degree,neighbor

class node(object):

    def __init__(self, num):
        self.num = num
        self.children = []
        self.parent = 0
        self.infected = False
        self.degree = 0
        self.max_degree = 0
        self.redundant_deg = 0
        self.neighbor = []
        self.rc = 1
        self.descendant_num = 0
        self.prob_Gn = 0
        self.end_vertex_num = 0
        self.root_path = []
        self.hop = 0
        self.visited = 0

    def ch_append(self, child):
        self.children.append(child)

    def ne_append(self, neighbor):
        self.neighbor.append(neighbor)


# Generating random tree with n vertices under d-irregular tree

# STEP 1 : construct the base graph G
G = []
for i in range(0, N + 1):
    G.append(node(i))

# candidate=[i for i in range(2,N+1)]

# for i in range(1,N+1):
#       rand_deg=randint(1,d)
#       for j in range(i+1,N+1):
#               if (G[i].degree < rand_deg) and (j in candidate):
#                       G[i].ch_append(j)
#                       G[i].ne_append(j)
#                       G[i].degree=G[i].degree+1
#                       G[j].ne_append(i)
#                       G[j].parent=i
#                       G[j].degree=G[j].degree+1
#                       temp=candidate.index(j)
#                       candidate.pop(temp)

# generate graph G which is d-irregular and contains cycle[ without self cycle
for i in range(1, N + 1):
    rand_deg = randint(1, d)
    G[i].max_degree = rand_deg
for i in range(1, N + 1):
    while (G[i].degree + G[i].redundant_deg < G[i].max_degree):
        rand_j = randint(1, N)
        if (rand_j not in G[i].children) and (G[rand_j].degree < G[rand_j].max_degree):
            if rand_j != i:
                G[i].ch_append(rand_j)
                G[i].ne_append(rand_j)
                G[i].degree = G[i].degree + 1
                G[rand_j].ne_append(i)
                G[rand_j].parent = i
                G[rand_j].degree = G[rand_j].degree + 1
            else:
                G[i].redundant_deg = G[i].redundant_deg + 1

# STEP 2 : Randomly pick a node as the source
source = randint(1, N)
G[source].infected = True

# STEP 3 : Simulate the spreading to n nodes
infected_group = [source]
end_vertices = []
susceptible_group = list(G[source].neighbor)

num_end = 0  # count the number of end vertices
true_num = 1  # count the real infected numbers

for i in range(1, n):
    if (num_end < float(n)):
        ran_index = randint(0, len(susceptible_group) - 1)
        temp = susceptible_group[ran_index]
        if temp in infected_group:
            continue
        infected_group.append(temp)
        G[temp].infected = True
        if len(G[temp].neighbor) == 1:  # if temp is a leaf, end number+1
            num_end += 1
        for j in G[temp].neighbor:
            if j not in infected_group:
                susceptible_group.append(j)

        pop_item = susceptible_group.index(temp)
        susceptible_group.pop(pop_item)
        true_num += 1  # count the infected number
        # print infected_group

n = true_num      # reset n


# Pick a node from infected group as a root Construct Gn as a rooted tree
# with the root
root_index = randint(0, len(infected_group) - 1)  # root_index is from 0~n-1
root = infected_group[root_index]
Gn = [node(0)]                   # Gn is from 1~n   Gn[0] is null vertex


for i in range(1, N + 1):  # Set Gn as large as G, but with uninfected node=0
    if i in infected_group:
        Gn.append(node(i))
    else:
        Gn.append(node(0))

rootify(root)  # change Gn to a rooted tree


for i in range(1, N + 1):  # Set degree of nodes in Gn
    Gn[i].degree = len(Gn[i].neighbor)

# Gr is the simplified graph,gr is its index
Gr = [node(0)]
edge_heap = []
record_edges(root)
for i in range(1, N + 1):
    if i in infected_group:
        Gr.append(node(i))
    else:
        Gr.append(node(0))
kruskal()
rootify2(root)
child_sum(root)  # compute t^root_v for each node v


# Plot the Network by iGraph
Gp = Graph()
Gp.add_vertices(N)

for i in range(1, N + 1):
    for j in range(1, N + 1):
        if j in G[i].children:
            Gp.add_edges([(i - 1, j - 1)])  # Gp is started from node "0"

for i in range(1, N + 1):
    Gp.vs[i - 1]["num"] = i
    if G[i].infected is True:
        if G[i].degree == 1:
            Gp.vs[i - 1]["state"] = "infected"  # highlight the end vertex
            Gp.vs[i - 1]["color"] = "yellow"
        else:
            Gp.vs[i - 1]["state"] = "infected"
            Gp.vs[i - 1]["color"] = "pink"
    else:
        Gp.vs[i - 1]["state"] = "uninfected"
        Gp.vs[i - 1]["color"] = "white"
    if i == source:
        Gp.vs[i - 1]["color"] = "orange"

Gp.vs["label"] = Gp.vs["num"]


# Point out the Rumor Center and change the color of the node

rumor_center1(root)
rumor_center2(root)
max_rc = 0
max_node = 0
for i in range(1, N + 1):
    if Gr[i].rc > max_rc:
        max_rc = Gr[i].rc
        max_node = i

Gp.vs[max_node - 1]["color"] = "red"

# ----------------------------------
# Set the output style
layout = Gp.layout_reingold_tilford_circular()
# layout=Gp.layout_grid_fruchterman_reingold()


plot(Gp, layout=layout, bbox=(500, 500))
print("root", root)
print("source", source)
print(infected_group)
# print ('dfs\n',dfs(root,path=[]))
# print ('natural bfs\n',bfs(root,1))
# print ('ascending bfs\n',bfs(root,2))
# print ('descending bfs\n',bfs(root,3))
# print ('max_deg_search \n',max_deg_search(root,path=[],neighbor_heap=[],possibility=1))
# print ('min_deg_search \n',min_deg_search(root,path=[],neighbor_heap=[],possibility=1))

print(get_max_p(1))
print(get_max_p(2))
print(get_max_p(3))
print(get_max_p(4))
print(get_max_p(5))
