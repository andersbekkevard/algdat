"""
Tests for in-place APSP implementations.

We compare:
1. Original SLOW-APSP (with M matrix) vs In-place SLOW-APSP
2. Original FASTER-APSP (with M matrix) vs In-place FASTER-APSP
3. All versions against Floyd-Warshall (ground truth)
"""

import random
from apsp import (
    slow_apsp,
    slow_apsp_inplace,
    faster_apsp,
    faster_apsp_inplace,
    floyd_warshall,
    create_weight_matrix,
    matrices_equal,
    print_matrix,
    INF,
)


def test_textbook_example():
    """
    Test with the graph from Figure 23.1 in the textbook.
    5 vertices, various positive and negative edges.
    """
    print("=" * 60)
    print("TEST: Textbook Example (Figure 23.1)")
    print("=" * 60)

    # From Figure 23.1 in CLRS (0-indexed)
    # Original uses 1-indexed, we use 0-indexed
    n = 5
    edges = [
        (0, 1, 3), (0, 2, 8), (0, 4, -4),
        (1, 3, 1), (1, 4, 7),
        (2, 1, 4),
        (3, 0, 2), (3, 2, -5),
        (4, 3, 6),
    ]
    W = create_weight_matrix(edges, n)

    print("Weight Matrix W:")
    print_matrix(W, "W")

    # Compute with all methods
    fw = floyd_warshall(W, n)
    slow = slow_apsp(W, n)
    slow_ip = slow_apsp_inplace(W, n)
    fast = faster_apsp(W, n)
    fast_ip = faster_apsp_inplace(W, n)

    print_matrix(fw, "Floyd-Warshall (ground truth)")

    # Compare results
    results = []

    if matrices_equal(slow, fw, n):
        print("✅ SLOW-APSP matches Floyd-Warshall")
        results.append(True)
    else:
        print("❌ SLOW-APSP DIFFERS from Floyd-Warshall")
        print_matrix(slow, "SLOW-APSP")
        results.append(False)

    if matrices_equal(slow_ip, fw, n):
        print("✅ SLOW-APSP (in-place) matches Floyd-Warshall")
        results.append(True)
    else:
        print("❌ SLOW-APSP (in-place) DIFFERS from Floyd-Warshall")
        print_matrix(slow_ip, "SLOW-APSP (in-place)")
        results.append(False)

    if matrices_equal(fast, fw, n):
        print("✅ FASTER-APSP matches Floyd-Warshall")
        results.append(True)
    else:
        print("❌ FASTER-APSP DIFFERS from Floyd-Warshall")
        print_matrix(fast, "FASTER-APSP")
        results.append(False)

    if matrices_equal(fast_ip, fw, n):
        print("✅ FASTER-APSP (in-place) matches Floyd-Warshall")
        results.append(True)
    else:
        print("❌ FASTER-APSP (in-place) DIFFERS from Floyd-Warshall")
        print_matrix(fast_ip, "FASTER-APSP (in-place)")
        results.append(False)

    print()
    return all(results)


def test_simple_triangle():
    """Test with a simple triangle graph."""
    print("=" * 60)
    print("TEST: Simple Triangle")
    print("=" * 60)

    n = 3
    edges = [
        (0, 1, 1),
        (1, 2, 2),
        (0, 2, 10),  # Direct path is longer than via 1
    ]
    W = create_weight_matrix(edges, n)

    print_matrix(W, "W")

    fw = floyd_warshall(W, n)
    slow_ip = slow_apsp_inplace(W, n)
    fast_ip = faster_apsp_inplace(W, n)

    print_matrix(fw, "Floyd-Warshall")

    results = []

    if matrices_equal(slow_ip, fw, n):
        print("✅ SLOW-APSP (in-place) correct")
        results.append(True)
    else:
        print("❌ SLOW-APSP (in-place) INCORRECT")
        print_matrix(slow_ip, "SLOW-APSP (in-place)")
        results.append(False)

    if matrices_equal(fast_ip, fw, n):
        print("✅ FASTER-APSP (in-place) correct")
        results.append(True)
    else:
        print("❌ FASTER-APSP (in-place) INCORRECT")
        print_matrix(fast_ip, "FASTER-APSP (in-place)")
        results.append(False)

    print()
    return all(results)


def test_negative_edges():
    """Test with negative edges (but no negative cycles)."""
    print("=" * 60)
    print("TEST: Negative Edges")
    print("=" * 60)

    n = 4
    edges = [
        (0, 1, 2),
        (0, 2, 5),
        (1, 2, -3),  # Negative edge
        (1, 3, 1),
        (2, 3, 2),
    ]
    W = create_weight_matrix(edges, n)

    print_matrix(W, "W")

    fw = floyd_warshall(W, n)
    slow_ip = slow_apsp_inplace(W, n)
    fast_ip = faster_apsp_inplace(W, n)

    print_matrix(fw, "Floyd-Warshall")

    results = []

    if matrices_equal(slow_ip, fw, n):
        print("✅ SLOW-APSP (in-place) handles negative edges")
        results.append(True)
    else:
        print("❌ SLOW-APSP (in-place) FAILS with negative edges")
        print_matrix(slow_ip, "SLOW-APSP (in-place)")
        results.append(False)

    if matrices_equal(fast_ip, fw, n):
        print("✅ FASTER-APSP (in-place) handles negative edges")
        results.append(True)
    else:
        print("❌ FASTER-APSP (in-place) FAILS with negative edges")
        print_matrix(fast_ip, "FASTER-APSP (in-place)")
        results.append(False)

    print()
    return all(results)


def test_disconnected():
    """Test with disconnected vertices."""
    print("=" * 60)
    print("TEST: Disconnected Graph")
    print("=" * 60)

    n = 4
    edges = [
        (0, 1, 1),
        (2, 3, 1),
        # No edges between {0,1} and {2,3}
    ]
    W = create_weight_matrix(edges, n)

    print_matrix(W, "W")

    fw = floyd_warshall(W, n)
    slow_ip = slow_apsp_inplace(W, n)
    fast_ip = faster_apsp_inplace(W, n)

    print_matrix(fw, "Floyd-Warshall")

    results = []

    if matrices_equal(slow_ip, fw, n):
        print("✅ SLOW-APSP (in-place) handles disconnected graph")
        results.append(True)
    else:
        print("❌ SLOW-APSP (in-place) FAILS with disconnected graph")
        print_matrix(slow_ip, "SLOW-APSP (in-place)")
        results.append(False)

    if matrices_equal(fast_ip, fw, n):
        print("✅ FASTER-APSP (in-place) handles disconnected graph")
        results.append(True)
    else:
        print("❌ FASTER-APSP (in-place) FAILS with disconnected graph")
        print_matrix(fast_ip, "FASTER-APSP (in-place)")
        results.append(False)

    print()
    return all(results)


def test_complete_graph():
    """Test with a complete graph."""
    print("=" * 60)
    print("TEST: Complete Graph (n=5)")
    print("=" * 60)

    n = 5
    edges = []
    for i in range(n):
        for j in range(n):
            if i != j:
                # Weights that make indirect paths sometimes better
                edges.append((i, j, abs(i - j) * 3 + 1))

    W = create_weight_matrix(edges, n)

    fw = floyd_warshall(W, n)
    slow_ip = slow_apsp_inplace(W, n)
    fast_ip = faster_apsp_inplace(W, n)

    results = []

    if matrices_equal(slow_ip, fw, n):
        print("✅ SLOW-APSP (in-place) correct on complete graph")
        results.append(True)
    else:
        print("❌ SLOW-APSP (in-place) INCORRECT on complete graph")
        results.append(False)

    if matrices_equal(fast_ip, fw, n):
        print("✅ FASTER-APSP (in-place) correct on complete graph")
        results.append(True)
    else:
        print("❌ FASTER-APSP (in-place) INCORRECT on complete graph")
        results.append(False)

    print()
    return all(results)


def test_long_chain():
    """Test with a long chain where shortest paths have many edges."""
    print("=" * 60)
    print("TEST: Long Chain (n=10)")
    print("=" * 60)

    n = 10
    edges = []
    # Chain: 0 -> 1 -> 2 -> ... -> 9 with weight 1 each
    for i in range(n - 1):
        edges.append((i, i + 1, 1))
    # Also add a direct but expensive edge from 0 to 9
    edges.append((0, n - 1, 100))

    W = create_weight_matrix(edges, n)

    fw = floyd_warshall(W, n)
    slow_ip = slow_apsp_inplace(W, n)
    fast_ip = faster_apsp_inplace(W, n)

    # Check that 0->9 shortest path is 9, not 100
    print(f"Shortest path 0->{n-1}: {fw[0][n-1]} (should be {n-1})")

    results = []

    if matrices_equal(slow_ip, fw, n):
        print("✅ SLOW-APSP (in-place) correct on long chain")
        results.append(True)
    else:
        print("❌ SLOW-APSP (in-place) INCORRECT on long chain")
        print(f"  Got 0->{n-1}: {slow_ip[0][n-1]}, expected: {fw[0][n-1]}")
        results.append(False)

    if matrices_equal(fast_ip, fw, n):
        print("✅ FASTER-APSP (in-place) correct on long chain")
        results.append(True)
    else:
        print("❌ FASTER-APSP (in-place) INCORRECT on long chain")
        print(f"  Got 0->{n-1}: {fast_ip[0][n-1]}, expected: {fw[0][n-1]}")
        results.append(False)

    print()
    return all(results)


def test_random_graphs(num_tests: int = 10, max_n: int = 15):
    """Test on random graphs."""
    print("=" * 60)
    print(f"TEST: Random Graphs ({num_tests} tests, n up to {max_n})")
    print("=" * 60)

    all_passed = True

    for t in range(num_tests):
        n = random.randint(3, max_n)
        # Random number of edges
        num_edges = random.randint(n, n * (n - 1) // 2)

        edges = []
        edge_set = set()
        for _ in range(num_edges):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edge_set:
                # Mix of positive and some negative weights
                w = random.randint(-5, 20)
                edges.append((u, v, w))
                edge_set.add((u, v))

        W = create_weight_matrix(edges, n)

        # Check for negative cycles using Floyd-Warshall
        fw = floyd_warshall(W, n)
        has_neg_cycle = any(fw[i][i] < 0 for i in range(n))

        if has_neg_cycle:
            # Skip graphs with negative cycles
            continue

        slow_ip = slow_apsp_inplace(W, n)
        fast_ip = faster_apsp_inplace(W, n)

        slow_ok = matrices_equal(slow_ip, fw, n)
        fast_ok = matrices_equal(fast_ip, fw, n)

        if slow_ok and fast_ok:
            print(f"  Test {t+1}: n={n}, |E|={len(edges)} ✅")
        else:
            print(f"  Test {t+1}: n={n}, |E|={len(edges)} ❌")
            if not slow_ok:
                print("    SLOW-APSP (in-place) failed")
            if not fast_ok:
                print("    FASTER-APSP (in-place) failed")
            all_passed = False

    print()
    return all_passed


def test_single_vertex():
    """Edge case: single vertex."""
    print("=" * 60)
    print("TEST: Single Vertex")
    print("=" * 60)

    n = 1
    W = [[0]]

    fw = floyd_warshall(W, n)
    slow_ip = slow_apsp_inplace(W, n)
    fast_ip = faster_apsp_inplace(W, n)

    results = []

    if matrices_equal(slow_ip, fw, n):
        print("✅ SLOW-APSP (in-place) handles single vertex")
        results.append(True)
    else:
        print("❌ SLOW-APSP (in-place) FAILS on single vertex")
        results.append(False)

    if matrices_equal(fast_ip, fw, n):
        print("✅ FASTER-APSP (in-place) handles single vertex")
        results.append(True)
    else:
        print("❌ FASTER-APSP (in-place) FAILS on single vertex")
        results.append(False)

    print()
    return all(results)


def test_two_vertices():
    """Edge case: two vertices."""
    print("=" * 60)
    print("TEST: Two Vertices")
    print("=" * 60)

    n = 2
    edges = [(0, 1, 5), (1, 0, 3)]
    W = create_weight_matrix(edges, n)

    fw = floyd_warshall(W, n)
    slow_ip = slow_apsp_inplace(W, n)
    fast_ip = faster_apsp_inplace(W, n)

    print_matrix(fw, "Floyd-Warshall")

    results = []

    if matrices_equal(slow_ip, fw, n):
        print("✅ SLOW-APSP (in-place) handles two vertices")
        results.append(True)
    else:
        print("❌ SLOW-APSP (in-place) FAILS on two vertices")
        results.append(False)

    if matrices_equal(fast_ip, fw, n):
        print("✅ FASTER-APSP (in-place) handles two vertices")
        results.append(True)
    else:
        print("❌ FASTER-APSP (in-place) FAILS on two vertices")
        results.append(False)

    print()
    return all(results)


def run_all_tests():
    """Run all tests and summarize results."""
    print("\n" + "=" * 60)
    print("RUNNING ALL APSP IN-PLACE TESTS")
    print("=" * 60 + "\n")

    tests = [
        ("Textbook Example", test_textbook_example),
        ("Simple Triangle", test_simple_triangle),
        ("Negative Edges", test_negative_edges),
        ("Disconnected Graph", test_disconnected),
        ("Complete Graph", test_complete_graph),
        ("Long Chain", test_long_chain),
        ("Single Vertex", test_single_vertex),
        ("Two Vertices", test_two_vertices),
        ("Random Graphs", test_random_graphs),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"❌ {name} raised exception: {e}")
            results.append((name, False))

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("\nConclusion: In-place implementations are CORRECT.")
        print("The M matrix in SLOW-APSP and FASTER-APSP is NOT necessary.")
    else:
        print("❌ SOME TESTS FAILED!")
        print("\nSome in-place implementations may have issues.")

    return all_passed


if __name__ == "__main__":
    run_all_tests()
