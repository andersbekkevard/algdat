"""
Depth-First Search (DFS) Implementation
From "Introduction to Algorithms" by Cormen, Leiserson, Rivest, and Stein
"""


class Vertex:
    """Vertex in a graph with DFS attributes"""

    def __init__(self, name):
        self.name = name
        self.color = "WHITE"  # WHITE, GRAY, or BLACK
        self.pi = None  # Predecessor/parent
        self.d = None  # Discovery time
        self.f = None  # Finish time

    def __repr__(self):
        return f"Vertex({self.name})"


class Graph:
    """Graph representation with adjacency list"""

    def __init__(self):
        self.vertices = {}
        self.adj = {}

    def add_vertex(self, name):
        """Add a vertex to the graph"""
        if name not in self.vertices:
            self.vertices[name] = Vertex(name)
            self.adj[name] = []

    def add_edge(self, u, v):
        """Add a directed edge from u to v"""
        if u not in self.vertices:
            self.add_vertex(u)
        if v not in self.vertices:
            self.add_vertex(v)
        self.adj[u].append(v)

    def get_vertices(self):
        """Return list of vertices"""
        return list(self.vertices.values())


def DFS(G):
    """
    Depth-First Search algorithm (CLRS pseudocode)

    DFS(G)
    1 for each vertex u ∈ G.V
    2   u.color = WHITE
    3   u.π = NIL
    4 time = 0
    5 for each vertex u ∈ G.V
    6   if u.color == WHITE
    7     DFS-VISIT(G, u)
    """
    # Lines 1-3: Initialize all vertices
    for u in G.get_vertices():
        u.color = "WHITE"
        u.pi = None

    # Line 4: Initialize time
    time = [0]  # Using list to make it mutable in nested function

    # Lines 5-7: Visit each white vertex
    for u in G.get_vertices():
        if u.color == "WHITE":
            DFS_VISIT(G, u, time)


def DFS_VISIT(G, u, time):
    """
    DFS-VISIT helper function (CLRS pseudocode)

    DFS-VISIT(G, u)
    1 time = time + 1              // white vertex u has just been discovered
    2 u.d = time
    3 u.color = GRAY
    4 for each vertex v in G.Adj[u]// explore each edge (u, v)
    5   if v.color == WHITE
    6     v.π = u
    7     DFS-VISIT(G, v)
    8 time = time + 1
    9 u.f = time
    10 u.color = BLACK             // blacken u; it is finished
    """
    # Lines 1-3: Discover vertex u
    time[0] = time[0] + 1
    u.d = time[0]
    u.color = "GRAY"

    # Lines 4-7: Explore edges
    for v_name in G.adj[u.name]:
        v = G.vertices[v_name]
        if v.color == "WHITE":
            v.pi = u
            DFS_VISIT(G, v, time)

    # Lines 8-10: Finish vertex u
    time[0] = time[0] + 1
    u.f = time[0]
    u.color = "BLACK"


def print_dfs_results(G, graph_name):
    """Print DFS results in a formatted table"""
    print(f"\n{'='*60}")
    print(f"DFS Results for {graph_name}")
    print(f"{'='*60}")

    # Sort vertices by name for consistent output
    vertices = sorted(G.get_vertices(), key=lambda v: v.name)

    # Print table header
    print(f"{'Vertex':<10} {'π (Parent)':<15} {'d (Discovery)':<18} {'f (Finish)':<15}")
    print(f"{'-'*60}")

    # Print each vertex's information
    for v in vertices:
        parent = v.pi.name if v.pi else "NIL"
        discovery = v.d if v.d is not None else "N/A"
        finish = v.f if v.f is not None else "N/A"
        print(f"{v.name:<10} {parent:<15} {discovery:<18} {finish:<15}")

    print(f"{'='*60}\n")


def create_graph_1():
    """
    Example graph from CLRS Figure 22.4
    A simple directed graph with a single path
    """
    G = Graph()
    G.add_edge("u", "v")
    G.add_edge("u", "x")
    G.add_edge("v", "y")
    G.add_edge("w", "y")
    G.add_edge("w", "z")
    G.add_edge("x", "v")
    G.add_edge("y", "x")
    G.add_edge("z", "z")
    return G, "Graph 1: CLRS-style directed graph"


def create_graph_2():
    """
    A simple DAG (Directed Acyclic Graph)
    """
    G = Graph()
    G.add_edge("a", "b")
    G.add_edge("a", "c")
    G.add_edge("b", "d")
    G.add_edge("c", "d")
    G.add_edge("d", "e")
    return G, "Graph 2: Simple DAG"


def create_graph_3():
    """
    A graph with multiple connected components
    """
    G = Graph()
    # Component 1
    G.add_edge("1", "2")
    G.add_edge("2", "3")
    G.add_edge("3", "1")

    # Component 2
    G.add_edge("4", "5")
    G.add_edge("5", "6")

    # Component 3 (isolated vertex)
    G.add_vertex("7")

    return G, "Graph 3: Multiple connected components"


def create_graph_4():
    """
    A tree structure
    """
    G = Graph()
    G.add_edge("root", "left")
    G.add_edge("root", "right")
    G.add_edge("left", "left-left")
    G.add_edge("left", "left-right")
    G.add_edge("right", "right-left")
    return G, "Graph 4: Tree structure"


def verify_timestamp_property(G, graph_name):
    """
    Verify the DFS Timestamp Property:

    THEOREM: For a graph G with n vertices, after running DFS:
    1. Each timestamp t ∈ {1, 2, 3, ..., 2n} is used exactly once
    2. No timestamp is used more than once (either as d or f)
    3. No timestamp is skipped

    PROOF BY VERIFICATION:
    - time starts at 0
    - time increments by 1 exactly twice per vertex (once when discovered, once when finished)
    - Each vertex is visited exactly once (color prevents revisiting)
    - Therefore: n vertices → 2n timestamp assignments → timestamps = {1, 2, ..., 2n}
    """
    print(f"\n{'='*60}")
    print(f"TIMESTAMP PROPERTY VERIFICATION: {graph_name}")
    print(f"{'='*60}")

    vertices = G.get_vertices()
    n = len(vertices)
    expected_max_time = 2 * n

    # Collect all discovery and finish times
    all_times = []
    d_times = []
    f_times = []

    for v in vertices:
        if v.d is not None:
            all_times.append(v.d)
            d_times.append(v.d)
        if v.f is not None:
            all_times.append(v.f)
            f_times.append(v.f)

    # Sort for display
    all_times_sorted = sorted(all_times)

    print(f"\nGraph has {n} vertices")
    print(f"Expected timestamp range: 1 to {expected_max_time}")
    print(f"Expected number of timestamps: {expected_max_time}")
    print(f"Actual number of timestamps: {len(all_times)}")

    # Check 1: Verify we have exactly 2n timestamps
    check1_passed = len(all_times) == expected_max_time
    print(
        f"\n✓ CHECK 1: Exactly 2n timestamps"
        if check1_passed
        else f"\n✗ CHECK 1 FAILED: Expected {expected_max_time}, got {len(all_times)}"
    )

    # Check 2: Verify no duplicates (each timestamp used at most once)
    duplicates = []
    seen = set()
    for t in all_times:
        if t in seen:
            duplicates.append(t)
        seen.add(t)

    check2_passed = len(duplicates) == 0
    if check2_passed:
        print(f"✓ CHECK 2: No timestamp used more than once")
    else:
        print(f"✗ CHECK 2 FAILED: Duplicate timestamps found: {duplicates}")

    # Check 3: Verify no gaps (all timestamps from 1 to 2n are present)
    expected_set = set(range(1, expected_max_time + 1))
    actual_set = set(all_times)
    missing = expected_set - actual_set
    extra = actual_set - expected_set

    check3_passed = len(missing) == 0 and len(extra) == 0
    if check3_passed:
        print(
            f"✓ CHECK 3: No missing timestamps, all in range [1, {expected_max_time}]"
        )
    else:
        if missing:
            print(f"✗ CHECK 3 FAILED: Missing timestamps: {sorted(missing)}")
        if extra:
            print(f"✗ CHECK 3 FAILED: Unexpected timestamps: {sorted(extra)}")

    # Check 4: Verify d < f for each vertex (parenthesis property)
    check4_passed = True
    violations = []
    for v in vertices:
        if v.d is not None and v.f is not None:
            if v.d >= v.f:
                check4_passed = False
                violations.append(f"{v.name}: d={v.d}, f={v.f}")

    if check4_passed:
        print(f"✓ CHECK 4: For all vertices, d < f (discovery before finish)")
    else:
        print(f"✗ CHECK 4 FAILED: Violations found:")
        for violation in violations:
            print(f"  {violation}")

    # Summary
    all_passed = check1_passed and check2_passed and check3_passed and check4_passed

    print(f"\n{'-'*60}")
    if all_passed:
        print("✓ ALL CHECKS PASSED - Timestamp property verified!")
        print(f"\nTimestamp sequence: {all_times_sorted}")
        print(f"This forms a perfect sequence [1, 2, ..., {expected_max_time}]")
    else:
        print("✗ SOME CHECKS FAILED - Property violated!")

    print(f"{'='*60}\n")

    return all_passed


def print_graph_structure(G, graph_name):
    """Print the adjacency list representation of the graph"""
    print(f"\n{'='*60}")
    print(f"Graph Structure: {graph_name}")
    print(f"{'='*60}")

    vertices = sorted(G.adj.keys())
    for v in vertices:
        neighbors = G.adj[v]
        if neighbors:
            print(f"{v} → {', '.join(neighbors)}")
        else:
            print(f"{v} → (no outgoing edges)")
    print(f"{'='*60}\n")


def main():
    """Run DFS on multiple test graphs"""
    print("\n" + "=" * 60)
    print("DEPTH-FIRST SEARCH (DFS) IMPLEMENTATION")
    print("From 'Introduction to Algorithms' (CLRS)")
    print("=" * 60)

    # Create test graphs
    graphs = [create_graph_1(), create_graph_2(), create_graph_3(), create_graph_4()]

    # Run DFS on each graph
    for G, graph_name in graphs:
        print_graph_structure(G, graph_name)
        DFS(G)
        print_dfs_results(G, graph_name)

        # VERIFICATION: Prove timestamp property
        # Comment out the line below to disable verification
        verify_timestamp_property(G, graph_name)

        # Add spacing between graphs
        print("\n" + "~" * 60 + "\n")


if __name__ == "__main__":
    main()
