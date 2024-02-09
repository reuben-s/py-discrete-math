import math

class Edge:
    def __init__(self, u, v=None, weight=math.inf):
        self.u = u
        self.v = v
        self.weight = weight

    def get_weight(self): # Utility function to format weights
        if self.weight == math.inf:
            return "Inf"
        else:
            return self.weight