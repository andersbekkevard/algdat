"""
DFS Edge Classification - Educational Implementation
From "Introduction to Algorithms" by Cormen, Leiserson, Rivest, and Stein

EDGE CLASSIFICATION IN DFS:
==========================

In a DFS of an undirected or directed graph G = (V, E), every edge can be classified
into one of four types based on the depth-first forest produced by the search:

1. TREE EDGES: Edges in the depth-first forest. Edge (u,v) is a tree edge if v was
   first discovered by exploring edge (u,v).

2. BACK EDGES: Edges (u,v) connecting a vertex u to an ancestor v in a depth-first
   tree. Self-loops are back edges. Back edges indicate cycles in directed graphs.

3. FORWARD EDGES: Non-tree edges (u,v) connecting a vertex u to a proper descendant v
   in a depth-first tree.

4. CROSS EDGES: All other edges. Can connect vertices in the same DFS tree (where
   neither is an ancestor of the other) or vertices in different DFS trees.

CLASSIFICATION ALGORITHM (using vertex colors):
===============================================

When exploring edge (u,v) from vertex u:
- If v.color == WHITE: (u,v) is a TREE EDGE
- If v.color == GRAY:  (u,v) is a BACK EDGE (v is an ancestor currently being explored)
- If v.color == BLACK: (u,v) is a FORWARD or CROSS EDGE
  - If u.d < v.d: FORWARD EDGE (v is a descendant that finished)
  - If u.d > v.d: CROSS EDGE (v is in a different branch or tree)

IMPORTANT PROPERTIES:
====================
- In DFS of an UNDIRECTED graph: only tree edges and back edges can occur
- In DFS of a DIRECTED graph: all four edge types can occur
- A directed graph is ACYCLIC (DAG) if and only if DFS yields no back edges
"""

from typing import List, Tuple, Dict, Set
from enum import Enum


class VertexColor(Enum):
    """
    Enumeration of vertex colors in DFS (CLRS)
    """

    WHITE = "WHITE"  # Undiscovered vertex
    GRAY = "GRAY"  # Discovered but not finished (currently being explored)
    BLACK = "BLACK"  # Finished vertex (all descendants explored)

    def __str__(self):
        return self.value


class EdgeType(Enum):
    """
    Enumeration of the four edge types in DFS (CLRS)
    """

    TREE = "TREE"  # Edges in the depth-first forest
    BACK = "BACK"  # Edges to ancestors (indicate cycles)
    FORWARD = "FORWARD"  # Edges to proper descendants (not in tree)
    CROSS = "CROSS"  # Edges between different branches or trees

    def __str__(self):
        return self.value


class Vertex:
    """Vertex in a graph with DFS attributes"""

    def __init__(self, name):
        self.name = name
        self.color = VertexColor.WHITE  # WHITE, GRAY, or BLACK
        self.pi = None  # Predecessor
        self.d = None  # Discovery time
        self.f = None  # Finish time

    def __repr__(self):
        return f"Vertex({self.name})"


class Graph:
    """Graph representation with adjacency list"""

    def __init__(self, directed=True):
        self.vertices = {}
        self.adj = {}
        self.directed = directed
        # Store edges for classification
        self.edges = []

    def add_vertex(self, name):
        """Add a vertex to the graph"""
        if name not in self.vertices:
            self.vertices[name] = Vertex(name)
            self.adj[name] = []

    def add_edge(self, u, v):
        """Add an edge from u to v"""
        if u not in self.vertices:
            self.add_vertex(u)
        if v not in self.vertices:
            self.add_vertex(v)

        self.adj[u].append(v)
        self.edges.append((u, v))

        # For undirected graphs, add reverse edge
        if not self.directed:
            self.adj[v].append(u)

    def get_vertices(self):
        """Return list of vertices"""
        return list(self.vertices.values())


class EdgeClassifier:
    """Classifies edges during DFS traversal using EdgeType enum"""

    def __init__(self):
        # Dictionary mapping EdgeType to list of edges
        self.edges = {
            EdgeType.TREE: [],
            EdgeType.BACK: [],
            EdgeType.FORWARD: [],
            EdgeType.CROSS: [],
        }

    def classify_edge(self, u, v, G):
        """
        Classify edge (u,v) based on v's color and discovery times

        CLRS Classification Rules:
        - WHITE vertex v: tree edge
        - GRAY vertex v: back edge
        - BLACK vertex v: forward or cross edge (use discovery times)

        Returns:
            EdgeType enum value
        """
        edge = (u.name, v.name)

        if v.color == VertexColor.WHITE:
            # Tree edge: v is being discovered for the first time via (u,v)
            self.edges[EdgeType.TREE].append(edge)
            return EdgeType.TREE

        elif v.color == VertexColor.GRAY:
            # Back edge: v is an ancestor of u (still being processed)
            self.edges[EdgeType.BACK].append(edge)
            return EdgeType.BACK

        elif v.color == VertexColor.BLACK:
            # v has already been fully processed
            if u.d < v.d:
                # Forward edge: v is a descendant of u
                self.edges[EdgeType.FORWARD].append(edge)
                return EdgeType.FORWARD
            else:
                # Cross edge: v is neither ancestor nor descendant
                self.edges[EdgeType.CROSS].append(edge)
                return EdgeType.CROSS

    def get_edges(self, edge_type: EdgeType) -> List[Tuple[str, str]]:
        """Get all edges of a specific type"""
        return self.edges[edge_type]

    def get_summary(self):
        """Return summary of edge classifications"""
        return {
            "tree": len(self.edges[EdgeType.TREE]),
            "back": len(self.edges[EdgeType.BACK]),
            "forward": len(self.edges[EdgeType.FORWARD]),
            "cross": len(self.edges[EdgeType.CROSS]),
            "total": sum(len(edges) for edges in self.edges.values()),
        }

    # Convenience properties for backward compatibility
    @property
    def tree_edges(self):
        return self.edges[EdgeType.TREE]

    @property
    def back_edges(self):
        return self.edges[EdgeType.BACK]

    @property
    def forward_edges(self):
        return self.edges[EdgeType.FORWARD]

    @property
    def cross_edges(self):
        return self.edges[EdgeType.CROSS]


def DFS_with_classification(G):
    """
    DFS with edge classification
    Returns EdgeClassifier object with all classified edges
    """
    classifier = EdgeClassifier()

    # Initialize all vertices
    for u in G.get_vertices():
        u.color = VertexColor.WHITE
        u.pi = None

    time = [0]

    # Visit each white vertex
    for u in G.get_vertices():
        if u.color == VertexColor.WHITE:
            DFS_VISIT_classify(G, u, time, classifier)

    return classifier


def DFS_VISIT_classify(G, u, time, classifier):
    """
    DFS-VISIT with edge classification
    Classifies each edge as it's encountered
    """
    # Discover vertex u
    time[0] = time[0] + 1
    u.d = time[0]
    u.color = VertexColor.GRAY

    # Explore each edge (u,v)
    for v_name in G.adj[u.name]:
        v = G.vertices[v_name]

        # Classify the edge BEFORE potentially recursing
        edge_type = classifier.classify_edge(u, v, G)

        # Only recurse on tree edges (WHITE vertices)
        if v.color == VertexColor.WHITE:
            v.pi = u
            DFS_VISIT_classify(G, v, time, classifier)

    # Finish vertex u
    time[0] = time[0] + 1
    u.f = time[0]
    u.color = VertexColor.BLACK


def print_edge_classification_results(G, classifier, graph_name, description):
    """Print detailed edge classification results"""
    print(f"\n{'='*70}")
    print(f"EDGE CLASSIFICATION: {graph_name}")
    print(f"{'='*70}")
    print(f"Description: {description}")
    print(f"Graph type: {'Directed' if G.directed else 'Undirected'}")
    print(f"Vertices: {len(G.vertices)}, Edges: {len(G.edges)}")
    print(f"{'='*70}\n")

    # Print adjacency list
    print("Adjacency List:")
    print("-" * 70)
    for v in sorted(G.adj.keys()):
        neighbors = G.adj[v]
        if neighbors:
            print(f"  {v} → {', '.join(neighbors)}")
        else:
            print(f"  {v} → (no outgoing edges)")
    print()

    # Print vertex discovery/finish times
    print("Vertex Timestamps:")
    print("-" * 70)
    print(f"{'Vertex':<10} {'Discovery (d)':<15} {'Finish (f)':<15} {'Interval':<15}")
    print("-" * 70)
    vertices = sorted(G.get_vertices(), key=lambda v: v.d if v.d else float("inf"))
    for v in vertices:
        interval = f"[{v.d}, {v.f}]" if v.d and v.f else "N/A"
        print(f"{v.name:<10} {v.d or 'N/A':<15} {v.f or 'N/A':<15} {interval:<15}")
    print()

    # Print edge classifications
    summary = classifier.get_summary()

    print("Edge Classification Results:")
    print("-" * 70)

    if classifier.tree_edges:
        print(f"\n  TREE EDGES ({len(classifier.tree_edges)}):")
        print(f"  {'└─'} These edges form the depth-first forest")
        for u, v in sorted(classifier.tree_edges):
            u_vertex = G.vertices[u]
            v_vertex = G.vertices[v]
            print(f"      ({u}, {v}) - {u} discovers {v} at time {v_vertex.d}")
    else:
        print(f"\n  TREE EDGES (0): None")

    if classifier.back_edges:
        print(f"\n  BACK EDGES ({len(classifier.back_edges)}):")
        print(
            f"  {'└─'} These edges point to ancestors (indicate cycles in directed graphs)"
        )
        for u, v in sorted(classifier.back_edges):
            u_vertex = G.vertices[u]
            v_vertex = G.vertices[v]
            print(
                f"      ({u}, {v}) - {u} [{u_vertex.d},{u_vertex.f}] → ancestor {v} [{v_vertex.d},{v_vertex.f}]"
            )
    else:
        print(f"\n  BACK EDGES (0): None")

    if classifier.forward_edges:
        print(f"\n  FORWARD EDGES ({len(classifier.forward_edges)}):")
        print(f"  {'└─'} These edges point to proper descendants (not in DFS tree)")
        for u, v in sorted(classifier.forward_edges):
            u_vertex = G.vertices[u]
            v_vertex = G.vertices[v]
            print(
                f"      ({u}, {v}) - {u} [{u_vertex.d},{u_vertex.f}] → descendant {v} [{v_vertex.d},{v_vertex.f}]"
            )
    else:
        print(f"\n  FORWARD EDGES (0): None")

    if classifier.cross_edges:
        print(f"\n  CROSS EDGES ({len(classifier.cross_edges)}):")
        print(f"  {'└─'} These edges connect different branches or trees")
        for u, v in sorted(classifier.cross_edges):
            u_vertex = G.vertices[u]
            v_vertex = G.vertices[v]
            print(
                f"      ({u}, {v}) - {u} [{u_vertex.d},{u_vertex.f}] → {v} [{v_vertex.d},{v_vertex.f}]"
            )
    else:
        print(f"\n  CROSS EDGES (0): None")

    # Summary statistics
    print(f"\n{'-'*70}")
    print(
        f"Summary: {summary['tree']} tree, {summary['back']} back, "
        f"{summary['forward']} forward, {summary['cross']} cross"
    )

    # Check for cycles
    if G.directed:
        if classifier.back_edges:
            print(f"⚠ CYCLE DETECTED: Graph contains back edges → NOT a DAG")
        else:
            print(f"✓ NO CYCLES: Graph is a DAG (Directed Acyclic Graph)")

    print(f"{'='*70}\n")


def create_dag_graph():
    """
    A Directed Acyclic Graph (DAG)
    Should have: tree edges, forward edges, cross edges
    Should NOT have: back edges
    """
    G = Graph(directed=True)
    G.add_edge("a", "b")
    G.add_edge("a", "c")
    G.add_edge("b", "d")
    G.add_edge("b", "e")
    G.add_edge("c", "e")
    G.add_edge("c", "f")
    G.add_edge("d", "e")  # This might be a forward or cross edge
    G.add_edge("a", "f")  # This might be a forward edge
    return G, "DAG Example", "A directed acyclic graph - no back edges"


def create_cyclic_graph():
    """
    A directed graph with cycles
    Should have: tree edges, back edges (indicating cycles)
    """
    G = Graph(directed=True)
    G.add_edge("1", "2")
    G.add_edge("2", "3")
    G.add_edge("3", "4")
    G.add_edge("4", "2")  # Back edge creating a cycle
    G.add_edge("3", "5")
    G.add_edge("5", "6")
    G.add_edge("6", "3")  # Another back edge
    return G, "Cyclic Graph", "Contains cycles (back edges present)"


def create_complete_example():
    """
    Graph designed to show all four edge types
    """
    G = Graph(directed=True)
    # Tree edges (primary DFS path)
    G.add_edge("s", "a")
    G.add_edge("a", "b")
    G.add_edge("b", "c")

    # Back edge (creates cycle)
    G.add_edge("c", "a")

    # Forward edge (skips ahead to descendant)
    G.add_edge("s", "c")

    # Cross edges (between different branches)
    G.add_edge("s", "d")
    G.add_edge("d", "e")
    G.add_edge("e", "b")  # Cross edge to different branch

    return G, "All Edge Types", "Designed to demonstrate all four edge types"


def create_undirected_graph():
    """
    An undirected graph
    Should only have: tree edges and back edges
    """
    G = Graph(directed=False)
    G.add_edge("a", "b")
    G.add_edge("b", "c")
    G.add_edge("c", "d")
    G.add_edge("d", "b")  # Creates a cycle
    G.add_edge("a", "e")
    return (
        G,
        "Undirected Graph",
        "Only tree and back edges (no forward/cross in undirected)",
    )


def create_clrs_figure_22_5():
    """
    Based on CLRS Figure 22.5 - classic example showing all edge types
    """
    G = Graph(directed=True)
    # Build the graph from CLRS
    G.add_edge("u", "v")
    G.add_edge("u", "x")
    G.add_edge("v", "y")
    G.add_edge("x", "v")
    G.add_edge("y", "x")
    G.add_edge("w", "y")
    G.add_edge("w", "z")
    G.add_edge("z", "z")  # Self-loop (back edge)
    return G, "CLRS Figure 22.5", "Classic textbook example with all edge types"


def create_parenthesis_structure():
    """
    Graph to illustrate the parenthesis structure
    """
    G = Graph(directed=True)
    G.add_edge("a", "b")
    G.add_edge("b", "c")
    G.add_edge("c", "d")
    G.add_edge("a", "e")
    G.add_edge("e", "f")
    G.add_edge("b", "f")  # Cross or forward edge
    return G, "Parenthesis Structure", "Demonstrates nested interval property"


def main():
    """Run edge classification on multiple example graphs"""
    print("\n" + "=" * 70)
    print(" " * 15 + "DFS EDGE CLASSIFICATION")
    print(" " * 10 + "Educational Implementation (CLRS)")
    print("=" * 70)
    print("\nThis program demonstrates the four types of edges in DFS:")
    print("  1. TREE edges    - Edges in the DFS forest")
    print("  2. BACK edges    - Edges to ancestors (indicate cycles)")
    print("  3. FORWARD edges - Edges to descendants (not in tree)")
    print("  4. CROSS edges   - All other edges")
    print("\n" + "=" * 70)

    # Create test graphs
    graphs = [
        create_dag_graph(),
        create_cyclic_graph(),
        create_complete_example(),
        create_clrs_figure_22_5(),
        create_parenthesis_structure(),
        create_undirected_graph(),
    ]

    # Classify edges in each graph
    for G, name, description in graphs:
        classifier = DFS_with_classification(G)
        print_edge_classification_results(G, classifier, name, description)
        print("\n" + "~" * 70 + "\n")


def demonstrate_enum_usage():
    """
    Demonstration of how to use the EdgeType and VertexColor enums directly
    """
    print("\n" + "=" * 70)
    print("ENUM USAGE DEMONSTRATION")
    print("=" * 70 + "\n")

    # Create a simple graph
    G = Graph(directed=True)
    G.add_edge("a", "b")
    G.add_edge("b", "c")
    G.add_edge("c", "a")  # Back edge (cycle)

    # Run DFS with classification
    classifier = DFS_with_classification(G)

    print("Example: Accessing edges by type using the EdgeType enum\n")

    # Access edges using the enum directly
    print(f"1. Using enum: classifier.get_edges(EdgeType.TREE)")
    print(f"   Result: {classifier.get_edges(EdgeType.TREE)}\n")

    print(f"2. Using enum: classifier.get_edges(EdgeType.BACK)")
    print(f"   Result: {classifier.get_edges(EdgeType.BACK)}\n")

    # Iterate over all edge types
    print("3. Iterating over all EdgeType enum values:")
    for edge_type in EdgeType:
        edges = classifier.get_edges(edge_type)
        print(f"   {edge_type.name:8} ({edge_type.value}): {edges}")

    print("\n" + "-" * 70 + "\n")
    print("Example: VertexColor enum usage\n")

    # Check vertex colors (all should be BLACK after DFS completes)
    for v in G.get_vertices():
        print(f"   Vertex {v.name}: color = {v.color} (enum: {v.color.name})")

    print("\n" + "-" * 70 + "\n")
    print("Benefits of using Enums:")
    print("  ✓ Type safety - prevents typos like 'TREA' instead of 'TREE'")
    print("  ✓ IDE autocomplete - easier to discover available options")
    print("  ✓ Clear intent - EdgeType.TREE is more explicit than 'TREE'")
    print("  ✓ Refactoring - changing enum values updates all usages")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

    # Uncomment to see enum usage demonstration
    # demonstrate_enum_usage()
