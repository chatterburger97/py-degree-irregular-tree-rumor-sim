from priority_queue import PriorityQueue


def dijkstra(G, infected_group, dist_map, starting_node_number):
    # dictionary dist_map is of the form : (node_number, dist_map[node_number])
    dist_map[starting_node_number] = 0

    for node_number in infected_group:
        if node_number != starting_node_number:
            dist_map[node_number] = float("inf")

    dist_priority_queue = PriorityQueue(dist_map)

    spt_set = set()
    spt_set.add(starting_node_number)
    infected_group_set = set(infected_group)
    # while the spt does not contain all the elements of the infected graph
    while not infected_group_set.issubset(spt_set):
        current_node_number = dist_priority_queue.pop_task()
        current_node = G[current_node_number]
        spt_set.add(current_node_number)
        for neighbor_node_number in current_node.neighbor:
            if neighbor_node_number in infected_group and neighbor_node_number not in spt_set:
                if dist_map[neighbor_node_number] > (dist_map[current_node.num] + 1):
                    dist_map[neighbor_node_number] = dist_map[current_node.num] + 1
                    # need to use a priority queue, not a simple heap
                    # https://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes
                    dist_priority_queue.add_task(neighbor_node_number, dist_map[neighbor_node_number])
