from typing import Tuple
from typing_extensions import Self
import matplotlib.pyplot as plt
import networkx as nx
import random


class Maze:
    def new_empty(self, size_x: int, size_y: int):
        # Creates an empty rectangular maze with dimensions size_x x size_y
        self.size_x, self.size_y = size_x, size_y
        self.G = nx.Graph()
        self.G.add_nodes_from([(x, y) for x in range(size_x) for y in range(size_y)])
        return self

    def random_neighbor(self, x: int, y: int) -> Tuple[int, int]:
        # Returns a random neighbor in bounds
        # todo: control RNG seed
        neighbors = [
            (x + dx, y + dy) for (dx, dy) in [(0, 1), (1, 0), (0, -1), (-1, 0)]
            if 0 <= x + dx < self.size_x and 0 <= y + dy < self.size_y
        ]
        return random.choice(neighbors)

    def add_random_wilson(self) -> Self:
        # Creates a random rectangular maze with dimensions size_x x size_y using Wilson's algorithm
        # The algorithm is described in https://dl.acm.org/doi/10.1145/237814.237880

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
                next_node[curr] = self.random_neighbor(*curr)
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

    def cartesian_product(self, other: Self) -> nx.Graph:
        # todo: desc
        assert(self.size_x == other.size_x and self.size_y == other.size_y)

        product = nx.Graph()

        # todo: implement

        return product


maze = Maze().new_empty(5, 5).add_random_wilson().draw()
