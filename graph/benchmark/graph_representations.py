"""
Graph Representations Comparison

This module implements three different graph representations:
1. Edge List - Simple list of edges
2. Adjacency List - Dictionary/list mapping vertices to their neighbors
3. Adjacency Matrix - 2D matrix representation

Each representation is benchmarked on common graph operations.
"""

from collections import defaultdict, deque
from typing import List, Tuple, Dict, Set, Optional
import heapq
import time
import random
import matplotlib.pyplot as plt
import numpy as np


# ============================================================================
# CONFIGURATION: Enable/Disable Graph Representations in Benchmarks
# ============================================================================
REPRESENTATIONS_CONFIG = {
    "Edge List": True,  # Set to False to exclude Edge List from benchmarks
    "Adjacency List": True,  # Set to False to exclude Adjacency List
    "Adjacency Matrix": True,  # Set to False to exclude Adjacency Matrix
}
# ============================================================================


class EdgeList:
    """
    Edge List Representation
    Stores graph as a simple list of edges (u, v, weight)

    Pros: Simple, space-efficient, easy to iterate through all edges
    Cons: Slow neighbor lookups, slow edge existence checks
    """

    def __init__(self, num_vertices: int, directed: bool = False):
        self.num_vertices = num_vertices
        self.directed = directed
        self.edges: List[Tuple[int, int, float]] = []

    def add_edge(self, u: int, v: int, weight: float = 1.0):
        """Add an edge to the graph"""
        self.edges.append((u, v, weight))
        if not self.directed:
            self.edges.append((v, u, weight))

    def has_edge(self, u: int, v: int) -> bool:
        """Check if edge exists between u and v"""
        for edge_u, edge_v, _ in self.edges:
            if edge_u == u and edge_v == v:
                return True
        return False

    def get_neighbors(self, u: int) -> List[Tuple[int, float]]:
        """Get all neighbors of vertex u with their weights"""
        neighbors = []
        for edge_u, edge_v, weight in self.edges:
            if edge_u == u:
                neighbors.append((edge_v, weight))
        return neighbors

    def get_all_vertices(self) -> Set[int]:
        """Get all vertices that have edges"""
        vertices = set()
        for u, v, _ in self.edges:
            vertices.add(u)
            vertices.add(v)
        return vertices


class AdjacencyList:
    """
    Adjacency List Representation
    Each vertex maps to a list of (neighbor, weight) tuples

    Pros: Space-efficient for sparse graphs, fast neighbor lookups
    Cons: Slower edge existence checks than adjacency matrix
    """

    def __init__(self, num_vertices: int, directed: bool = False):
        self.num_vertices = num_vertices
        self.directed = directed
        self.adj_list: Dict[int, List[Tuple[int, float]]] = defaultdict(list)

    def add_edge(self, u: int, v: int, weight: float = 1.0):
        """Add an edge to the graph"""
        self.adj_list[u].append((v, weight))
        if not self.directed:
            self.adj_list[v].append((u, weight))

    def has_edge(self, u: int, v: int) -> bool:
        """Check if edge exists between u and v"""
        if u not in self.adj_list:
            return False
        return any(neighbor == v for neighbor, _ in self.adj_list[u])

    def get_neighbors(self, u: int) -> List[Tuple[int, float]]:
        """Get all neighbors of vertex u with their weights"""
        return self.adj_list.get(u, [])

    def get_all_vertices(self) -> Set[int]:
        """Get all vertices in the graph"""
        return set(self.adj_list.keys())


class AdjacencyMatrix:
    """
    Adjacency Matrix Representation
    2D matrix where matrix[u][v] = weight if edge exists, else 0/infinity

    Pros: Fast edge existence checks, fast edge weight lookups
    Cons: Space-inefficient for sparse graphs (O(V²) space)
    """

    def __init__(self, num_vertices: int, directed: bool = False):
        self.num_vertices = num_vertices
        self.directed = directed
        # Initialize with infinity (no edge)
        self.matrix = [[float("inf")] * num_vertices for _ in range(num_vertices)]
        # Distance from vertex to itself is 0
        for i in range(num_vertices):
            self.matrix[i][i] = 0

    def add_edge(self, u: int, v: int, weight: float = 1.0):
        """Add an edge to the graph"""
        self.matrix[u][v] = weight
        if not self.directed:
            self.matrix[v][u] = weight

    def has_edge(self, u: int, v: int) -> bool:
        """Check if edge exists between u and v"""
        return self.matrix[u][v] != float("inf") and u != v

    def get_neighbors(self, u: int) -> List[Tuple[int, float]]:
        """Get all neighbors of vertex u with their weights"""
        neighbors = []
        for v in range(self.num_vertices):
            if self.matrix[u][v] != float("inf") and u != v:
                neighbors.append((v, self.matrix[u][v]))
        return neighbors

    def get_all_vertices(self) -> Set[int]:
        """Get all vertices in the graph"""
        vertices = set()
        for u in range(self.num_vertices):
            for v in range(self.num_vertices):
                if self.matrix[u][v] != float("inf") and u != v:
                    vertices.add(u)
                    vertices.add(v)
        return vertices if vertices else set(range(self.num_vertices))


# Graph Algorithm Implementations


def bfs(graph, start: int) -> Dict[int, int]:
    """
    Breadth-First Search
    Returns dictionary mapping each reachable vertex to its distance from start
    """
    distances = {start: 0}
    queue = deque([start])

    while queue:
        u = queue.popleft()
        for v, _ in graph.get_neighbors(u):
            if v not in distances:
                distances[v] = distances[u] + 1
                queue.append(v)

    return distances


def dfs(graph, start: int) -> Set[int]:
    """
    Depth-First Search
    Returns set of all vertices reachable from start
    """
    visited = set()
    stack = [start]

    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            for v, _ in graph.get_neighbors(u):
                if v not in visited:
                    stack.append(v)

    return visited


def dijkstra(graph, start: int) -> Dict[int, float]:
    """
    Dijkstra's Shortest Path Algorithm
    Returns dictionary mapping each vertex to its shortest distance from start
    """
    distances = {start: 0}
    pq = [(0, start)]  # (distance, vertex)
    visited = set()

    while pq:
        dist, u = heapq.heappop(pq)

        if u in visited:
            continue

        visited.add(u)

        for v, weight in graph.get_neighbors(u):
            new_dist = dist + weight
            if v not in distances or new_dist < distances[v]:
                distances[v] = new_dist
                heapq.heappush(pq, (new_dist, v))

    return distances


def check_all_edges(graph, edges_to_check: List[Tuple[int, int]]) -> int:
    """
    Check existence of multiple edges
    Returns count of edges that exist
    """
    count = 0
    for u, v in edges_to_check:
        if graph.has_edge(u, v):
            count += 1
    return count


def get_all_neighbors(graph, vertices: List[int]) -> int:
    """
    Get neighbors for multiple vertices
    Returns total count of neighbors
    """
    count = 0
    for u in vertices:
        count += len(graph.get_neighbors(u))
    return count


# Graph Generation Utilities


def generate_random_graph(
    num_vertices: int, num_edges: int, max_weight: float = 10.0, directed: bool = False
) -> List[Tuple[int, int, float]]:
    """Generate a random graph as list of edges"""
    edges = []
    edge_set = set()

    while len(edges) < num_edges:
        u = random.randint(0, num_vertices - 1)
        v = random.randint(0, num_vertices - 1)

        if u != v and (u, v) not in edge_set:
            weight = random.uniform(1, max_weight)
            edges.append((u, v, weight))
            edge_set.add((u, v))
            if not directed:
                edge_set.add((v, u))

    return edges


def build_graph(
    graph_class,
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    directed: bool = False,
):
    """Build a graph from edge list using specified representation"""
    graph = graph_class(num_vertices, directed)
    for u, v, weight in edges:
        graph.add_edge(u, v, weight)
    return graph


# Benchmarking Functions


def benchmark_construction(
    num_vertices: int, edges: List[Tuple[int, int, float]], directed: bool = False
) -> Dict[str, float]:
    """Benchmark graph construction time"""
    results = {}

    # Edge List
    if REPRESENTATIONS_CONFIG.get("Edge List", True):
        start = time.perf_counter()
        edge_list = build_graph(EdgeList, num_vertices, edges, directed)
        results["Edge List"] = time.perf_counter() - start

    # Adjacency List
    if REPRESENTATIONS_CONFIG.get("Adjacency List", True):
        start = time.perf_counter()
        adj_list = build_graph(AdjacencyList, num_vertices, edges, directed)
        results["Adjacency List"] = time.perf_counter() - start

    # Adjacency Matrix
    if REPRESENTATIONS_CONFIG.get("Adjacency Matrix", True):
        start = time.perf_counter()
        adj_matrix = build_graph(AdjacencyMatrix, num_vertices, edges, directed)
        results["Adjacency Matrix"] = time.perf_counter() - start

    return results


def benchmark_edge_check(
    graphs: Dict[str, any], test_edges: List[Tuple[int, int]]
) -> Dict[str, float]:
    """Benchmark edge existence checking"""
    results = {}

    for name, graph in graphs.items():
        start = time.perf_counter()
        check_all_edges(graph, test_edges)
        results[name] = time.perf_counter() - start

    return results


def benchmark_neighbor_query(
    graphs: Dict[str, any], test_vertices: List[int]
) -> Dict[str, float]:
    """Benchmark neighbor queries"""
    results = {}

    for name, graph in graphs.items():
        start = time.perf_counter()
        get_all_neighbors(graph, test_vertices)
        results[name] = time.perf_counter() - start

    return results


def benchmark_bfs(graphs: Dict[str, any], start_vertex: int) -> Dict[str, float]:
    """Benchmark BFS traversal"""
    results = {}

    for name, graph in graphs.items():
        start = time.perf_counter()
        bfs(graph, start_vertex)
        results[name] = time.perf_counter() - start

    return results


def benchmark_dfs(graphs: Dict[str, any], start_vertex: int) -> Dict[str, float]:
    """Benchmark DFS traversal"""
    results = {}

    for name, graph in graphs.items():
        start = time.perf_counter()
        dfs(graph, start_vertex)
        results[name] = time.perf_counter() - start

    return results


def benchmark_dijkstra(graphs: Dict[str, any], start_vertex: int) -> Dict[str, float]:
    """Benchmark Dijkstra's algorithm"""
    results = {}

    for name, graph in graphs.items():
        start = time.perf_counter()
        dijkstra(graph, start_vertex)
        results[name] = time.perf_counter() - start

    return results


# Comprehensive Benchmark Suite


def run_comprehensive_benchmark(
    num_vertices: int = 500,
    num_edges: int = 2000,
    num_tests: int = 100,
    directed: bool = False,
):
    """
    Run comprehensive benchmark comparing all graph representations
    """
    print(f"\n{'='*70}")
    print(f"COMPREHENSIVE GRAPH REPRESENTATION BENCHMARK")
    print(f"{'='*70}")
    print(f"Vertices: {num_vertices}")
    print(f"Edges: {num_edges}")
    print(f"Directed: {directed}")
    print(f"Test Queries: {num_tests}")
    print(f"{'='*70}\n")

    # Generate random graph
    print("Generating random graph...")
    edges = generate_random_graph(num_vertices, num_edges, directed=directed)

    # Build all enabled representations
    enabled_reps = [name for name, enabled in REPRESENTATIONS_CONFIG.items() if enabled]
    print(f"Building graph representations: {', '.join(enabled_reps)}...\n")
    construction_times = benchmark_construction(num_vertices, edges, directed)

    graphs = {}
    if REPRESENTATIONS_CONFIG.get("Edge List", True):
        graphs["Edge List"] = build_graph(EdgeList, num_vertices, edges, directed)
    if REPRESENTATIONS_CONFIG.get("Adjacency List", True):
        graphs["Adjacency List"] = build_graph(
            AdjacencyList, num_vertices, edges, directed
        )
    if REPRESENTATIONS_CONFIG.get("Adjacency Matrix", True):
        graphs["Adjacency Matrix"] = build_graph(
            AdjacencyMatrix, num_vertices, edges, directed
        )

    # Generate test data
    test_edges = [
        (random.randint(0, num_vertices - 1), random.randint(0, num_vertices - 1))
        for _ in range(num_tests)
    ]
    test_vertices = [random.randint(0, num_vertices - 1) for _ in range(num_tests)]
    start_vertex = random.randint(0, num_vertices - 1)

    # Run benchmarks
    print("Running benchmarks...\n")
    edge_check_times = benchmark_edge_check(graphs, test_edges)
    neighbor_query_times = benchmark_neighbor_query(graphs, test_vertices)
    bfs_times = benchmark_bfs(graphs, start_vertex)
    dfs_times = benchmark_dfs(graphs, start_vertex)
    dijkstra_times = benchmark_dijkstra(graphs, start_vertex)

    # Compile results
    all_results = {
        "Construction": construction_times,
        "Edge Check": edge_check_times,
        "Neighbor Query": neighbor_query_times,
        "BFS": bfs_times,
        "DFS": dfs_times,
        "Dijkstra": dijkstra_times,
    }

    # Print results
    print_results(all_results)

    # Visualize results
    visualize_results(all_results, num_vertices, num_edges)

    return all_results


def print_results(results: Dict[str, Dict[str, float]]):
    """Print benchmark results in a formatted table"""
    # Get enabled representations
    representations = [
        name for name, enabled in REPRESENTATIONS_CONFIG.items() if enabled
    ]

    if not representations:
        print("No representations enabled!")
        return

    # Create dynamic header
    header = f"{'Operation':<20} "
    for rep in representations:
        short_name = rep[:12]  # Abbreviate if needed
        header += f"{short_name:<15} "
    header += "Winner"

    print(f"\n{header}")
    print(f"{'-'*80}")

    for operation, times in results.items():
        line = f"{operation:<20} "

        # Add times for each enabled representation
        for rep in representations:
            time_ms = times.get(rep, float("inf"))
            line += f"{time_ms*1000:>12.4f}ms "

        # Find winner (lowest time)
        if times:
            winner = min(times.items(), key=lambda x: x[1])[0]
            line += f"{winner:<15}"

        print(line)

    print(f"{'-'*80}\n")


def visualize_results(
    results: Dict[str, Dict[str, float]], num_vertices: int, num_edges: int
):
    """Create beautiful visualizations of benchmark results"""

    # Get enabled representations
    representations = [
        name for name, enabled in REPRESENTATIONS_CONFIG.items() if enabled
    ]

    if not representations:
        print("No representations enabled for visualization!")
        return

    operations = list(results.keys())

    # Create figure with subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle(
        f"Graph Representation Performance Comparison\n"
        f"({num_vertices} vertices, {num_edges} edges)",
        fontsize=16,
        fontweight="bold",
    )

    # Dynamic color assignment with good contrast
    # Use a curated palette with high contrast colors
    color_palette = [
        "#E63946",  # Red
        "#06AED5",  # Cyan
        "#F77F00",  # Orange
        "#06D6A0",  # Teal
        "#9D4EDD",  # Purple
        "#FFB703",  # Yellow
        "#EF476F",  # Pink
        "#118AB2",  # Blue
    ]
    # Select colors based on number of enabled representations
    colors = color_palette[: len(representations)]

    # Individual operation plots
    for idx, (operation, times) in enumerate(results.items()):
        row = idx // 3
        col = idx % 3
        ax = axes[row, col]

        values = [times[rep] * 1000 for rep in representations]  # Convert to ms
        bars = ax.bar(
            range(len(representations)),
            values,
            color=colors,
            alpha=0.8,
            edgecolor="black",
            linewidth=1.5,
        )

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:.4f}",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
            )

        ax.set_ylabel("Time (ms)", fontweight="bold")
        ax.set_title(operation, fontweight="bold", fontsize=12)
        ax.set_xticks(range(len(representations)))
        ax.set_xticklabels(representations, rotation=15, ha="right")
        ax.grid(axis="y", alpha=0.3, linestyle="--")

        # Highlight the winner (lowest bar) with a star
        min_idx = values.index(min(values))
        ax.plot(
            min_idx,
            values[min_idx],
            marker="*",
            markersize=20,
            color="gold",
            markeredgecolor="black",
            markeredgewidth=1.5,
        )

    plt.tight_layout()
    plt.savefig(
        "/Users/andersbekkevard/dev/python/school/algdat/graph/benchmark_results.png",
        dpi=300,
        bbox_inches="tight",
    )
    print(f"Visualization saved to: graph/benchmark_results.png\n")
    plt.show()

    # Create a summary comparison chart
    fig, ax = plt.subplots(figsize=(14, 8))

    x = np.arange(len(operations))
    # Dynamic width based on number of representations
    num_reps = len(representations)
    width = 0.8 / num_reps if num_reps > 0 else 0.25

    for idx, rep in enumerate(representations):
        values = [results[op][rep] * 1000 for op in operations]
        offset = (idx - num_reps / 2 + 0.5) * width
        bars = ax.bar(
            x + offset,
            values,
            width,
            label=rep,
            color=colors[idx],
            alpha=0.8,
            edgecolor="black",
            linewidth=1.5,
        )

    ax.set_xlabel("Operations", fontweight="bold", fontsize=12)
    ax.set_ylabel("Time (ms)", fontweight="bold", fontsize=12)
    ax.set_title(
        "Graph Representations: Complete Performance Comparison",
        fontweight="bold",
        fontsize=14,
    )
    ax.set_xticks(x)
    ax.set_xticklabels(operations, rotation=15, ha="right")
    ax.legend(fontsize=11, framealpha=0.9)
    ax.grid(axis="y", alpha=0.3, linestyle="--")

    plt.tight_layout()
    plt.savefig(
        "/Users/andersbekkevard/dev/python/school/algdat/graph/benchmark_summary.png",
        dpi=300,
        bbox_inches="tight",
    )
    print(f"Summary visualization saved to: graph/benchmark_summary.png\n")
    plt.show()


def demo_usage():
    """Demonstrate usage of different graph representations"""
    print("\n" + "=" * 70)
    print("DEMO: Graph Representations Usage")
    print("=" * 70 + "\n")

    num_vertices = 5

    # Create sample edges
    edges = [
        (0, 1, 4.0),
        (0, 2, 1.0),
        (1, 2, 2.0),
        (1, 3, 5.0),
        (2, 3, 8.0),
        (2, 4, 3.0),
        (3, 4, 6.0),
    ]

    print("Sample Graph Edges:")
    for u, v, w in edges:
        print(f"  {u} -> {v} (weight: {w})")
    print()

    # Build graphs
    edge_list = build_graph(EdgeList, num_vertices, edges)
    adj_list = build_graph(AdjacencyList, num_vertices, edges)
    adj_matrix = build_graph(AdjacencyMatrix, num_vertices, edges)

    graphs = {
        "Edge List": edge_list,
        "Adjacency List": adj_list,
        "Adjacency Matrix": adj_matrix,
    }

    # Test operations
    print("Testing Operations:\n")

    # Check edge existence
    print(f"Has edge (0, 1)?")
    for name, graph in graphs.items():
        print(f"  {name}: {graph.has_edge(0, 1)}")
    print()

    # Get neighbors
    print(f"Neighbors of vertex 2:")
    for name, graph in graphs.items():
        neighbors = graph.get_neighbors(2)
        print(f"  {name}: {neighbors}")
    print()

    # BFS
    print(f"BFS from vertex 0:")
    for name, graph in graphs.items():
        distances = bfs(graph, 0)
        print(f"  {name}: {distances}")
    print()

    # Dijkstra
    print(f"Dijkstra from vertex 0:")
    for name, graph in graphs.items():
        distances = dijkstra(graph, 0)
        print(f"  {name}: {distances}")
    print()


if __name__ == "__main__":
    # Run demo
    demo_usage()

    # Run comprehensive benchmark with different graph sizes
    print("\n" + "=" * 70)
    print("STARTING COMPREHENSIVE BENCHMARKS")
    print("=" * 70)

    # Small graph (sparse)
    print("\n### SMALL SPARSE GRAPH ###")
    run_comprehensive_benchmark(num_vertices=100, num_edges=300, num_tests=50)

    # Medium graph (moderate density)
    print("\n### MEDIUM GRAPH ###")
    run_comprehensive_benchmark(num_vertices=500, num_edges=2000, num_tests=100)

    # Large graph (sparse)
    print("\n### LARGE SPARSE GRAPH ###")
    run_comprehensive_benchmark(num_vertices=1000, num_edges=5000, num_tests=100)

    print("\n" + "=" * 70)
    print("ALL BENCHMARKS COMPLETED!")
    print("=" * 70 + "\n")
