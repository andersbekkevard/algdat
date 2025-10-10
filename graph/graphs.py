from enum import Enum
from math import inf
from typing import Optional
from queue import Queue


INF = 10**18


# region definitions
class Color(Enum):
    WHITE = 1
    GRAY = 2
    BLACK = 3

    def __str__(self) -> str:
        return self.name.capitalize()


class Graph:
    def __init__(self):
        self.vertices: list[Node] = []

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_edge(self, vertex1, vertex2):
        vertex1.add_neighbor(vertex2)
        vertex2.add_neighbor(vertex1)

    def __str__(self) -> str:
        representation = "=" * 20 + " Graph " + "=" * 20 + "\n"
        for vertex in self.vertices:
            representation += f"{vertex}\n"
        return representation

    def __repr__(self) -> str:
        return self.__str__()


class Node:
    def __init__(self, value):
        self.value = value
        self.color = Color.WHITE
        self.neighbors: list[Node] = []
        self.d = 0
        self.pred: Optional[Node] = None
        self.f = 0

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def get_neighbors(self):
        return self.neighbors

    def __str__(self) -> str:
        neighbor_values = [neighbor.value for neighbor in self.neighbors]
        return (
            f"Node(value={self.value}, color={self.color}, neighbors={neighbor_values})"
        )

    def __repr__(self) -> str:
        return self.__str__()


# endregion


# region test graph
def get_test_graph():
    """
    Properties:
    - Connected graph (all vertices reachable)
    - Contains cycles (A-B-F-E-A, C-G-H-D-C, etc.)
    - Not bipartite (contains odd-length cycles)
    - Multiple paths between vertices
    - Mixed vertex degrees (1-4 neighbors)

    Visual representation:
        A - B - C - D
        |   |   |
        E - F - G - H
        |       |
        I - J - K

    Returns:
        Graph: A Graph object with 11 vertices and 13 edges
    """
    g = Graph()

    vertices = {}
    for i, name in enumerate(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]):
        vertices[name] = Node(name)
        g.add_vertex(vertices[name])

    edges = [
        ("A", "B"),
        ("A", "E"),
        ("B", "C"),
        ("B", "F"),
        ("C", "D"),
        ("C", "G"),
        ("D", "H"),
        ("E", "F"),
        ("E", "I"),
        ("F", "G"),
        ("G", "H"),
        ("G", "K"),
        ("I", "J"),
        ("J", "K"),
    ]

    for v1, v2 in edges:
        g.add_edge(vertices[v1], vertices[v2])

    return g


def get_small_test_graph():
    """
    Properties:
    - Small connected graph (4 vertices, 3 edges)
    - Contains one cycle (A-B-C-A)
    - Simple structure for basic testing
    - Not bipartite (contains odd-length cycle)

    Visual representation:
        A - B
        |   |
        D - C

    Returns:
        Graph: A Graph object with 4 vertices and 4 edges
    """
    g = Graph()

    vertices = {}
    for name in ["A", "B", "C", "D"]:
        vertices[name] = Node(name)
        g.add_vertex(vertices[name])

    edges = [
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
        ("D", "A"),
    ]

    for v1, v2 in edges:
        g.add_edge(vertices[v1], vertices[v2])

    return g


# endregion


def bfs(G: Graph, start: Node):
    for u in G.vertices:
        u.color = Color.WHITE
        u.d = INF
        u.pred = None
    start.d = 0
    start.color = Color.GRAY

    Q: Queue[Node] = Queue()
    Q.put(start)
    while not Q.empty():
        u = Q.get()
        u.color = Color.GRAY
        print(u)
        for v in u.get_neighbors():
            if v.color == Color.WHITE:
                v.color = Color.GRAY
                v.d = u.d + 1
                v.pred = u
                Q.put(v)
        u.color = Color.BLACK


def dfs_visit(G: Graph, u: Node):
    global time
    time += 1
    u.d = time
    u.color = Color.GRAY
    print(u)
    for v in u.get_neighbors():
        if v.color == Color.WHITE:
            v.pred = u
            dfs_visit(G, v)
    time += 1
    u.f = time
    u.color = Color.BLACK


def dfs(G: Graph):
    for u in G.vertices:
        u.color = Color.WHITE
        u.pred = None
    global time
    time = 0

    for u in G.vertices:
        if u.color == Color.WHITE:
            dfs_visit(G, u)


if __name__ == "__main__":
    test_graph = get_test_graph()
    dfs(test_graph)
