import search_heuristics as srch
import matplotlib.pyplot as plt
from math import sqrt
from collections import OrderedDict
from dijkstra import dijkstra


def find_max_P(chosen_search, input_graph, infected_group, bfs_argument=1, dfs_argument=0):
    max_p = -1
    start_node = -1
    for val in infected_group:
        if chosen_search == 'bfs':
            P= input_graph.rumor_centrality(val) * input_graph.bfs(val, bfs_argument)[1]
        elif chosen_search == 'dfs':
            input_graph.degsum=0
            P = input_graph.rumor_centrality(val) * input_graph.dfs(val, dfs_argument, path=[], possibility=1)[1]
        elif chosen_search == 'min_deg_search':
            P = input_graph.rumor_centrality(val) * input_graph.min_deg_search(val, path=[], neighbor_heap=[], possibility=1)[1]
        elif chosen_search == 'max_deg_search':
            P = input_graph.rumor_centrality(val) * input_graph.max_deg_search(val, path=[], neighbor_heap=[], possibility=1)[1]
        elif chosen_search == 'deg_search_arithmetic_avg':
            P = input_graph.rumor_centrality(val) * (
            input_graph.max_deg_search(val, path=[], neighbor_heap=[], possibility=1)[1] +
            input_graph.min_deg_search(val, path=[], neighbor_heap=[], possibility=1)[1]) / 2
        elif chosen_search == 'deg_search_geometric_avg':
            P = input_graph.rumor_centrality(val) * sqrt(
                input_graph.max_deg_search(val, path=[], neighbor_heap=[], possibility=1)[1] *
                input_graph.min_deg_search(val, path=[], neighbor_heap=[], possibility=1)[1])
        elif chosen_search == 'bfs_arithmetic_avg':
            P = input_graph.rumor_centrality(val) * (
            input_graph.bfs(val, 2)[1] + input_graph.bfs(val, 3)[1]) / 2
        elif chosen_search == 'bfs_geometric_avg':
            P = input_graph.rumor_centrality(val) * sqrt(
                input_graph.bfs(val, 2)[1] * input_graph.bfs(val, 3)[1])
        elif chosen_search == 'dfs_arithmetic_avg':
            input_graph.degsum = 0
            a=input_graph.dfs(val, 2, path=[], possibility=1)[1]
            input_graph.degsum = 0
            b=input_graph.dfs(val, 3, path=[], possibility=1)[1]
            P = input_graph.rumor_centrality(val) * (a+b) / 2
        elif chosen_search == 'dfs_geometric_avg':
            input_graph.degsum = 0
            a = input_graph.dfs(val, 2, path=[], possibility=1)[1]
            input_graph.degsum = 0
            b = input_graph.dfs(val, 3, path=[], possibility=1)[1]
            P = input_graph.rumor_centrality(val) * sqrt(a * b)
        if max_p < float(P):
            max_p = float(P)
            start_node = val
    return start_node


class Simulator:
    def __init__(self, chosen_search, bfs_argument=1,dfs_argument=1):
        self.chosen_search = chosen_search
        self.bfs_argument = bfs_argument
        self.dfs_argument = dfs_argument
        self.hopErrorSum = 0
        self.error_distribution_dict = {}

    def add_hop_error(self, constructed_graph, input_graph, actual_source, infected_group):
        dist_map = dict()
        dijkstra(constructed_graph, infected_group, dist_map, actual_source)
        estimated_start_node = find_max_P(self.chosen_search, input_graph, infected_group, self.bfs_argument, self.dfs_argument)
        hop_error = dist_map[estimated_start_node]
        try:
            self.error_distribution_dict[hop_error] += 1
        except KeyError:
            self.error_distribution_dict[hop_error] = 1

    def plot_hop_error(self, sim_n,file_prefix,d,N,n):
        error_distribution_ordered_dict = OrderedDict(sorted(self.error_distribution_dict.items()))
        if self.chosen_search == 'bfs':
            title = self.chosen_search + str(self.bfs_argument)
        elif self.chosen_search == 'dfs':
            title = self.chosen_search + str(self.dfs_argument)
        else:
            title = self.chosen_search
        print(title, error_distribution_ordered_dict)
        plt.title(title+" sim_n="+str(sim_n)+" degree="+str(d)+" graphsize="+str(N)+" infectsize="+str(n))
        plt.bar(range(len(self.error_distribution_dict)), error_distribution_ordered_dict.values(), align='center')
        plt.xticks(range(len(self.error_distribution_dict)), error_distribution_ordered_dict.keys())
        plt.tight_layout()
        plt.savefig(str(file_prefix + '_' + title + '.png'))
        plt.clf()


def plot_all(sim_n, name, degree, size,isize):
    sim_list = []
    sim_list.append(Simulator('bfs', 1))
    sim_list.append(Simulator('bfs', 2))
    sim_list.append(Simulator('bfs', 3))
    sim_list.append(Simulator('dfs', 0, 1))
    sim_list.append(Simulator('dfs', 0, 2))
    sim_list.append(Simulator('dfs', 0, 3))
    sim_list.append(Simulator('min_deg_search'))
    sim_list.append(Simulator('max_deg_search'))
    sim_list.append(Simulator('deg_search_arithmetic_avg'))
    sim_list.append(Simulator('deg_search_geometric_avg'))
    sim_list.append(Simulator('bfs_arithmetic_avg'))
    sim_list.append(Simulator('bfs_geometric_avg'))
    sim_list.append(Simulator('dfs_arithmetic_avg'))
    sim_list.append(Simulator('dfs_geometric_avg'))
    print("simulate start")
    for val in range(0, sim_n):
        print("simulating "+str(val)+"of"+str(sim_n))
        graph_generator = srch.Graph(size, degree,isize)
        print("graph"+str(val)+"generated")
        graph = graph_generator.construct_graph()
        print("graph" + str(val) + "constructed")
        flag = False
        source = -1
        infected_group = []
        while not flag:
            try:
                source, infected_group = graph_generator.spread_rumor(isize)
                print("graph" + str(val) + "spreaded")
                flag = True
            except ValueError:  # known bug in randint in spread_rumor
                #print("fail")
                flag = False
        for i in sim_list:
            i.add_hop_error(graph, graph_generator, source, infected_group)
        print("graph" + str(val) + "hop added")
    # store the sum of hop errors for each search as a key-value pair in a global dictionary
    for i in sim_list:
        i.plot_hop_error(sim_n,name,degree,size,isize)


def remove(value, deletechars):
    for c in deletechars:
        value = value.replace(c, '')
    return value

# run actual main method
if __name__ == '__main__':
    valid = False
    while not valid:
        try:
            sim_count = raw_input("Please enter the number of times you wish to simulate\n")
            names = raw_input("Enter a unique name for the saved plot file \n")
            d = raw_input("Enter degree of trees")
            N = raw_input("Enter size of Graph")
            n=raw_input("Enter size of infected graph")
            remove(names, '\/:*?"<>|')
            plot_all(int(sim_count), names, int(d), int(N),int(n))
            valid = True
        except ValueError:
            print(' ERROR : Invalid input. Please input sim count as number')
            valid = False
