

class graph:

    def __init__(self, v, edges):
        self.v = v
        self.edgeTo = edges

    def V(self):
        return self.v
                
    def adj(self, x):
        try:
            r = self.edgeTo[x]
            return r
        except KeyError:
            return []