"""
Depth-First Search (DFS) Implementations and Applications

This module provides multiple DFS implementations:
- Recursive DFS
- Iterative DFS (using stack)
- DFS for various applications (cycle detection, connected components, topological sort)

Works with both custom Graph class and adjacency lists.
"""

from typing import List, Set, Dict, Optional, Callable
from collections import defaultdict


def dfs_recursive(graph, start: int, visited: Optional[Set[int]] = None) -> List[int]:
    """
    Recursive DFS traversal.

    Args:
        graph: Graph object with get_neighbors method or adjacency list dict
        start: Starting vertex
        visited: Set of visited vertices (used internally)

    Returns:
        List of vertices in DFS traversal order
    """
    if visited is None:
        visited = set()

    traversal_order = []

    def dfs_helper(vertex: int):
        visited.add(vertex)
        traversal_order.append(vertex)

        # Get neighbors based on graph type
        if hasattr(graph, "get_neighbors"):
            neighbors = graph.get_neighbors(vertex)
        else:
            neighbors = graph.get(vertex, [])

        for neighbor in neighbors:
            if neighbor not in visited:
                dfs_helper(neighbor)

    dfs_helper(start)
    return traversal_order


def dfs_iterative(graph, start: int) -> List[int]:
    """
    Iterative DFS traversal using explicit stack.

    Args:
        graph: Graph object with get_neighbors method or adjacency list dict
        start: Starting vertex

    Returns:
        List of vertices in DFS traversal order
    """
    visited = set()
    stack = [start]
    traversal_order = []

    while stack:
        vertex = stack.pop()

        if vertex not in visited:
            visited.add(vertex)
            traversal_order.append(vertex)

            # Get neighbors based on graph type
            if hasattr(graph, "get_neighbors"):
                neighbors = graph.get_neighbors(vertex)
            else:
                neighbors = graph.get(vertex, [])

            # Add neighbors in reverse order to maintain left-to-right traversal
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append(neighbor)

    return traversal_order


def dfs_with_callback(
    graph,
    start: int,
    pre_visit: Optional[Callable] = None,
    post_visit: Optional[Callable] = None,
) -> None:
    """
    DFS with pre-visit and post-visit callbacks.
    Useful for applications like topological sort.

    Args:
        graph: Graph object or adjacency list
        start: Starting vertex
        pre_visit: Function to call when first visiting a vertex
        post_visit: Function to call when leaving a vertex
    """
    visited = set()

    def dfs_helper(vertex: int):
        visited.add(vertex)

        if pre_visit:
            pre_visit(vertex)

        # Get neighbors
        if hasattr(graph, "get_neighbors"):
            neighbors = graph.get_neighbors(vertex)
        else:
            neighbors = graph.get(vertex, [])

        for neighbor in neighbors:
            if neighbor not in visited:
                dfs_helper(neighbor)

        if post_visit:
            post_visit(vertex)

    dfs_helper(start)


def find_all_paths(graph, start: int, end: int) -> List[List[int]]:
    """
    Find all paths from start to end vertex using DFS.

    Args:
        graph: Graph object or adjacency list
        start: Starting vertex
        end: Target vertex

    Returns:
        List of all paths (each path is a list of vertices)
    """
    all_paths = []

    def dfs_path(vertex: int, path: List[int], visited: Set[int]):
        path.append(vertex)
        visited.add(vertex)

        if vertex == end:
            all_paths.append(path.copy())
        else:
            # Get neighbors
            if hasattr(graph, "get_neighbors"):
                neighbors = graph.get_neighbors(vertex)
            else:
                neighbors = graph.get(vertex, [])

            for neighbor in neighbors:
                if neighbor not in visited:
                    dfs_path(neighbor, path, visited)

        path.pop()
        visited.remove(vertex)

    dfs_path(start, [], set())
    return all_paths


def has_cycle_undirected(graph, num_vertices: int) -> bool:
    """
    Detect if an undirected graph has a cycle using DFS.

    Args:
        graph: Graph object or adjacency list
        num_vertices: Total number of vertices

    Returns:
        True if cycle exists, False otherwise
    """
    visited = set()

    def dfs_cycle(vertex: int, parent: int) -> bool:
        visited.add(vertex)

        # Get neighbors
        if hasattr(graph, "get_neighbors"):
            neighbors = graph.get_neighbors(vertex)
        else:
            neighbors = graph.get(vertex, [])

        for neighbor in neighbors:
            if neighbor not in visited:
                if dfs_cycle(neighbor, vertex):
                    return True
            elif neighbor != parent:
                # Found a back edge (not to parent) -> cycle exists
                return True

        return False

    # Check all components
    for vertex in range(num_vertices):
        if vertex not in visited:
            if dfs_cycle(vertex, -1):
                return True

    return False


def has_cycle_directed(graph, num_vertices: int) -> bool:
    """
    Detect if a directed graph has a cycle using DFS.
    Uses color-based detection (white, gray, black).

    Args:
        graph: Adjacency list for directed graph
        num_vertices: Total number of vertices

    Returns:
        True if cycle exists, False otherwise
    """
    # White: unvisited, Gray: being processed, Black: finished
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * num_vertices

    def dfs_cycle(vertex: int) -> bool:
        color[vertex] = GRAY

        # Get neighbors
        if hasattr(graph, "get_neighbors"):
            neighbors = graph.get_neighbors(vertex)
        else:
            neighbors = graph.get(vertex, [])

        for neighbor in neighbors:
            if color[neighbor] == GRAY:
                # Back edge to a vertex in current path -> cycle
                return True
            if color[neighbor] == WHITE:
                if dfs_cycle(neighbor):
                    return True

        color[vertex] = BLACK
        return False

    # Check all vertices
    for vertex in range(num_vertices):
        if color[vertex] == WHITE:
            if dfs_cycle(vertex):
                return True

    return False


def connected_components(graph, num_vertices: int) -> List[List[int]]:
    """
    Find all connected components in an undirected graph using DFS.

    Args:
        graph: Graph object or adjacency list
        num_vertices: Total number of vertices

    Returns:
        List of components, each component is a list of vertices
    """
    visited = set()
    components = []

    def dfs_component(vertex: int, component: List[int]):
        visited.add(vertex)
        component.append(vertex)

        # Get neighbors
        if hasattr(graph, "get_neighbors"):
            neighbors = graph.get_neighbors(vertex)
        else:
            neighbors = graph.get(vertex, [])

        for neighbor in neighbors:
            if neighbor not in visited:
                dfs_component(neighbor, component)

    for vertex in range(num_vertices):
        if vertex not in visited:
            component = []
            dfs_component(vertex, component)
            components.append(component)

    return components


def topological_sort_dfs(graph, num_vertices: int) -> Optional[List[int]]:
    """
    Perform topological sort on a directed acyclic graph (DAG) using DFS.

    Args:
        graph: Adjacency list for directed graph
        num_vertices: Total number of vertices

    Returns:
        Topologically sorted list of vertices, or None if graph has a cycle
    """
    # First check for cycles
    if has_cycle_directed(graph, num_vertices):
        return None

    visited = set()
    stack = []

    def dfs_topo(vertex: int):
        visited.add(vertex)

        # Get neighbors
        if hasattr(graph, "get_neighbors"):
            neighbors = graph.get_neighbors(vertex)
        else:
            neighbors = graph.get(vertex, [])

        for neighbor in neighbors:
            if neighbor not in visited:
                dfs_topo(neighbor)

        # Add to stack after visiting all descendants
        stack.append(vertex)

    for vertex in range(num_vertices):
        if vertex not in visited:
            dfs_topo(vertex)

    # Reverse stack to get topological order
    return stack[::-1]


def is_bipartite(graph, num_vertices: int) -> bool:
    """
    Check if a graph is bipartite using DFS.
    A graph is bipartite if it can be colored with 2 colors
    such that no adjacent vertices have the same color.

    Args:
        graph: Graph object or adjacency list
        num_vertices: Total number of vertices

    Returns:
        True if graph is bipartite, False otherwise
    """
    color = [-1] * num_vertices  # -1 means uncolored

    def dfs_bipartite(vertex: int, c: int) -> bool:
        color[vertex] = c

        # Get neighbors
        if hasattr(graph, "get_neighbors"):
            neighbors = graph.get_neighbors(vertex)
        else:
            neighbors = graph.get(vertex, [])

        for neighbor in neighbors:
            if color[neighbor] == -1:
                # Color with opposite color
                if not dfs_bipartite(neighbor, 1 - c):
                    return False
            elif color[neighbor] == c:
                # Same color as current vertex -> not bipartite
                return False

        return True

    # Check all components
    for vertex in range(num_vertices):
        if color[vertex] == -1:
            if not dfs_bipartite(vertex, 0):
                return False

    return True


# Example usage and demonstrations
if __name__ == "__main__":
    # Example 1: Adjacency list representation
    print("=" * 60)
    print("Example 1: DFS on Adjacency List")
    print("=" * 60)

    adj_list = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1, 3, 4], 3: [1, 2, 4], 4: [2, 3]}

    print("\nGraph (adjacency list):")
    for vertex, neighbors in adj_list.items():
        print(f"  {vertex}: {neighbors}")

    print("\nRecursive DFS from vertex 0:")
    print(f"  {dfs_recursive(adj_list, 0)}")

    print("\nIterative DFS from vertex 0:")
    print(f"  {dfs_iterative(adj_list, 0)}")

    # Example 2: Using custom Graph class
    print("\n" + "=" * 60)
    print("Example 2: DFS on Custom Graph Class")
    print("=" * 60)

    try:
        from graphs import Graph

        g = Graph(6)
        g.add_edge(0, 1)
        g.add_edge(0, 2)
        g.add_edge(1, 3)
        g.add_edge(2, 3)
        g.add_edge(2, 4)
        g.add_edge(4, 5)

        print("\nRecursive DFS from vertex 0:")
        print(f"  {dfs_recursive(g, 0)}")

        print("\nIterative DFS from vertex 0:")
        print(f"  {dfs_iterative(g, 0)}")

    except ImportError:
        print("\n(Custom Graph class not available)")

    # Example 3: Find all paths
    print("\n" + "=" * 60)
    print("Example 3: Find All Paths")
    print("=" * 60)

    paths = find_all_paths(adj_list, 0, 4)
    print(f"\nAll paths from 0 to 4:")
    for i, path in enumerate(paths, 1):
        print(f"  Path {i}: {' -> '.join(map(str, path))}")

    # Example 4: Cycle detection
    print("\n" + "=" * 60)
    print("Example 4: Cycle Detection")
    print("=" * 60)

    print(f"\nDoes the graph have a cycle? {has_cycle_undirected(adj_list, 5)}")

    # Example 5: Connected components
    print("\n" + "=" * 60)
    print("Example 5: Connected Components")
    print("=" * 60)

    # Graph with multiple components
    disconnected_graph = {0: [1, 2], 1: [0, 2], 2: [0, 1], 3: [4], 4: [3], 5: []}

    components = connected_components(disconnected_graph, 6)
    print(f"\nConnected components:")
    for i, comp in enumerate(components, 1):
        print(f"  Component {i}: {comp}")

    # Example 6: Topological Sort (DAG)
    print("\n" + "=" * 60)
    print("Example 6: Topological Sort")
    print("=" * 60)

    # Directed acyclic graph (DAG)
    dag = {0: [1, 2], 1: [3], 2: [3], 3: [4], 4: []}

    topo_order = topological_sort_dfs(dag, 5)
    if topo_order:
        print(f"\nTopological order: {' -> '.join(map(str, topo_order))}")
    else:
        print("\nGraph has a cycle (not a DAG)")

    # Example 7: Bipartite check
    print("\n" + "=" * 60)
    print("Example 7: Bipartite Graph Check")
    print("=" * 60)

    bipartite_graph = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]}

    print(f"\nIs graph bipartite? {is_bipartite(bipartite_graph, 4)}")
    print(f"Is original graph bipartite? {is_bipartite(adj_list, 5)}")

    print("\n" + "=" * 60)
