from igraph import *
from math import *
from heapq import *
from random import *
from collections import deque

#irregular, d is the max degree for the nodes
d=3
# Size of G : |G|=N
N=50 #step
# Size of Infection Group G_n
n=10
#a global variable that can increase every search call, calculate sum of degree
degsum=0

#function to root the tree
def rootify(k):
    for i in G[k].neighbor:
        if i!=Gn[k].parent and i in infected_group:
            Gn[i].parent=k
            Gn[i].ne_append(k)
            Gn[k].ne_append(i)
            Gn[k].ch_append(i)
            rootify(i)

#function to compute child sum

def child_sum(k):
    temp_sum=0
    if len(Gn[k].children)>0:
        for i in Gn[k].children:
            temp_sum=temp_sum+child_sum(i)
        Gn[k].descedant_num=1+temp_sum
        return 1+temp_sum
    else:
        Gn[k].descedant_num=1
        return 1

#function to compute rumor centrality

def rumor_center1(k):
    temp_mul=1
    if len(Gn[k].children)>0:
        for i in Gn[k].children:
            temp_mul=temp_mul*rumor_center1(i)
            if k==root :
                Gn[k].rc=factorial(n)/(Gn[k].descedant_num*temp_mul)
        return Gn[k].descedant_num*temp_mul
    else:
        return 1

def rumor_center2(k):
    for i in Gn[k].children:
        Gn[i].rc=Gn[k].rc*(Gn[i].descedant_num/(n-float(Gn[i].descedant_num)))
        rumor_center2(i)

#function to sort neighbors according to degree
def deg_sort(i,Reverse):
    return sorted(Gn[i].neighbor,key=lambda v:(G[v].degree,Gn[v].descedant_num),reverse=Reverse)

#function to bfs and dfs
def bfs(source,Type):
    path = []
    q = deque([source])
    possibility=1
    neighbor_num=0
    while q:
        current=q.popleft()
        path.append(current)
        true_neighbor=G[current].neighbor
        if(Type == 1):#nature order
            temp_neighbor=Gn[current].neighbor
        elif(Type == 2):#min order
            temp_neighbor=deg_sort(current,False)
        elif(Type == 3):#max order
            temp_neighbor=deg_sort(current,True)
        if neighbor_num==0:
            neighbor_num=neighbor_num+len(true_neighbor)
        else:
            neighbor_num=neighbor_num+len(true_neighbor)-2
        if neighbor_num!=0:
            possibility=possibility/float(neighbor_num)
        #print(current,G[current].degree,Gn[current].degree,neighbor_num,possibility)
        for i in temp_neighbor:
            if i not in path:
                q.append(i)
    return path,possibility

def dfs(source, path=[],possibility=1):
    path.append(source)
    global degsum
    if degsum==0:
        degsum+=G[source].degree
    else:
        degsum+=G[source].degree-2
    possibility/=float(degsum)
    #print(source,G[source].degree,Gn[source].degree,degsum,possibility)
    for current in Gn[source].neighbor:
        if current not in path:
            path,possibility=dfs(current, path,possibility)
    return path,possibility


# function for heurisitic1
def min_deg_search(source,path=[],neighbor_heap=[],possibility=1,degsum=0):
    path.append(source)
    if degsum==0:
        degsum+=G[source].degree
    else:
        degsum+=G[source].degree-2
    for i in Gn[source].neighbor:
        if i not in path:
            heappush(neighbor_heap,(G[i].degree,Gn[i].descedant_num,i))
    if neighbor_heap:
        possibility=possibility/float(degsum)
        #print(possibility)
        #print(neighbor_heap)
        path,possibility=min_deg_search((heappop(neighbor_heap))[2],path,neighbor_heap,possibility,degsum)
    return path,possibility

def max_deg_search(source,path=[],neighbor_heap=[],possibility=1,degsum=0):
    path.append(source)
    if degsum==0:
        degsum+=G[source].degree
    else:
        degsum+=G[source].degree-2
    for i in Gn[source].neighbor:
        if i not in path:
            heappush(neighbor_heap,(-G[i].degree,-Gn[i].descedant_num,i))
    if neighbor_heap:
        possibility=possibility/float(degsum)
        #print(possibility)
        #print(neighbor_heap)
        path,possibility=max_deg_search((heappop(neighbor_heap))[2],path,neighbor_heap,possibility,degsum)
    return path,possibility

def get_max_p(type):
    max_p=0
    max_path=[]
    for i in infected_group:
        if type==1:
            global degsum
            degsum=0
            temppath,p=dfs(i, path=[], possibility=1)
        elif type==2:
            temppath, p =bfs(i, 1)
        elif type == 3:
            temppath, p =bfs(i, 2)
        elif type == 4:
            temppath, p =bfs(i, 3)
        elif type==5:
            temppath, p =max_deg_search(i, path=[], neighbor_heap=[], possibility=1)
        else:
            temppath, p =min_deg_search(i, path=[], neighbor_heap=[], possibility=1)
        #print(type,p)
        if p>max_p:
            max_p=p
            max_path=temppath
    return max_path,max_p
# Class of node with number,children,parent,state,degree,neighbor


class node(object):

    def __init__(self, num):
        self.num = num
        self.children=[]
        self.parent=0
        self.infected=False
        self.degree=0
        self.neighbor=[]
        self.rc=1
        self.descedant_num=0
        self.prob_Gn=0
        self.end_vertex_num=0
        self.root_path=[]
    def ch_append(self, child):
        self.children.append(child)
    def ne_append(self,neighbor):
        self.neighbor.append(neighbor)

# Generating random tree with n vertices under d-irregular tree 

# STEP 1 : construct the base graph G
G=[]
for i in range(0,N+1):
    G.append(node(i))

candidate=[i for i in range(2,N+1)]

for i in range(1,N+1):
    rand_deg=randint(1,d)
    for j in range(i+1,N+1):
        if (G[i].degree < rand_deg) and (j in candidate):
            G[i].ch_append(j)
            G[i].ne_append(j)
            G[i].degree=G[i].degree+1
            G[j].ne_append(i)
            G[j].parent=i
            G[j].degree=G[j].degree+1
            temp=candidate.index(j)
            candidate.pop(temp)



# STEP 2 : Randomly pick a node as the source
source=randint(1,N)
G[source].infected=True

# STEP 3 : Simulate the spreading to n nodes
infected_group=[source]
end_vertices=[]
susceptible_group=list(G[source].neighbor)

num_end=0  # count the number of end vertices
true_num=1 # count the real infected numbers

for i in range(1, n):
    if (num_end < float(n)):
        ran_index=randint(1,len(susceptible_group))-1
        temp=susceptible_group[ran_index]
        infected_group.append(temp)
        G[temp].infected=True
        if len(G[temp].neighbor)==1:     #if temp is a leaf, end number+1
            num_end+=1
        for j in G[temp].neighbor:
            if j not in infected_group:
                susceptible_group.append(j)

        pop_item = susceptible_group.index(temp)
        susceptible_group.pop(pop_item)
        true_num += 1                        # count the infected number
        # print infected_group

n = true_num      # reset n


# Pick a node from infected group as a root Construct Gn as a rooted tree with the root

root_index=randint(0, len(infected_group)-1) #root_index is from 0~n-1
root = infected_group[root_index]
Gn = [node(0)]                   # Gn is from 1~n   Gn[0] is null vertex


for i in range(1, N+1):        #Set Gn as large as G, but with uninfected node=0
    if i in infected_group:
        Gn.append(node(i))
    else:
        Gn.append(node(0))

rootify(root)   #change Gn to a rooted tree
child_sum(root) #compute t^root_v for each node v


for i in range(1,N+1):   #Set degree of nodes in Gn
    Gn[i].degree=len(Gn[i].neighbor)

#Plot the Network by iGraph
Gp=Graph()
Gp.add_vertices(N)


for i in range(1, N+1):
    for j in range(1, N+1):
        if j in G[i].children:
            Gp.add_edges([(i-1, j-1)]) #Gp is started from node "0"

for i in range(1,N+1):
    Gp.vs[i-1]["num"] = i
    if G[i].infected == True:
        if G[i].degree==1:
            Gp.vs[i-1]["state"]="infected"          #highlight the end vertex
            Gp.vs[i-1]["color"]="yellow"
        else:
            Gp.vs[i-1]["state"]="infected"
            Gp.vs[i-1]["color"]="pink"
    else:
        Gp.vs[i-1]["state"] = "uninfected"
        Gp.vs[i-1]["color"]="white"
    if i==source:
        Gp.vs[i-1]["color"]="orange"

Gp.vs["label"] = Gp.vs["num"]


## Point out the Rumor Center and change the color of the node

rumor_center1(root)
rumor_center2(root)
max_rc=0
max_node=0
for i in range(1,N+1):
    if Gn[i].rc>max_rc:
        max_rc=Gn[i].rc
        max_node=i

Gp.vs[max_node-1]["color"]="red"

# ----------------------------------
# Set the output style
layout=Gp.layout_reingold_tilford_circular()
#layout=Gp.layout_grid_fruchterman_reingold()


plot(Gp,layout=layout,bbox=(500,500))
print (infected_group,max_node)
print("root",root)

print(get_max_p(1))
print(get_max_p(2))
print(get_max_p(3))
print(get_max_p(4))
print(get_max_p(5))
# degsum=0
# print ('dfs\n',dfs(root,path=[],possibility=1))
# print ('natural bfs\n',bfs(root,1))
# print ('ascending bfs\n',bfs(root,2))
# print ('descending bfs\n',bfs(root,3))
# print ('max_deg_search \n',max_deg_search(root,path=[],neighbor_heap=[],possibility=1))
# print ('min_deg_search \n',min_deg_search(root,path=[],neighbor_heap=[],possibility=1))

