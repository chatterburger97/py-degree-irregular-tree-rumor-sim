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
