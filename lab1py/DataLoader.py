import re
from Node import Node


class DataLoader:
    """Class to load data from a file"""
    def __init__(self, path, heuristic_path=None):
        self.path = path
        self.heuristic_path = heuristic_path

    def load_plain_data(self):
        """Load plain data without weights for plain BFS"""
        nodes = {}
        with open(self.path, 'r', encoding='utf-8') as f:
            start = self.skip_comments(f)
            end = f.readline().strip().split()  # multiple goals
            for line in f:
                line = line.replace(':', '').replace(' ', ',').strip().split(',')
                nodes[line[0]] = Node(line[0], [line[i] for i in range(1, len(line), 2)])

        goal = [nodes[end[i]] for i in range(len(end))] if len(end) > 1 else nodes[end[0]]  # handle multiple goals
        return nodes[start], goal, nodes

    def load_weighted_data(self):
        """Load weighted data for UCS (Dijkstra's algorithm)"""
        nodes = {}
        with open(self.path, 'r', encoding='utf-8') as f:
            start = self.skip_comments(f)
            end = f.readline().strip().split()  # multiple goals
            for line in f:
                line = line.replace(':', '').replace(' ', ',').strip().split(',')
                nodes[line[0]] = Node(line[0])
                children = [int(child) if child.isdigit() else child for child in line[1:]]
                pairs = [children[i:i + 2] for i in range(0, len(children), 2)]
                nodes[line[0]].children = {pair[0]: pair[1] for pair in pairs}

        goal = [nodes[end[i]] for i in range(len(end))] if len(end) > 1 else nodes[end[0]]  # handle multiple goals
        return nodes[start], goal, nodes

    def load_heuristic(self):
        """Load heuristic data for A* algorithm"""
        heuristic = {}
        with open(self.heuristic_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = re.findall(r'\w+', line, flags=re.UNICODE)
                heuristic[line[0]] = int(line[1])
        return heuristic

    @staticmethod
    def skip_comments(f):
        line = f.readline().strip()
        while line.startswith('#'):
            line = f.readline().strip()
        return line
