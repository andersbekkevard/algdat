"""
DAG Shortest Paths Algorithm
Finds shortest paths from a source vertex in a Directed Acyclic Graph (DAG)
Time Complexity: O(V + E)
"""

from collections import defaultdict, deque
from typing import Dict, List, Tuple, Optional


class Graph:
    """Graph representation using adjacency list with weighted edges"""

    def __init__(self, vertices: int):
        self.V = vertices
        self.adj: Dict[int, List[Tuple[int, float]]] = defaultdict[
            int, List[Tuple[int, float]]
        ](list)

    def add_edge(self, u: int, v: int, weight: float):
        """Add a directed edge from u to v with given weight"""
        self.adj[u].append((v, weight))

    def topological_sort_util(self, v: int, visited: Dict[int, bool], stack: List[int]):
        """Utility function for topological sort using DFS"""
        visited[v] = True

        # Recursively visit all adjacent vertices
        if v in self.adj:
            for neighbor, _ in self.adj[v]:
                if not visited.get(neighbor, False):
                    self.topological_sort_util(neighbor, visited, stack)

        # Push current vertex to stack after all descendants are processed
        stack.append(v)

    def topological_sort(self) -> List[int]:
        """
        Perform topological sort on the DAG
        Returns vertices in topologically sorted order
        """
        visited = {i: False for i in range(self.V)}
        stack = []

        # Call the recursive helper function for all vertices
        for i in range(self.V):
            if not visited[i]:
                self.topological_sort_util(i, visited, stack)

        # Return vertices in topologically sorted order (reverse of stack)
        return stack[::-1]


def initialize_single_source(
    G: Graph, s: int
) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
    """
    Initialize-Single-Source(G, s)
    Sets distance to infinity for all vertices except source

    Returns:
        distances: dictionary mapping vertex -> shortest distance from source
        predecessors: dictionary mapping vertex -> predecessor in shortest path
    """
    distances = {i: float("inf") for i in range(G.V)}
    predecessors: Dict[int, Optional[int]] = {i: None for i in range(G.V)}
    distances[s] = 0
    return distances, predecessors


def relax(
    u: int,
    v: int,
    weight: float,
    distances: Dict[int, float],
    predecessors: Dict[int, Optional[int]],
) -> bool:
    """
    Relax(u, v, w)
    Update shortest path estimate for vertex v if path through u is shorter

    Returns:
        True if relaxation occurred, False otherwise
    """
    if distances[v] > distances[u] + weight:
        distances[v] = distances[u] + weight
        predecessors[v] = u
        return True
    return False


def dag_shortest_paths(
    G: Graph, s: int
) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
    """
    Dag-Shortest-Paths(G, w, s)
    Finds shortest paths from source s in a DAG

    Algorithm:
    1. Topologically sort the vertices
    2. Initialize single source distances
    3. Process vertices in topological order
    4. Relax all edges from each vertex

    Args:
        G: Directed Acyclic Graph
        s: Source vertex

    Returns:
        distances: shortest distances from source to all vertices
        predecessors: predecessor pointers for path reconstruction
    """
    # Step 1: Topologically sort G
    topsort = G.topological_sort()

    # Step 2: Initialize-Single-Source(G, s)
    distances, predecessors = initialize_single_source(G, s)

    # Step 3-5: For each vertex u in topological order
    #           For each vertex v in G.Adj[u]
    #           Relax(u, v, w)
    for u in topsort:
        if u in G.adj:
            for v, weight in G.adj[u]:
                relax(u, v, weight, distances, predecessors)

    return distances, predecessors


def get_shortest_path(
    predecessors: Dict[int, Optional[int]], s: int, t: int
) -> Optional[List[int]]:
    """
    Reconstruct shortest path from source s to target t

    Args:
        predecessors: predecessor dictionary from dag_shortest_paths
        s: source vertex
        t: target vertex

    Returns:
        List of vertices in the shortest path from s to t, or None if no path exists
    """
    if predecessors[t] is None and t != s:
        return None  # No path exists

    path = []
    current = t
    while current is not None:
        path.append(current)
        current = predecessors[current]

    return path[::-1]


def print_shortest_paths(
    G: Graph,
    s: int,
    distances: Dict[int, float],
    predecessors: Dict[int, Optional[int]],
):
    """Print shortest paths from source to all reachable vertices"""
    print(f"\nShortest paths from vertex {s}:")
    print("-" * 50)

    for v in range(G.V):
        if distances[v] == float("inf"):
            print(f"Vertex {v}: No path (distance = ∞)")
        else:
            path = get_shortest_path(predecessors, s, v)
            if path is not None:
                path_str = " -> ".join(map(str, path))
                print(f"Vertex {v}: distance = {distances[v]:.2f}, path = {path_str}")
            else:
                print(f"Vertex {v}: No path")


# Example usage and test cases
if __name__ == "__main__":
    print("=" * 50)
    print("DAG Shortest Paths Algorithm")
    print("=" * 50)

    # Example 1: Simple DAG
    print("\nExample 1: Simple DAG")
    g1 = Graph(6)
    g1.add_edge(0, 1, 5)
    g1.add_edge(0, 2, 3)
    g1.add_edge(1, 3, 6)
    g1.add_edge(1, 2, 2)
    g1.add_edge(2, 4, 4)
    g1.add_edge(2, 5, 2)
    g1.add_edge(2, 3, 7)
    g1.add_edge(3, 4, -1)
    g1.add_edge(4, 5, -2)

    distances, predecessors = dag_shortest_paths(g1, 0)
    print_shortest_paths(g1, 0, distances, predecessors)

    # Example 2: DAG from CLRS textbook (Figure 24.5)
    print("\n" + "=" * 50)
    print("Example 2: CLRS Textbook Example")
    g2 = Graph(6)
    g2.add_edge(0, 1, 5)  # r -> s
    g2.add_edge(0, 2, 3)  # r -> t
    g2.add_edge(1, 2, 2)  # s -> t
    g2.add_edge(1, 3, 6)  # s -> x
    g2.add_edge(2, 3, 7)  # t -> x
    g2.add_edge(2, 4, 4)  # t -> y
    g2.add_edge(2, 5, 2)  # t -> z
    g2.add_edge(3, 4, -1)  # x -> y
    g2.add_edge(3, 5, 1)  # x -> z
    g2.add_edge(4, 5, -2)  # y -> z

    source = 1  # Start from vertex s
    distances, predecessors = dag_shortest_paths(g2, source)
    print_shortest_paths(g2, source, distances, predecessors)

    # Example 3: Linear chain
    print("\n" + "=" * 50)
    print("Example 3: Linear Chain")
    g3 = Graph(5)
    g3.add_edge(0, 1, 1)
    g3.add_edge(1, 2, 2)
    g3.add_edge(2, 3, 3)
    g3.add_edge(3, 4, 4)

    distances, predecessors = dag_shortest_paths(g3, 0)
    print_shortest_paths(g3, 0, distances, predecessors)

    # Example 4: Graph from LP formulation
    print("\n" + "=" * 50)
    print("Example 4: LP Formulation Graph")
    print("Vertices: A=0, B=1, C=2, D=3, E=4, F=5")
    g4 = Graph(6)
    # From LP constraints: d_v <= d_u + w means edge (u, v) with weight w
    g4.add_edge(0, 1, 2)
    g4.add_edge(0, 2, 5)
    g4.add_edge(1, 2, 1)
    g4.add_edge(1, 3, 2)
    g4.add_edge(2, 3, 3)
    g4.add_edge(2, 4, 6)
    g4.add_edge(3, 4, 1)
    g4.add_edge(3, 5, 4)
    g4.add_edge(4, 5, 2)

    source = 0  # Start from vertex A
    distances, predecessors = dag_shortest_paths(g4, source)
    print_shortest_paths(g4, source, distances, predecessors)
