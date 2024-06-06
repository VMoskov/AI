import copy
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))
from UCS import UCS


class ASTAR:
    """A* algorithm implementation."""
    def __init__(self, start, goal, nodes, path):
        self.start = start
        self.goal = goal if isinstance(goal, list) else [goal]  # in case of multiple goals
        self._goal_reached = None  # in case of multiple goals, this will store the goal node we reached
        self.nodes = nodes
        self.file = os.path.basename(path)
        self._found_solution = False
        self._states_visited = 0
        self._total_cost = 0
        self._is_optimistic = True
        self._is_consistent = True

    @property
    def goal_reached(self):
        return self._goal_reached

    @property
    def total_cost(self):
        return self._total_cost

    def __str__(self):
        path = self._get_path()
        return (f'# A-STAR {self.file}\n[FOUND_SOLUTION]: {"yes" if self._found_solution else "no"}\n'
                f'[STATES_VISITED]: {self._states_visited}\n[PATH_LENGTH]: {len(path)}\n'
                f'[TOTAL_COST]: {self._total_cost: .1f}\n[PATH]: {" => ".join(path)}')

    def search(self):
        opened_nodes = [self.start]
        closed_nodes = []

        while opened_nodes:
            opened_nodes.sort(key=lambda node: (node.heuristic_cost, node.state))
            current_node = opened_nodes.pop(0)

            if any([current_node.state == goal.state for goal in self.goal]):
                self._goal_reached = current_node
                self._found_solution = True
                self._total_cost = current_node.cost
                self._states_visited = len({node.state for node in closed_nodes})
                return True

            closed_nodes.append(current_node)
            for child in current_node.children:
                child_node = self.nodes[child]
                new_cost = current_node.cost + current_node.children[child]

                if child_node not in closed_nodes or new_cost < child_node.cost:
                    child_node = copy.deepcopy(child_node)
                    child_node.cost = new_cost
                    child_node.calculate_heuristic_cost()
                    child_node.parent = current_node
                    opened_nodes.append(child_node)
        return False

    def _get_path(self):
        path = []
        current_node = self._goal_reached
        while current_node:
            path.append(current_node.state)
            current_node = current_node.parent
        return path[::-1]

    def check_optimistic(self):
        print(f'# HEURISTIC-OPTIMISTIC {self.file}')
        for state in self.nodes:
            nodes = copy.deepcopy(self.nodes)
            start = copy.copy(nodes[state])
            [node.reset() for node in nodes.values()]
            ucs = UCS(start, copy.deepcopy(self.goal), nodes)
            ucs.search()
            if start.heuristic <= ucs.total_cost:
                condition = 'OK'
            else:
                self._is_optimistic = False
                condition = 'ERR'
            print(f'[CONDITION]: [{condition}] h({start.state}) <= h*: {start.heuristic:.1f} <= {ucs.total_cost:.1f}')
        print(f'[CONCLUSION]: Heuristic is{" not " if not self._is_optimistic else " "}optimistic.')

    def check_consistent(self):
        print(f'# HEURISTIC-CONSISTENT {self.file}')
        for node in self.nodes:
            current_node = self.nodes[node]
            for child in current_node.children:
                child_node = self.nodes[child]
                if current_node.heuristic <= child_node.heuristic + current_node.children[child]:
                    condition = 'OK'
                else:
                    self._is_consistent = False
                    condition = 'ERR'
                print(f'[CONDITION]: [{condition}] h({current_node.state}) <= h({child_node.state}) + c: '
                      f'{current_node.heuristic:.1f} <= {child_node.heuristic:.1f} + {current_node.children[child]:.1f}')
        print(f'[CONCLUSION]: Heuristic is{" not" if not self._is_consistent else ""} consistent.')
