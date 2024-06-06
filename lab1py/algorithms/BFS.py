from collections import deque


class BFS:
    """Breadth First Search algorithm implementation"""
    def __init__(self, start, goal, nodes):
        self.start = start
        self.goal = goal if isinstance(goal, list) else [goal]  # in case of multiple goals
        self._goal_reached = None  # in case of multiple goals, this will store the goal node we reached
        self.nodes = nodes
        self._found_solution = False
        self._states_visited = 0

    @property
    def goal_reached(self):
        return self._goal_reached

    def __str__(self):
        path = self._get_path()
        return (f'# BFS\n[FOUND_SOLUTION]: {"yes" if self._found_solution else "no"}\n'
                f'[STATES_VISITED]: {self._states_visited}\n[PATH_LENGTH]: {len(path)}\n[PATH]: {" => ".join(path)}')

    def search(self):
        opened_nodes = deque([self.start])
        opened_nodes_set = {self.start}
        closed_nodes = set()

        while opened_nodes:
            current_node = opened_nodes.popleft()
            opened_nodes_set.remove(current_node)
            if any([current_node.state == goal.state for goal in self.goal]):
                self._goal_reached = current_node
                self._found_solution = True
                self._states_visited = len(closed_nodes)
                return True

            current_node.children.sort()
            closed_nodes.add(current_node)  # maybe to the end of the loop
            for child in current_node.children:
                child_node = self.nodes[child]
                if child_node not in closed_nodes and child_node not in opened_nodes_set:
                    child_node.parent = current_node
                    opened_nodes.append(child_node)
                    opened_nodes_set.add(child_node)
        return False

    def _get_path(self):
        path = []
        current_node = self.goal_reached
        while current_node:
            path.append(current_node.state)
            current_node = current_node.parent
        return path[::-1]
