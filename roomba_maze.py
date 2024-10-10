from typing import List, Tuple
from typing_extensions import Self
import matplotlib.pyplot as plt
import networkx as nx
import random


class Maze:
    # Stores a maze

    @staticmethod
    def cardinal_directions() -> List[Tuple[int, int]]:
        return [(0, 1), (1, 0), (0, -1), (-1, 0)]

    @staticmethod
    def are_neighbors(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        return abs(x1 - x2) + abs(y1 - y2) == 1

    def is_in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def move(self, x: int, y: int, direction: int) -> Tuple[int, int]:
        dx, dy = self.cardinal_directions()[direction]
        res = (x + dx, y + dy)
        return res if self.is_in_bounds(*res) and self.G.has_edge((x, y), res) else (x, y)

    def neighbors_of(self, x: int, y: int) -> List[int]:
        return [
            (x + dx, y + dy) for (dx, dy) in self.cardinal_directions()
            if self.is_in_bounds(x + dx, y + dy)
        ]

    def new_empty(self, size_x: int, size_y: int):
        # Creates an empty rectangular maze with dimensions size_x x size_y
        self.size_x, self.size_y = size_x, size_y
        self.G = nx.Graph()
        self.G.add_nodes_from([(x, y) for x in range(size_x) for y in range(size_y)])
        return self

    def add_random_wilson(self) -> Self:
        # Generates a random rectangular maze with dimensions size_x x size_y using Wilson's algorithm
        # The algorithm is described in https://dl.acm.org/doi/10.1145/237814.237880

        # Assumption: `self.G` has nodes representing cells of a rectangle

        # Init
        in_maze = {node: False for node in self.G.nodes}
        next_node = {node: None for node in self.G.nodes}
        # todo: set RNG seed

        # Choose a root node at random
        root = (random.randrange(self.size_x), random.randrange(self.size_y))
        next_node[root] = root
        in_maze[root] = True

        # Add branches
        for node in self.G.nodes:
            curr = node
            while not in_maze[curr]:
                next_node[curr] = random.choice(self.neighbors_of(*curr))
                curr = next_node[curr]

            curr = node
            while not in_maze[curr]:
                self.G.add_edge(curr, next_node[curr])
                in_maze[curr] = True
                curr = next_node[curr]

        return self

    def draw(self) -> Self:
        # Draws the maze
        # todo: PyVis for interactive diagram

        nx.draw(self.G, {node: node for node in self.G})
        plt.show()
        return self


class ConcurrentMovesGraph:
    # A directed graph that encodes all possible concurrent moves in two mazes
    def __init__(self, maze1: Maze, maze2: Maze):
        self.digraph = nx.DiGraph()
        self.digraph.add_nodes_from([(u, v) for u in maze1.G.nodes for v in maze2.G.nodes])
        self.digraph.add_edges_from([
            ((u, v), (maze1.move(*u, d), maze2.move(*v, d)))  # arc head can be reached from arc tail in 1 move
            for u in maze1.G.nodes for v in maze2.G.nodes for d in range(len(maze1.cardinal_directions()))
        ])

    def draw(self) -> Self:
        # Draws the graph
        # todo: PyVis for interactive diagram

        nx.draw(self.digraph)
        plt.show()
        return self

    def num_nodes(self) -> int:
        # Returns the number of nodes in the graph
        return self.digraph.number_of_nodes()

    def is_reachable_from_all(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        # Checks if a given (simultaneous) state in two mazes can be reached from all starting states
        shortest_paths = nx.single_target_shortest_path(self.digraph, ((x1, y1), (x2, y2)))
        return len(shortest_paths) == self.num_nodes()


def main():
    size_x, size_y = 10, 10
    for i in range(100):
        # print(i)
        maze1 = Maze().new_empty(size_x, size_y).add_random_wilson()
        maze2 = Maze().new_empty(size_x, size_y).add_random_wilson()
        aux_graph = ConcurrentMovesGraph(maze1, maze2)
        if not aux_graph.is_reachable_from_all(0, 0, 0, 0):
            print(f'Found counterexample: {maze1.graph} {maze2.graph}')
            maze1.draw()
            maze2.draw()


if __name__ == '__main__':
    main()
