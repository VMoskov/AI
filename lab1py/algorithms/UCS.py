import heapq


class UCS:
    """Uniform Cost Search algorithm implementation (Dijkstra's algorithm)"""
    def __init__(self, start, goal, nodes):
        self.start = start
        self.goal = goal if isinstance(goal, list) else [goal]  # in case of multiple goals
        self._goal_reached = None  # in case of multiple goals, this will store the goal node we reached
        self.nodes = nodes
        self._found_solution = False
        self._states_visited = 0
        self._total_cost = 0

    @property
    def goal_reached(self):
        return self._goal_reached

    @property
    def total_cost(self):
        return self._total_cost

    def __str__(self):
        path = self._get_path()
        return (f'# UCS\n[FOUND_SOLUTION]: {"yes" if self._found_solution else "no"}\n'
                f'[STATES_VISITED]: {self._states_visited}\n[PATH_LENGTH]: {len(path)}\n'
                f'[TOTAL_COST]: {self._total_cost: .1f}\n[PATH]: {" => ".join(path)}')

    def search(self):
        opened_nodes = [self.start]
        opened_nodes_set = {self.start}
        closed_nodes = set()

        while opened_nodes:
            current_node = heapq.heappop(opened_nodes)

            if any([current_node.state == goal.state for goal in self.goal]):
                self._goal_reached = current_node
                self._found_solution = True
                self._total_cost = current_node.cost
                self._states_visited = len({node.state for node in closed_nodes})
                return True

            closed_nodes.add(current_node)
            for child, cost_to_child in current_node.children.items():
                child_node = self.nodes[child]
                new_cost = current_node.cost + cost_to_child
                if child_node not in closed_nodes and (new_cost < child_node.cost or child_node.cost == 0):
                    child_node.cost = new_cost
                    child_node.calculate_heuristic_cost()
                    child_node.parent = current_node
                    if child_node not in opened_nodes_set:
                        heapq.heappush(opened_nodes, child_node)
        return False

    def _get_path(self):
        path = []
        current_node = self._goal_reached
        while current_node:
            path.append(current_node.state)
            current_node = current_node.parent
        return path[::-1]
