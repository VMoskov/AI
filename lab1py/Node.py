class Node:
    """Class to represent a node in a graph"""
    def __init__(self, state, children=None, parent=None, cost=0, heuristic=0):
        self.state = state
        self.children = children
        self.parent = parent
        self.cost = cost
        self._heuristic = heuristic
        self.heuristic_cost = self.cost + self.heuristic

    @property
    def heuristic(self):
        return self._heuristic

    def __str__(self):
        return f'{self.state}: {[child for child in self.children]}, cost: {self.cost}, heuristic: {self.heuristic}'

    def __lt__(self, other):
        if self.heuristic_cost == other.heuristic_cost:
            return self.state < other.state
        return self.heuristic_cost < other.heuristic_cost

    def calculate_heuristic_cost(self):
        self.heuristic_cost = self.cost + self.heuristic

    def reset(self):
        self.cost = 0
        self._heuristic = 0
        self.calculate_heuristic_cost()
        self.parent = None

    def set_heuristics(self, heuristics):
        self._heuristic = heuristics[self.state]
