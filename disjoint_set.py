import node


class DisjointSet:

    def __init__(self):
        self.p = dict()

    def find(self, x):
        if x == self.p[x]:
            return x
        else:
            self.p[x] = self.find(self.p[x])
            return self.p[x]

    def union(self, x, y):
        self.p[self.find(x)] = self.find(y)

    def add(self, x):
        self.p[x] = x

    def return_as_list(self):
        return self.p

    # additional function
    def add_edge(self, Gr, length, v1, v2):
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
