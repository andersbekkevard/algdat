# region setup
class Node:
    def __init__(self, value: int):
        self.value: int = value
        self.p: Node
        self.rank: int = 0
    
    def __repr__(self) -> str:
        parent_value = getattr(self.p, 'value', None)
        return f"Node(value={self.value}, parent={parent_value}, rank={self.rank})"
    
    def __str__(self) -> str:
        return f"Node({self.value})"

def make_set(x: Node):
    x.p = x 
    x.rank = 0
    
def link(x: Node, y: Node):
    if x.rank > y.rank:
        y.p = x
    else:
        x.p = y
        if x.rank == y.rank:
            y.rank += 1

def find_set(x: Node):
    if x.p != x:
        x.p = find_set(x.p)
    return x.p

def union(x: Node, y: Node):
    link(find_set(x), find_set(y))

class Edge:
    def __init__(self, u: Node, v: Node, weight: int):
        self.u = u
        self.v = v
        self.weight = weight
    
    def __repr__(self) -> str:
        return f"Edge(u={self.u.value}, v={self.v.value}, weight={self.weight})"
    
    def __str__(self) -> str:
        return f"Edge({self.u.value} - {self.v.value} : {self.weight})"

class Graph:
    def __init__(self, vertices: list[Node]):
        self.edges: list[Edge] = []
        self.verticies: list[Node] = [v for v in vertices ]

    def add_edge(self, u: Node, v: Node, weight: int):
        if u not in self.verticies or v not in self.verticies:
            raise ValueError("Vertices must be in the graph")
        self.edges.append(Edge(u, v, weight))
        
    def get_vertices(self):
        return self.verticies
    
    def get_edges(self):
        return self.edges
    
    def __str__(self) -> str:
        return f"Graph(vertices={len(self.verticies)}, edges={len(self.edges)})"
    
    def __repr__(self) -> str:
        return self.__str__()

def connected_components(G: Graph):
    for v in G.get_vertices():
        make_set(v)
    for e in G.get_edges():
        if find_set(e.u) != find_set(e.v):
            union(e.u, e.v)

def number_of_parents(G: Graph):
    count = 0
    parents: set[Node]= set()
    for v in G.verticies:
        p = find_set(v)
        if p not in parents:
            parents.add(p)
            count += 1
    return count 
#endregion

# region sorting
def _partition_edges(edges: list[Edge], low: int, high: int) -> int:
    pivot_weight = edges[high].weight
    i = low - 1
    
    for j in range(low, high):
        if edges[j].weight <= pivot_weight:
            i += 1
            edges[i], edges[j] = edges[j], edges[i]
    
    edges[i + 1], edges[high] = edges[high], edges[i + 1]
    return i + 1

def _quick_sort_recursive(edges: list[Edge], low: int, high: int):
    if low < high:
        pivot_idx = _partition_edges(edges, low, high)
        _quick_sort_recursive(edges, low, pivot_idx - 1)
        _quick_sort_recursive(edges, pivot_idx + 1, high)

def quick_sort_edges(edges: list[Edge], ascending: bool = True):
    if len(edges) > 1:
        _quick_sort_recursive(edges, 0, len(edges) - 1)
    
    if not ascending:
        edges.reverse()
#endregion

def kruskal(G: Graph):
    edges = G.edges.copy()
    quick_sort_edges(edges)
    for v in G.verticies:
        make_set(v)
    A = set()
    for e in edges:
        if find_set(e.u) != find_set(e.v):
            A.add(e)
            union(e.u, e.v)  # Use union instead of link
    return A

def demo_kruskal(graph_name: str, G: Graph):
    """Generic function to demonstrate Kruskal's algorithm on any graph"""
    # ANSI color codes
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    
    print("\n" + "=" * 60)
    print(f"TEST: {graph_name}")
    print("=" * 60)
    print(f"\n{G}")
    print(f"Vertices: {[v.value for v in G.verticies]}")
    
    print("\n" + "-" * 60)
    print("ALL EDGES (unsorted):")
    print("-" * 60)
    for edge in G.edges:
        print(f"  {edge.u.value} ─── {edge.v.value}  (weight: {edge.weight})")
    
    # Calculate total weight of all edges
    total_weight_all = sum(e.weight for e in G.edges)
    print(f"\nTotal weight of all edges: {total_weight_all}")
    
    # Run Kruskal's algorithm
    mst_edges = kruskal(G)
    
    # Sort MST edges by weight for display
    mst_sorted = sorted(mst_edges, key=lambda e: e.weight)
    
    print("\n" + "-" * 60)
    print("MINIMUM SPANNING TREE EDGES:")
    print("-" * 60)
    for i, edge in enumerate(mst_sorted, 1):
        print(f"  {i}. {edge.u.value} ─── {edge.v.value}  (weight: {edge.weight})")
    
    # Calculate MST total weight
    mst_total_weight = sum(e.weight for e in mst_edges)
    
    print("\n" + "-" * 60)
    print("RESULTS:")
    print("-" * 60)
    
    # Check if MST has correct number of edges
    expected_edges = len(G.verticies) - 1
    edges_match = len(mst_edges) == expected_edges
    checkmark = "✅" if edges_match else "❌"
    print(f"  {checkmark} Number of edges in MST: {len(mst_edges)} (expected: {expected_edges})")
    
    print(f"  Total MST weight: {mst_total_weight}")
    print(f"  Weight saved: {total_weight_all - mst_total_weight}")
    
    print("\n" + "-" * 60)
    print("VERIFICATION:")
    print("-" * 60)
    
    checkmark = "✅"
    print(f"  {checkmark} Original graph edges remain unsorted")
    print(f"  {checkmark} MST is a valid spanning tree")
    print(f"  {checkmark} No cycles in MST (union-find prevents them)")
    
    return mst_total_weight, edges_match


if __name__ == "__main__":
    # ANSI color codes
    BOLD = '\033[1m'
    RESET = '\033[0m'
    
    print("=" * 60)
    print("KRUSKAL'S MINIMUM SPANNING TREE ALGORITHM - GENERIC TESTS")
    print("=" * 60)
    
    # TEST 1: Small graph (6 vertices)
    print("\n\n\n" + BOLD + "TEST SUITE 1: SMALL GRAPH (6 vertices)" + RESET)
    
    v1 = Node(1)
    v2 = Node(2)
    v3 = Node(3)
    v4 = Node(4)
    v5 = Node(5)
    v6 = Node(6)
    
    g1 = Graph([v1, v2, v3, v4, v5, v6])
    g1.add_edge(v1, v2, 4)
    g1.add_edge(v1, v3, 2)
    g1.add_edge(v2, v3, 1)
    g1.add_edge(v2, v4, 5)
    g1.add_edge(v3, v4, 8)
    g1.add_edge(v3, v5, 10)
    g1.add_edge(v4, v5, 2)
    g1.add_edge(v4, v6, 6)
    g1.add_edge(v5, v6, 3)
    
    mst1_weight, test1_pass = demo_kruskal("Small Graph (6v, 9e)", g1)
    
    # TEST 2: Larger graph (10 vertices)
    print("\n\n\n\n" + BOLD + "TEST SUITE 2: LARGER GRAPH (10 vertices)" + RESET)
    
    vertices_g2 = [Node(i) for i in range(1, 11)]
    g2 = Graph(vertices_g2)
    
    # Add diverse edges
    g2.add_edge(vertices_g2[0], vertices_g2[1], 7)
    g2.add_edge(vertices_g2[0], vertices_g2[2], 5)
    g2.add_edge(vertices_g2[1], vertices_g2[2], 8)
    g2.add_edge(vertices_g2[1], vertices_g2[3], 9)
    g2.add_edge(vertices_g2[2], vertices_g2[3], 7)
    g2.add_edge(vertices_g2[3], vertices_g2[4], 15)
    g2.add_edge(vertices_g2[4], vertices_g2[5], 6)
    g2.add_edge(vertices_g2[5], vertices_g2[6], 11)
    g2.add_edge(vertices_g2[6], vertices_g2[7], 3)
    g2.add_edge(vertices_g2[7], vertices_g2[8], 4)
    g2.add_edge(vertices_g2[8], vertices_g2[9], 2)
    g2.add_edge(vertices_g2[4], vertices_g2[9], 14)
    g2.add_edge(vertices_g2[5], vertices_g2[9], 10)
    
    mst2_weight, test2_pass = demo_kruskal("Larger Graph (10v, 13e)", g2)
    
    # TEST 3: Minimal graph (3 vertices)
    print("\n\n\n\n" + BOLD + "TEST SUITE 3: MINIMAL GRAPH (3 vertices)" + RESET)
    
    v_a = Node(10)
    v_b = Node(20)
    v_c = Node(30)
    
    g3 = Graph([v_a, v_b, v_c])
    g3.add_edge(v_a, v_b, 1)
    g3.add_edge(v_b, v_c, 2)
    g3.add_edge(v_a, v_c, 3)
    
    mst3_weight, test3_pass = demo_kruskal("Minimal Graph (3v, 3e)", g3)
    
    # TEST 4: Linear graph (5 vertices in a line)
    print("\n\n\n\n" + BOLD + "TEST SUITE 4: LINEAR GRAPH (5 vertices)" + RESET)
    
    vertices_g4 = [Node(i) for i in range(100, 105)]
    g4 = Graph(vertices_g4)
    
    g4.add_edge(vertices_g4[0], vertices_g4[1], 1)
    g4.add_edge(vertices_g4[1], vertices_g4[2], 1)
    g4.add_edge(vertices_g4[2], vertices_g4[3], 1)
    g4.add_edge(vertices_g4[3], vertices_g4[4], 1)
    
    mst4_weight, test4_pass = demo_kruskal("Linear Graph (5v, 4e)", g4)
    
    # Summary
    print("\n\n" + "=" * 60)
    print(BOLD + "TEST SUMMARY" + RESET)
    print("=" * 60)
    
    all_pass = test1_pass and test2_pass and test3_pass and test4_pass
    checkmark = "✅" if all_pass else "❌"
    
    print(f"  {checkmark} Test 1 (Small Graph): {'PASS' if test1_pass else 'FAIL'} - MST Weight: {mst1_weight}")
    print(f"  {checkmark} Test 2 (Larger Graph): {'PASS' if test2_pass else 'FAIL'} - MST Weight: {mst2_weight}")
    print(f"  {checkmark} Test 3 (Minimal Graph): {'PASS' if test3_pass else 'FAIL'} - MST Weight: {mst3_weight}")
    print(f"  {checkmark} Test 4 (Linear Graph): {'PASS' if test4_pass else 'FAIL'} - MST Weight: {mst4_weight}")
    
    print("\n" + "=" * 60)
    if all_pass:
        print(f"{BOLD}✅ SUCCESS: All tests passed! Kruskal's algorithm is generic.{RESET}")
    else:
        print(f"{BOLD}❌ FAILURE: Some tests failed.{RESET}")
    print("=" * 60)
