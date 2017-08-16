import search_heuristics as srch
import matplotlib.pyplot as plt
from dijkstra import dijkstra
from math import sqrt

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
    elif chosen_search == 'min_deg_search':
        for val in infected_group:
            adjusted_possibility = input_graph.rumor_centrality(val) * input_graph.min_deg_search(val)[1]
            if max_permutation_probability < float(adjusted_possibility):
                max_permutation_probability = float(adjusted_possibility)
                estimated_start_node = val
    elif chosen_search == 'max_deg_search':
        for val in infected_group:
            adjusted_possibility = input_graph.rumor_centrality(val) * input_graph.max_deg_search(val)[1]
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
        self.iteration = 1
        # print 'initialised new simulator'

    def add_hop_error(self, constructed_graph, input_graph, actual_source, infected_group):
        # print(self.chosen_search, ', entering add_hop_error')
        dist_map = dict()
        dijkstra(constructed_graph, infected_group, dist_map, actual_source)
        estimated_start_node = find_max_possibility_path(self.chosen_search, input_graph, infected_group, self.bfs_argument)
        # print estimated_start_node
        self.hopErrorSum += dist_map[estimated_start_node]

    def plot_hop_error(self):
        if self.chosen_search == 'bfs':
            key = self.chosen_search + str(self.bfs_argument)
        else:
            key = self.chosen_search
        global_hop_error_dictionary[key] = self.hopErrorSum


def plot_all(sim_count, file_prefix):

    natural_bfs_sim = simulation_executor('bfs', 1)
    ascending_bfs_sim = simulation_executor('bfs', 2)
    descending_bfs_sim = simulation_executor('bfs', 3)
    min_deg_sim = simulation_executor('min_deg_search')
    max_deg_sim = simulation_executor('max_deg_search')
    bfs_arithmetic_avg = simulation_executor('bfs_arithmetic_avg')
    bfs_geometric_avg = simulation_executor('bfs_geometric_avg')

    for val in range(0, sim_count):
        input_graph = srch.Graph(100, 3)
        constructed_graph = input_graph.construct_underlying_graph()
        valid = False
        actual_source = -1
        infected_group = []

        while not valid:
            try:
                actual_source, infected_group = input_graph.spread_rumor(10)
                valid = True
            except ValueError:  # known bug in randint in spread_rumor
                valid = False

        natural_bfs_sim.add_hop_error(constructed_graph, input_graph, actual_source, infected_group)
        ascending_bfs_sim.add_hop_error(constructed_graph, input_graph, actual_source, infected_group)
        descending_bfs_sim.add_hop_error(constructed_graph, input_graph, actual_source, infected_group)
        min_deg_sim.add_hop_error(constructed_graph, input_graph, actual_source, infected_group)
        max_deg_sim.add_hop_error(constructed_graph, input_graph, actual_source, infected_group)
        bfs_arithmetic_avg.add_hop_error(constructed_graph, input_graph, actual_source, infected_group)
        bfs_geometric_avg.add_hop_error(constructed_graph, input_graph, actual_source, infected_group)

    # store the sum of hop errors for each search as a key-value pair in a global dictionary
    natural_bfs_sim.plot_hop_error()
    ascending_bfs_sim.plot_hop_error()
    descending_bfs_sim.plot_hop_error()
    min_deg_sim.plot_hop_error()
    max_deg_sim.plot_hop_error()
    bfs_arithmetic_avg.plot_hop_error()
    bfs_geometric_avg.plot_hop_error()

    # plot the final bar graph
    plt.bar(range(len(global_hop_error_dictionary)), global_hop_error_dictionary.values(), align='center')
    # plt.xticks(range(len(global_hop_error_dictionary)), global_hop_error_dictionary.keys())
    plt.xticks(range(len(global_hop_error_dictionary)), range(len(global_hop_error_dictionary.keys())))

    legend_keys = global_hop_error_dictionary.keys()
    legend_values = []
    for val in range(0, len(global_hop_error_dictionary)):
        legend_values.append(legend_keys[val])
    plt.legend(legend_keys, legend_values)

    plt.savefig(str(file_prefix + '.png'))


# run actual main method
if __name__ == '__main__':
    user_defined_sim_count = raw_input("Please enter the number of times you wish to simulate\n")
    user_defined_names = raw_input("Enter a unique name for the saved plot file \n")
    plot_all(int(user_defined_sim_count), user_defined_names)
