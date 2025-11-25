"""
A2025S - Path Finding with Space Constraints

Implements has_path(G, s_0, t_0, k) to find if a path exists between two nodes
using at most k edges, with O(lg k) space complexity.

Algorithm: Divide-and-conquer approach that recursively checks intermediate vertices,
splitting the edge budget in half at each level.
"""

import math
from contextlib import contextmanager


# ============================================================================
# Graph Data Structure
# ============================================================================


class Node:
    def __init__(self, value):
        self.value = value
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def __repr__(self):
        return f"Node({self.value})"


class Graph:
    def __init__(self):
        self.vertices = []

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_edge(self, u, v):
        """Add undirected edge between u and v"""
        u.add_neighbor(v)
        v.add_neighbor(u)


# ============================================================================
# Recursion Tracking (for space complexity verification)
# ============================================================================

_recursion_tracker = {"max_depth": 0, "current_depth": 0, "enabled": False}


@contextmanager
def track_recursion_depth():
    """Context manager to track maximum recursion depth for testing"""
    _recursion_tracker["enabled"] = True
    _recursion_tracker["max_depth"] = 0
    _recursion_tracker["current_depth"] = 0
    try:
        yield _recursion_tracker
    finally:
        _recursion_tracker["enabled"] = False


# ============================================================================
# Main Algorithm
# ============================================================================


def has_path(G, s_0, t_0, k=None):
    """
    Check if a path exists from s_0 to t_0 using at most k edges.

    Args:
        G: Graph to search
        s_0: Start node
        t_0: Target node
        k: Maximum edges allowed (default: |V| - 1)

    Returns:
        True if path exists, False otherwise

    Space Complexity: O(lg k)

    Algorithm: For each intermediate vertex v, recursively check if
    s_0 → v (with k/2 edges) and v → t_0 (with k/2 edges) both exist.
    """
    if k is None:
        k = len(G.vertices) - 1

    def recursive_solve(s, t, remaining_edges):
        # Track recursion depth for testing
        if _recursion_tracker["enabled"]:
            _recursion_tracker["current_depth"] += 1
            _recursion_tracker["max_depth"] = max(
                _recursion_tracker["max_depth"], _recursion_tracker["current_depth"]
            )

        try:
            # Base cases
            if s == t:
                return True
            if t in s.neighbors:
                return True
            if remaining_edges <= 1:
                return False

            # Divide-and-conquer: split edge budget
            k_1 = remaining_edges // 2
            k_2 = remaining_edges - k_1

            # Try each intermediate vertex v
            for v in G.vertices:
                if v == s_0 or v == t_0:
                    continue
                if recursive_solve(s, v, k_1) and recursive_solve(v, t, k_2):
                    return True

            return False
        finally:
            if _recursion_tracker["enabled"]:
                _recursion_tracker["current_depth"] -= 1

    return recursive_solve(s_0, t_0, k)


# ============================================================================
# Helper Functions for Building Test Graphs
# ============================================================================


def build_graph(node_labels, edges):
    """Build graph from labels and edge list. Returns (Graph, {label: Node})."""
    g = Graph()
    nodes = {label: Node(label) for label in node_labels}
    for node in nodes.values():
        g.add_vertex(node)
    for u, v in edges:
        g.add_edge(nodes[u], nodes[v])
    return g, nodes


def build_path_graph(length):
    """Build linear path: A-B-C-D-..."""
    labels = [chr(65 + i) for i in range(length)]
    edges = [(labels[i], labels[i + 1]) for i in range(length - 1)]
    return build_graph(labels, edges)


def build_star_graph(center, leaves):
    """Build star graph with center connected to all leaves"""
    labels = [center] + list(leaves)
    edges = [(center, leaf) for leaf in leaves]
    return build_graph(labels, edges)


def build_cycle_graph(labels):
    """Build cycle graph from labels"""
    edges = [(labels[i], labels[(i + 1) % len(labels)]) for i in range(len(labels))]
    return build_graph(labels, edges)


# ============================================================================
# Test Runner
# ============================================================================


def run_test_case(test_name, graph, nodes, start, end, k, expected, description=""):
    """Run single test case and print result"""
    result = has_path(graph, nodes[start], nodes[end], k)
    status = "✅" if result == expected else "❌"
    desc_str = f" - {description}" if description else ""
    k_str = f"k={k}" if k is not None else "auto k"
    print(
        f"  {start} → {end} ({k_str}): {result:5} (expected {expected:5}) {status}{desc_str}"
    )
    return result == expected


# ============================================================================
# Correctness Tests
# ============================================================================


def test_has_path():
    """Test correctness of has_path function"""
    print("Testing has_path function...")
    print("=" * 70)

    all_passed = True

    # Test 1: Base cases
    print("\n📋 Test 1: Base Cases")
    g, nodes = build_path_graph(3)  # A-B-C
    all_passed &= run_test_case("Base-1", g, nodes, "A", "A", 0, True, "same node")
    all_passed &= run_test_case(
        "Base-2", g, nodes, "A", "B", 1, True, "direct neighbor"
    )
    all_passed &= run_test_case(
        "Base-3", g, nodes, "A", "C", 1, False, "too far for k=1"
    )

    # Test 2: Linear path graphs
    print("\n📋 Test 2: Linear Path Graphs")
    g, nodes = build_path_graph(4)  # A-B-C-D
    all_passed &= run_test_case("Linear-1", g, nodes, "A", "C", 2, True, "2 edges")
    all_passed &= run_test_case("Linear-2", g, nodes, "A", "D", 3, True, "3 edges")
    all_passed &= run_test_case(
        "Linear-3", g, nodes, "A", "D", 2, False, "insufficient k"
    )

    g, nodes = build_path_graph(6)  # A-B-C-D-E-F
    all_passed &= run_test_case("Linear-4", g, nodes, "A", "F", 5, True, "5 edges")
    all_passed &= run_test_case("Linear-5", g, nodes, "B", "E", 3, True, "middle nodes")

    # Test 3: Star graphs
    print("\n📋 Test 3: Star Graphs")
    g, nodes = build_star_graph("A", "BCD")  # A in center
    all_passed &= run_test_case("Star-1", g, nodes, "B", "C", 2, True, "through center")
    all_passed &= run_test_case("Star-2", g, nodes, "B", "D", 2, True, "through center")
    all_passed &= run_test_case("Star-3", g, nodes, "B", "C", 1, False, "not direct")
    all_passed &= run_test_case("Star-4", g, nodes, "A", "B", 1, True, "to center")

    # Test 4: Cycle graphs
    print("\n📋 Test 4: Cycle Graphs")
    g, nodes = build_cycle_graph("ABCD")  # A-B-C-D-A
    all_passed &= run_test_case("Cycle-1", g, nodes, "A", "C", 2, True, "shortest path")
    all_passed &= run_test_case("Cycle-2", g, nodes, "A", "D", 1, True, "direct edge")
    all_passed &= run_test_case("Cycle-3", g, nodes, "B", "D", 2, True, "via C")

    # Test 5: Disconnected graphs
    print("\n📋 Test 5: Disconnected Graphs")
    g, nodes = build_graph("ABCD", [("A", "B")])  # A-B, C, D isolated
    all_passed &= run_test_case("Disconn-1", g, nodes, "A", "C", 10, False, "no path")
    all_passed &= run_test_case("Disconn-2", g, nodes, "C", "D", 10, False, "no path")
    all_passed &= run_test_case("Disconn-3", g, nodes, "A", "B", 1, True, "connected")

    # Test 6: Grid-like graph
    print("\n📋 Test 6: Grid-like Graph")
    # A-B-C
    # | | |
    # D-E-F
    g, nodes = build_graph(
        "ABCDEF",
        [
            ("A", "B"),
            ("B", "C"),
            ("D", "E"),
            ("E", "F"),
            ("A", "D"),
            ("B", "E"),
            ("C", "F"),
        ],
    )
    all_passed &= run_test_case("Grid-1", g, nodes, "A", "F", 3, True, "diagonal")
    all_passed &= run_test_case("Grid-2", g, nodes, "A", "C", 2, True, "across top")
    all_passed &= run_test_case("Grid-3", g, nodes, "D", "C", 3, True, "diagonal up")

    # Test 7: Complex graph with multiple paths
    print("\n📋 Test 7: Multiple Paths")
    #   B - C
    #  / \ / \
    # A   X   D
    #  \ / \ /
    #   E - F
    g, nodes = build_graph(
        "ABCDEF",
        [
            ("A", "B"),
            ("A", "E"),
            ("B", "C"),
            ("B", "E"),
            ("C", "D"),
            ("C", "F"),
            ("E", "F"),
            ("F", "D"),
        ],
    )
    all_passed &= run_test_case("Multi-1", g, nodes, "A", "D", 3, True, "3-edge path")
    all_passed &= run_test_case("Multi-2", g, nodes, "A", "D", 4, True, "4-edge path")
    all_passed &= run_test_case("Multi-3", g, nodes, "A", "F", 2, True, "2-edge path")

    print("\n" + "=" * 70)
    if all_passed:
        print("✅ All correctness tests passed!")
    else:
        print("❌ Some correctness tests failed!")
    print("=" * 70)

    return all_passed


# ============================================================================
# Space Complexity Tests
# ============================================================================


def test_space_complexity():
    """Verify O(lg k) space complexity by checking recursion depth"""
    print("\n" + "=" * 70)
    print("Testing space complexity (O(lg k))...")
    print("=" * 70)

    g, nodes = build_path_graph(16)
    node_list = [chr(65 + i) for i in range(16)]

    test_cases = [
        (1, "Base case"),
        (2, "Small k"),
        (4, "k=4"),
        (8, "k=8"),
        (16, "k=16"),
        (32, "k=32"),
        (64, "k=64"),
        (128, "k=128"),
        (256, "k=256"),
    ]

    print(
        f"\n{'k':>6} | {'Max Depth':>10} | {'log₂(k)':>8} | {'Upper Bound':>12} | {'Status':>6} | {'Description':>15}"
    )
    print("-" * 80)

    all_passed = True

    for k, description in test_cases:
        with track_recursion_depth() as tracker:
            result = has_path(g, nodes[node_list[0]], nodes[node_list[-1]], k)
            actual_depth = tracker["max_depth"]

        log_k = math.log2(k) if k > 0 else 0
        expected_upper_bound = math.ceil(log_k) * 2 + 3
        is_logarithmic = actual_depth <= expected_upper_bound

        status = "✅" if is_logarithmic else "❌"
        if not is_logarithmic:
            all_passed = False

        print(
            f"{k:6d} | {actual_depth:10d} | {log_k:8.2f} | {expected_upper_bound:12d} | {status:>6} | {description:>15}"
        )

    # Verify depth grows logarithmically as k increases
    print("\n" + "-" * 80)
    print("Growth Analysis:")
    print("-" * 80)

    depths = []
    k_values = [2**i for i in range(1, 9)]

    for k in k_values:
        with track_recursion_depth() as tracker:
            has_path(g, nodes[node_list[0]], nodes[node_list[-1]], k)
            depths.append(tracker["max_depth"])

    print(f"\nk values:      {k_values}")
    print(f"Max depths:    {depths}")
    print(f"log₂(k):       {[round(math.log2(k), 1) for k in k_values]}")

    # Check depth grows slowly (logarithmically, not linearly)
    growth_is_log = all(depths[i + 1] - depths[i] <= 4 for i in range(len(depths) - 1))

    print(f"\nLogarithmic growth verified: {'✅ Yes' if growth_is_log else '❌ No'}")
    all_passed &= growth_is_log

    print("\n" + "=" * 70)
    if all_passed:
        print("✅ All space complexity tests passed! Function uses O(lg k) space.")
    else:
        print("❌ Some space complexity tests failed!")
    print("=" * 70)

    return all_passed


def demo_clean_api():
    """Demonstrate the clean API of has_path()"""
    print("\n" + "=" * 70)
    print("Demo: Clean API with has_path()")
    print("=" * 70)

    print("\n📝 Example 1: Simple path A-B-C-D")
    g, nodes = build_path_graph(4)
    print(f"  has_path(g, A, D): {has_path(g, nodes['A'], nodes['D'])}")
    print(f"  has_path(g, A, D, k=2): {has_path(g, nodes['A'], nodes['D'], k=2)}")
    print(f"  has_path(g, A, D, k=3): {has_path(g, nodes['A'], nodes['D'], k=3)}")

    print("\n📝 Example 2: Star graph with center A")
    g, nodes = build_star_graph("A", "BCD")
    print(f"  has_path(g, B, C): {has_path(g, nodes['B'], nodes['C'])}")
    print(f"  has_path(g, B, D): {has_path(g, nodes['B'], nodes['D'])}")

    print("\n📝 Example 3: Disconnected graph")
    g, nodes = build_graph("ABCD", [("A", "B")])
    print(f"  has_path(g, A, B): {has_path(g, nodes['A'], nodes['B'])}")
    print(f"  has_path(g, A, C): {has_path(g, nodes['A'], nodes['C'])}")

    print("\n" + "=" * 70)
    print("✅ Clean API demonstration complete!")
    print("   Notice: Only 3 parameters needed (G, s_0, t_0)")
    print("   Optional: Add k parameter for custom edge budget")
    print("=" * 70)


if __name__ == "__main__":
    test_has_path()
    test_space_complexity()
    demo_clean_api()
