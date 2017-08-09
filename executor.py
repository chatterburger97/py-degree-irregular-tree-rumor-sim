import search_heuristics as srch
from dijkstra import dijkstra
import matplotlib.pyplot as plt
import hashlib
import time

def findMaxPossibilityPath(chosen_search, graph, infected_group, bfs_argument=1) :
    # max probability among the probabilities of any of the permutations that result in infected_group
    max_permutation_probability = 0
    # the node with the largest estimated probability as found above
    estimated_start_node = 0
   
    if chosen_search == 'bfs' : 
        for val in infected_group :
            possibility = graph.bfs(val, bfs_argument)[1]
            if max_permutation_probability < float(possibility):
                max_permutation_probability = float(possibility)
                estimated_start_node = val
    elif chosen_search == 'min_deg_search':
        for val in infected_group :
            possibility = graph.min_deg_search(val)[1]
            if max_permutation_probability < float(possibility):
                max_permutation_probability = float(possibility)
                estimated_start_node = val
    elif chosen_search == 'max_deg_search' :
        for val in infected_group :
            possibility = graph.max_deg_search(val)[1]
            if max_permutation_probability < float(possibility):
                max_permutation_probability = float(possibility)
                estimated_start_node = val
    elif chosen_search == 'dfs' :
        for val in infected_group :
            possibility = graph.dfs(val)[1]
            if max_permutation_probability < float(possibility):
                max_permutation_probability = float(possibility)
                estimated_start_node = val
    else :
        print 'please refer to search_heuristics for a list of valid search methods'
        
    return estimated_start_node

class simulation_executor :
    def __init__(self, chosen_search, sim_count, bfs_argument = 1) :
        self.chosen_search = chosen_search
        self.sim_count = sim_count
        self.bfs_argument = bfs_argument
        self.x_points = []
        self.y_points = []
        self.iteration = 1
        print 'initialised new simulator'

    def simulate(self) :
        print 'entering simulate function with search '
        for val in range(0, self.sim_count, 1):
            graph = srch.Graph(100, 3)
            constructed_graph = graph.return_full_underlying_graph()
            try :
                source, infected_group = graph.spread_rumor(10)
            except ValueError:
                self.sim_count-=1
                continue;
            else:
                dist_map = dict()
                dijkstra(constructed_graph, infected_group, dist_map, source)
                estimated_start_node = findMaxPossibilityPath(self.chosen_search, graph, infected_group, self.bfs_argument) 
                print 'estimated start node : ', estimated_start_node
                print 'hop error: ', dist_map[estimated_start_node]
                self.y_points.append(dist_map[estimated_start_node])
                print 'iteration number : ', val+1
                self.x_points.append(val + 1) # iteration number
    
    def plot_simulation(self, file_prefix=None) :
        print '<plotting simulation>\n'
        plt.plot(self.x_points,self.y_points, 'ro')
        plt.xlabel('Iteration number')
        plt.ylabel('Hop error b/w estimated best probability node and actual rumor source')
        if file_prefix is None :
            plt.show()
        else :
            filename = self.chosen_search + '_'+ file_prefix + '_' + str(self.iteration) + '.png'
            plt.savefig(str(filename))
            print 'filename : ', filename
            self.iteration+=1

def plotAll(sim_count, file_prefix) :
    # plot for natural bfs
    # natural_bfs_sim  = simulation_executor('bfs', sim_count)
    # natural_bfs_sim.simulate()
    # natural_bfs_sim.plot_simulation(file_prefix)

    # plot for ascending bfs
    # ascending_bfs_sim = simulation_executor('bfs',sim_count, 2)
    # ascending_bfs_sim.simulate()
    # ascending_bfs_sim.plot_simulation(file_prefix)

    # plot for descending
    descending_bfs_sim = simulation_executor('bfs', sim_count, 3)
    descending_bfs_sim.simulate()
    descending_bfs_sim.plot_simulation(file_prefix)

    # # plot for min_degree
    # min_deg_sim = simulation_executor('min_deg_search',3)
    # min_deg_sim.plot_simulation()

    # # plot for max degree
    # max_deg_sim = simulation_executor('max_deg_search', 3)
    # max_deg_sim.plot_simulation()
user_defined_sim_count = raw_input("Please enter the number of times you wish to simulate\n")
user_defined_names = raw_input("Enter a unique name for the saved plot file \n")
plotAll(int(user_defined_sim_count), user_defined_names)