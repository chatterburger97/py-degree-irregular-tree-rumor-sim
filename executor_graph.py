import graph_functions as graph_func
import matplotlib.pyplot as plt
from dijkstra import dijkstra
from math import sqrt
from collections import OrderedDict

global_hop_error_dictionary = {}


def find_max_possibility_path(chosen_search, input_graph, infected_group, bfs_argument=1):
    # max probability among the probabilities of any of the permutations that result in infected_group
    max_permutation_probability = 0
    estimated_start_node = 0
    if chosen_search == 'bfs':
        for val in infected_group:
            adjusted_possibility = input_graph.rumor_centrality(val) * input_graph.bfs(val, bfs_argument)[1]
            if max_permutation_probability < float(adjusted_possibility):
                max_permutation_probability = float(adjusted_possibility)
                estimated_start_node = val
    elif chosen_search == 'dfs':
        for val in infected_group:
            adjusted_possibility = input_graph.rumor_centrality(val) * input_graph.dfs(val, path=[], possibility=1, degsum=0)[1]
            if max_permutation_probability < float(adjusted_possibility):
                max_permutation_probability = float(adjusted_possibility)
                estimated_start_node = val
    elif chosen_search == 'min_deg_search':
        for val in infected_group:
            adjusted_possibility = input_graph.rumor_centrality(val) * input_graph.min_deg_search(val, path=[], neighbor_heap=[], possibility=1)[1]
            if max_permutation_probability < float(adjusted_possibility):
                max_permutation_probability = float(adjusted_possibility)
                estimated_start_node = val
    elif chosen_search == 'max_deg_search':
        for val in infected_group:
            adjusted_possibility = input_graph.rumor_centrality(val) * input_graph.max_deg_search(val, path=[], neighbor_heap=[], possibility=1)[1]
            if max_permutation_probability < float(adjusted_possibility):
                max_permutation_probability = float(adjusted_possibility)
                estimated_start_node = val
    elif chosen_search == 'dfs':
        for val in infected_group:
            adjusted_possibility = input_graph.rumor_centrality(val) * input_graph.dfs(val)[1]
            if max_permutation_probability < float(adjusted_possibility):
                max_permutation_probability = float(adjusted_possibility)
                estimated_start_node = val
    elif chosen_search == 'bfs_arithmetic_avg':
        for val in infected_group:
            adjusted_possibility = input_graph.rumor_centrality(val) * (input_graph.bfs(val, 2)[1] + input_graph.bfs(val, 3)[1]) / 2
            if max_permutation_probability < float(adjusted_possibility):
                max_permutation_probability = float(adjusted_possibility)
                estimated_start_node = val
    elif chosen_search == 'bfs_geometric_avg':
        for val in infected_group:
            adjusted_possibility = input_graph.rumor_centrality(val) * sqrt(input_graph.bfs(val, 2)[1] * input_graph.bfs(val, 3)[1])
            if max_permutation_probability < float(adjusted_possibility):
                max_permutation_probability = float(adjusted_possibility)
                estimated_start_node = val
    else:
        print 'please refer to search_heuristics for a list of valid search methods'

    return estimated_start_node


class simulation_executor:
    def __init__(self, chosen_search, bfs_argument=1):
        self.chosen_search = chosen_search
        self.bfs_argument = bfs_argument
        self.hopErrorSum = 0
        self.error_distribution_dict = {}
        # print 'initialised new simulator'
        # self.hop_error_dict = {}

    def add_hop_error(self, constructed_graph, input_graph, actual_source, infected_group):
        dist_map = dict()
        dijkstra(constructed_graph, infected_group, dist_map, actual_source)
        estimated_start_node = find_max_possibility_path(self.chosen_search, input_graph, infected_group, self.bfs_argument)

        # self.hopErrorSum += dist_map[estimated_start_node]
        hop_error = dist_map[estimated_start_node]
        try:
            self.error_distribution_dict[hop_error] += 1
        except KeyError:
            self.error_distribution_dict[hop_error] = 1

    def plot_hop_error(self, file_prefix, sim_count):
        # logic for plotting one graph per search type such that
        # the graph displays the hop error distribution
        error_distribution_ordered_dict = OrderedDict(sorted(self.error_distribution_dict.items()))
        if self.chosen_search == 'bfs':
            title = self.chosen_search + str(self.bfs_argument)
        else:
            title = self.chosen_search

        print title, error_distribution_ordered_dict
        plt.title(title)
        plt.bar(range(len(self.error_distribution_dict)), error_distribution_ordered_dict.values(), align='center')
        plt.xticks(range(len(self.error_distribution_dict)), error_distribution_ordered_dict.keys())
        plt.tight_layout()
        plt.savefig(str(file_prefix + '_' + title + '.png'))
        plt.clf()


def plot_all(sim_count, file_prefix):

    natural_bfs_sim = simulation_executor('bfs', 1)
    ascending_bfs_sim = simulation_executor('bfs', 2)
    descending_bfs_sim = simulation_executor('bfs', 3)
    min_deg_sim = simulation_executor('min_deg_search')
    max_deg_sim = simulation_executor('max_deg_search')
    bfs_arithmetic_avg_sim = simulation_executor('bfs_arithmetic_avg')
    bfs_geometric_avg_sim = simulation_executor('bfs_geometric_avg')
    dfs_sim = simulation_executor('dfs')

    for val in range(0, sim_count):
        input_graph = graph_func.Graph(100, 3)
        input_graph.construct_underlying_graph()

        valid = False
        actual_source = -1
        infected_group = []

        while not valid:
            try:
                actual_source, infected_group = input_graph.spread_rumor(10)
                infected_mst = input_graph.get_infected_mst()
                valid = True
            except ValueError:  # known bug in randint in spread_rumor
                valid = False

        natural_bfs_sim.add_hop_error(infected_mst, input_graph, actual_source, infected_group)
        ascending_bfs_sim.add_hop_error(infected_mst, input_graph, actual_source, infected_group)
        descending_bfs_sim.add_hop_error(infected_mst, input_graph, actual_source, infected_group)
        min_deg_sim.add_hop_error(infected_mst, input_graph, actual_source, infected_group)
        max_deg_sim.add_hop_error(infected_mst, input_graph, actual_source, infected_group)
        bfs_arithmetic_avg_sim.add_hop_error(infected_mst, input_graph, actual_source, infected_group)
        bfs_geometric_avg_sim.add_hop_error(infected_mst, input_graph, actual_source, infected_group)
        dfs_sim.add_hop_error(infected_mst, input_graph, actual_source, infected_group)

    # store the sum of hop errors for each search as a key-value pair in a global dictionary
    natural_bfs_sim.plot_hop_error(file_prefix, sim_count)
    ascending_bfs_sim.plot_hop_error(file_prefix, sim_count)
    descending_bfs_sim.plot_hop_error(file_prefix, sim_count)
    min_deg_sim.plot_hop_error(file_prefix, sim_count)
    max_deg_sim.plot_hop_error(file_prefix, sim_count)
    bfs_arithmetic_avg_sim.plot_hop_error(file_prefix, sim_count)
    bfs_geometric_avg_sim.plot_hop_error(file_prefix, sim_count)
    dfs_sim.plot_hop_error(file_prefix, sim_count)


def remove(value, deletechars):
    for c in deletechars:
        value = value.replace(c, '')
    return value


# run actual main method
if __name__ == '__main__':
    valid = False
    while(not valid):
        try:
            user_defined_sim_count = raw_input("Please enter the number of times you wish to simulate\n")
            user_defined_names = raw_input("Enter a unique name for the saved plot file \n")
            int(user_defined_sim_count)
            remove(user_defined_names, '\/:*?"<>|')
            plot_all(int(user_defined_sim_count), user_defined_names)
            valid = True
        except ValueError:
            print ' ERROR : Invalid input. Please input sim count as number'
            valid = False
