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
