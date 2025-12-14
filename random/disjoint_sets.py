class Node:
    def __init__(self, value):
        self.value = value
        self.p = self
        self.r = 0

    def __repr__(self):
        return f"Node({self.value})"


def make_set(item):
    return Node(item)


def find_set_single_compression(u: Node) -> Node:
    p = u.p
    while p != p.p:
        p = p.p
    u.p = p
    return u.p


def find_set_r(u: Node) -> Node:
    """
    If u is the parent: it returns itself.
    If not: It calls recursively, so we get the parent of parents in the chain
    Which will return the chain representative
    Compresses
    And then returns
    """
    if u.p != u:
        u.p = find_set_r(u.p)
    return u.p


def find_set(u: Node) -> Node:
    p = u.p
    while p != p.p:
        p = p.p
    # Now p is the top object
    current = u
    while current.p != p:
        next = current.p
        current.p = p
        current = next
    return p


def union(u: Node, v: Node):
    link(find_set(u), find_set(v))


def link(u: Node, v: Node):
    if u.r >= v.r:
        v.p = u
        u.r = max(u.r, v.r + 1)
    else:
        u.p = v
        v.r = max(v.r, u.r + 1)


class Graph:
    """Graph data structure with adjacency list representation."""

    def __init__(self, vertices: list[Node]):
        self.vertices: list[Node] = vertices
        self.E: dict[Node, list[Node]] = {v: [] for v in vertices}

    def add_edge(self, u: Node, v: Node):
        """Add an edge between vertices u and v."""
        if u not in self.E:
            self.E[u] = []
        if v not in self.E:
            self.E[v] = []
        if v not in self.E[u]:
            self.E[u].append(v)
        if u not in self.E[v]:
            self.E[v].append(u)


def connected_components(G: Graph) -> dict[Node, Node]:
    """
    Find connected components using disjoint sets.
    Assumes vertices are already initialized as disjoint sets (via make_set).
    Returns a dictionary mapping each node to its representative.
    """
    # Union vertices connected by edges
    for u in G.E:
        for v in G.E[u]:
            union(u, v)

    # Return mapping of each node to its representative
    return {vertex: find_set(vertex) for vertex in G.vertices}


def benchmark_find_set():
    """Benchmark find_set (iterative) vs find_set_r (recursive)."""
    import time

    def create_chain_structure(n: int) -> list[Node]:
        """Create a chain structure: 1 -> 2 -> 3 -> ... -> n (n is root)"""
        nodes = [make_set(i) for i in range(1, n + 1)]
        for i in range(n - 1):
            nodes[i].p = nodes[i + 1]
        nodes[-1].p = nodes[-1]  # Root points to itself
        return nodes

    def create_tree_structure(n: int) -> list[Node]:
        """Create a tree structure with depth log(n)"""
        nodes = [make_set(i) for i in range(1, n + 1)]
        nodes[0].p = nodes[0]  # Root points to itself
        # Create a balanced tree structure
        for i in range(1, n):
            parent_idx = (i - 1) // 2
            nodes[i].p = nodes[parent_idx]
        return nodes

    def reset_structure(nodes: list[Node], structure_type: str):
        """Reset nodes to the original structure."""
        # Reset all nodes first
        for node in nodes:
            node.p = node
            node.r = 0

        if structure_type == "chain":
            # Create chain: 1 -> 2 -> 3 -> ... -> n (n is root)
            for i in range(len(nodes) - 1):
                nodes[i].p = nodes[i + 1]
            nodes[-1].p = nodes[-1]  # Root points to itself
        elif structure_type == "tree":
            # Create tree: node 0 is root, others point to parent
            nodes[0].p = nodes[0]  # Root points to itself
            for i in range(1, len(nodes)):
                parent_idx = (i - 1) // 2
                nodes[i].p = nodes[parent_idx]

    test_cases = [
        ("Small chain (10 nodes)", 10, "chain"),
        ("Medium chain (100 nodes)", 100, "chain"),
        ("Large chain (1000 nodes)", 1000, "chain"),
        ("Small tree (100 nodes)", 100, "tree"),
        ("Medium tree (1000 nodes)", 1000, "tree"),
        ("Large tree (10000 nodes)", 10000, "tree"),
    ]

    num_find_operations = 1000

    print("=" * 70)
    print("BENCHMARK: find_set (iterative) vs find_set_r (recursive)")
    print("=" * 70)
    print(f"Operations per test: {num_find_operations:,} find operations\n")

    results = []

    for test_name, n, structure_type in test_cases:
        print(f"Test: {test_name}")
        print("-" * 70)

        # Create structure
        if structure_type == "chain":
            nodes = create_chain_structure(n)
        else:
            nodes = create_tree_structure(n)

        # Test iterative version
        reset_structure(nodes, structure_type)
        start = time.perf_counter()
        for _ in range(num_find_operations):
            find_set(nodes[0])  # Find from deepest node
        iterative_time = time.perf_counter() - start

        # Test recursive version
        reset_structure(nodes, structure_type)
        recursive_time = None
        recursion_error = False
        try:
            start = time.perf_counter()
            for _ in range(num_find_operations):
                find_set_r(nodes[0])  # Find from deepest node
            recursive_time = time.perf_counter() - start
        except RecursionError:
            recursion_error = True
            recursive_time = None

        # Calculate speedup and print results
        if recursion_error:
            speedup_factor = float("inf")
            faster = "iterative"
            print(f"  Iterative (find_set):     {iterative_time*1000:.4f} ms")
            print(
                f"  Recursive (find_set_r):    ⚠️  RecursionError (exceeded max depth)"
            )
            print(
                f"  Speedup:                   N/A (iterative avoids recursion limit)"
            )
        elif recursive_time is not None and recursive_time > 0:
            speedup = iterative_time / recursive_time
            faster = "iterative" if speedup < 1 else "recursive"
            speedup_factor = 1 / speedup if speedup < 1 else speedup
            print(f"  Iterative (find_set):     {iterative_time*1000:.4f} ms")
            print(f"  Recursive (find_set_r):    {recursive_time*1000:.4f} ms")
            print(
                f"  Speedup:                   {speedup_factor:.2f}x ({faster} is faster)"
            )
        else:
            speedup_factor = float("inf")
            faster = "iterative"
            print(f"  Iterative (find_set):     {iterative_time*1000:.4f} ms")
            print(f"  Recursive (find_set_r):    N/A")
            print(f"  Speedup:                   N/A")
        print()

        results.append(
            {
                "test": test_name,
                "iterative": iterative_time,
                "recursive": recursive_time,
                "speedup": speedup_factor,
                "faster": faster,
                "recursion_error": recursion_error,
            }
        )

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for result in results:
        if result["recursion_error"]:
            speedup_str = "N/A (recursion limit)"
        elif result["speedup"] == float("inf"):
            speedup_str = "N/A"
        else:
            speedup_str = f"{result['speedup']:.2f}x"
        print(f"{result['test']:30} | {result['faster']:10} | {speedup_str}")
    print()


if __name__ == "__main__":
    # Create disjoint sets for integers 1 through 5
    nodes = [make_set(i) for i in range(1, 6)]

    # Show initial sets: each node in its own set
    print("Initial representatives:")
    for i, node in enumerate(nodes):
        print(f"Node {node.value}: representative {find_set(node).value}")

    # Perform some unions
    print("\nUnion 1 and 2")
    union(nodes[0], nodes[1])  # union 1 and 2
    rep_1 = find_set(nodes[0]).value
    rep_2 = find_set(nodes[1]).value
    if rep_1 == rep_2:
        print(f"✅ Nodes 1 and 2 have same representative: {rep_1}")
    else:
        print(f"⚠️  Nodes 1 and 2 have different representatives: {rep_1} vs {rep_2}")

    print("\nUnion 3 and 4")
    union(nodes[2], nodes[3])  # union 3 and 4
    rep_3 = find_set(nodes[2]).value
    rep_4 = find_set(nodes[3]).value
    if rep_3 == rep_4:
        print(f"✅ Nodes 3 and 4 have same representative: {rep_3}")
    else:
        print(f"⚠️  Nodes 3 and 4 have different representatives: {rep_3} vs {rep_4}")

    print("\nUnion 2 and 3")
    union(nodes[1], nodes[2])  # union (1,2) with (3,4)
    reps = [find_set(node).value for node in nodes[:4]]
    if len(set(reps)) == 1:
        print(f"✅ Nodes 1, 2, 3, 4 all have same representative: {reps[0]}")
    else:
        print(f"⚠️  Nodes 1, 2, 3, 4 have different representatives: {reps}")

    # Find sets after some unions
    print("\nAfter unions:")
    for node in nodes:
        print(f"Node {node.value}: representative {find_set(node).value}")

    # Union remaining node 5 with representative of the other sets
    print("\nUnion 5 with 1")
    union(nodes[4], nodes[0])
    reps = [find_set(node).value for node in nodes]
    if len(set(reps)) == 1:
        print(f"✅ All nodes (1, 2, 3, 4, 5) have same representative: {reps[0]}")
    else:
        print(f"⚠️  Not all nodes have same representative: {reps}")

    print("\nFinal representatives:")
    for node in nodes:
        print(f"Node {node.value}: representative {find_set(node).value}")

    # Run benchmark
    print("\n" + "=" * 70)
    benchmark_find_set()
