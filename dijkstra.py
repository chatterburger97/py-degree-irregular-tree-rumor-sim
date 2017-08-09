import priority_queue

# how is the graph data structure stored? as an array of objects of class node
 # for all the nodes in a graph
 # first initialise a map data structure to store the hop distance from the root node 
 # if a node is a neighbor of the starting node then set the distance to 1, else to -1
 # 
 # pick a random neighbor node of the current node that is not already in the visited set, and add
 # it to the visited set
 # 
 # when at the current vertex, compare the distance values corresponding to each of its neighbors with 
 # {distance between start node and current node + distance between current node and the neighbor node}
 # update the value if it is less than the value already stored there

 # repeat till sptSet includes all the vertices in the subgraph 

# initialise the dictionary data structure with all distances = -1, start_node distance 0
# dist_map = {}
# infected group must be an array of type int
# starting node should also be of type int
def dijkstra(G, infected_group, dist_map, starting_node_number):
	# dictionary dist_map is of the form : (node_number, dist_map[node_number])
	dist_map[starting_node_number] = 0
	for node_number in infected_group: 
	 	if node_number != starting_node_number:
	 		dist_map[node_number] = float("inf")

	# dist_priority_queue is a priority queue
	dist_priority_queue = priority_queue.PriorityQueue(dist_map) 
	
	# initialise an spt_set, which initially only contains the starting node number
	# stores the nodes that are visited (added to the shortest path tree already) 
	spt_set = set()
	spt_set.add(starting_node_number)
	infected_group_set = set(infected_group)
	# while the spt does not contain all the elements of the infected graph
	while not infected_group_set.issubset(spt_set) :
		# the current node is the node having the minimum known distance from the start node
		current_node_number = dist_priority_queue.pop_task()
		current_node = G[current_node_number]
		# the current node is visited, so it is added to the spt_set
		spt_set.add(current_node_number)
		for neighbor_node_number in current_node.neighbor :
			if neighbor_node_number in infected_group and neighbor_node_number not in spt_set :
		 		if dist_map[neighbor_node_number]>(dist_map[current_node.num]+1) :
		 			dist_map[neighbor_node_number] = dist_map[current_node.num] + 1
		 			# need to use a priority queue, not a simple heap
		 			# https://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes
		 			dist_priority_queue.add_task(neighbor_node_number,dist_map[neighbor_node_number])






		 			




