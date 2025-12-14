"""
Attempt to find a counterexample where in-place FASTER-APSP gives incorrect results.

Based on professor's analysis:
- The INTERMEDIATE matrices will differ (L² in-place ≠ true L²)
- But the FINAL result should still be correct

Let's verify this with the professor's chain example and try to find a true counterexample.
"""

from apsp import INF, floyd_warshall, create_weight_matrix

Matrix = list[list[float]]


def extend_shortest_paths_with_copy(L: Matrix, W: Matrix, n: int) -> Matrix:
    """Original EXTEND-SHORTEST-PATHS that returns a NEW matrix (true matrix product)."""
    M = [[INF] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if L[i][k] + W[k][j] < M[i][j]:
                    M[i][j] = L[i][k] + W[k][j]
    return M


def extend_shortest_paths_inplace(L: Matrix, W: Matrix, n: int) -> None:
    """In-place version - modifies L directly."""
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if L[i][k] + W[k][j] < L[i][j]:
                    L[i][j] = L[i][k] + W[k][j]


def faster_apsp_with_trace(
    W: Matrix, n: int, inplace: bool
) -> tuple[Matrix, list[Matrix]]:
    """
    FASTER-APSP with trace of intermediate matrices.
    Returns (final_result, [intermediate_matrices])
    """
    L = [row[:] for row in W]
    intermediates = [[row[:] for row in L]]  # Store initial

    r = 1
    iteration = 0
    while r < n - 1:
        iteration += 1
        if inplace:
            extend_shortest_paths_inplace(L, L, n)
        else:
            L = extend_shortest_paths_with_copy(L, L, n)
        intermediates.append([row[:] for row in L])
        r = 2 * r

    return L, intermediates


def print_matrix(M: Matrix, name: str = "") -> None:
    """Pretty print a matrix."""
    n = len(M)
    if name:
        print(f"{name}:")
    for i in range(n):
        row_str = []
        for j in range(n):
            if M[i][j] == INF:
                row_str.append("  ∞")
            else:
                row_str.append(f"{M[i][j]:3.0f}")
        print("  [" + ", ".join(row_str) + "]")


def print_matrix_comparison(A: Matrix, B: Matrix, name_a: str, name_b: str) -> None:
    """Print two matrices side by side, highlighting differences."""
    n = len(A)
    print(f"\n{'─' * 30} vs {'─' * 30}")
    print(f"{name_a:^30} | {name_b:^30}")
    print(f"{'─' * 30} | {'─' * 30}")

    differences = []
    for i in range(n):
        row_a = []
        row_b = []
        for j in range(n):
            val_a = "∞" if A[i][j] == INF else f"{A[i][j]:.0f}"
            val_b = "∞" if B[i][j] == INF else f"{B[i][j]:.0f}"

            if A[i][j] != B[i][j]:
                row_a.append(f"[{val_a:>3}]")  # Bracket differences
                row_b.append(f"[{val_b:>3}]")
                diff_type = "LOWER" if B[i][j] < A[i][j] else "HIGHER"
                differences.append((i, j, A[i][j], B[i][j], diff_type))
            else:
                row_a.append(f" {val_a:>3} ")
                row_b.append(f" {val_b:>3} ")

        print(f"  {' '.join(row_a)} | {' '.join(row_b)}")

    if differences:
        print(f"\n⚠️  DIFFERENCES FOUND:")
        for i, j, va, vb, dtype in differences:
            va_str = "∞" if va == INF else f"{va:.0f}"
            vb_str = "∞" if vb == INF else f"{vb:.0f}"
            print(
                f"   [{i}][{j}]: {name_a}={va_str}, {name_b}={vb_str} ({dtype} in {name_b})"
            )
    else:
        print(f"\n✅ Matrices are IDENTICAL")

    return len(differences) > 0


def test_professors_chain_example():
    """
    Professor's example: chain 1→2→3→4 with weight 1, plus direct edge 1→4 with weight 10.

    With TRUE squaring (W²):
    - Can only use paths of ≤2 edges
    - l[0][3] should stay 10 (3-edge path 0→1→2→3 not allowed yet)

    With IN-PLACE:
    - Might compute l[0][2]=2 first, then use it to get l[0][3]=3
    - This is a 3-edge path, violating the "≤2 edges" invariant
    """
    print("=" * 70)
    print("PROFESSOR'S CHAIN EXAMPLE: 0→1→2→3 (weight 1) + direct 0→3 (weight 10)")
    print("=" * 70)

    n = 4
    edges = [
        (0, 1, 1),
        (1, 2, 1),
        (2, 3, 1),
        (0, 3, 10),  # Direct but expensive
    ]
    W = create_weight_matrix(edges, n)

    print("\nInitial W:")
    print_matrix(W)

    # Run both versions with traces
    true_result, true_trace = faster_apsp_with_trace(W, n, inplace=False)
    inplace_result, inplace_trace = faster_apsp_with_trace(W, n, inplace=True)

    # Ground truth
    fw = floyd_warshall(W, n)

    print(f"\nNumber of iterations: {len(true_trace) - 1}")

    # Compare intermediate matrices
    for i in range(1, len(true_trace)):
        print(f"\n{'=' * 70}")
        print(f"AFTER ITERATION {i} (computing L^{2**i}):")
        has_diff = print_matrix_comparison(
            true_trace[i], inplace_trace[i], f"True L^{2**i}", f"In-place 'L^{2**i}'"
        )

    # Compare final results
    print(f"\n{'=' * 70}")
    print("FINAL RESULTS vs GROUND TRUTH (Floyd-Warshall):")
    print("=" * 70)

    print("\nTrue FASTER-APSP vs Floyd-Warshall:")
    has_diff_true = print_matrix_comparison(
        true_result, fw, "True FASTER-APSP", "Floyd-Warshall"
    )

    print("\nIn-place FASTER-APSP vs Floyd-Warshall:")
    has_diff_inplace = print_matrix_comparison(
        inplace_result, fw, "In-place FASTER-APSP", "Floyd-Warshall"
    )

    if not has_diff_true and not has_diff_inplace:
        print("\n✅ Both versions produce CORRECT final results!")
        print("   The in-place version breaks the W^(2^k) invariant,")
        print("   but still converges to correct shortest paths.")


def test_longer_chain():
    """Test with a longer chain to see more iterations."""
    print("\n" + "=" * 70)
    print("LONGER CHAIN: 0→1→2→3→4→5→6→7 (all weight 1)")
    print("=" * 70)

    n = 8
    edges = [(i, i + 1, 1) for i in range(n - 1)]
    # Add expensive direct edge
    edges.append((0, n - 1, 100))
    W = create_weight_matrix(edges, n)

    true_result, true_trace = faster_apsp_with_trace(W, n, inplace=False)
    inplace_result, inplace_trace = faster_apsp_with_trace(W, n, inplace=True)
    fw = floyd_warshall(W, n)

    print(f"\nNumber of iterations: {len(true_trace) - 1}")
    print(f"Shortest path 0→{n-1} should be: {n-1}")

    # Show key entry [0][n-1] after each iteration
    print(f"\nL[0][{n-1}] after each iteration:")
    print(f"{'Iter':<6} {'True':>10} {'In-place':>10} {'Meaning':>30}")
    print("-" * 60)
    for i in range(len(true_trace)):
        true_val = true_trace[i][0][n - 1]
        inplace_val = inplace_trace[i][0][n - 1]
        true_str = "∞" if true_val == INF else f"{true_val:.0f}"
        inplace_str = "∞" if inplace_val == INF else f"{inplace_val:.0f}"
        if i == 0:
            meaning = "Initial (W)"
        else:
            meaning = f"paths ≤ {2**i} edges"
        print(f"{i:<6} {true_str:>10} {inplace_str:>10} {meaning:>30}")

    # Final comparison
    print(f"\n{'=' * 70}")
    print("FINAL COMPARISON:")
    print_matrix_comparison(true_result, fw, "True FASTER-APSP", "Floyd-Warshall")
    print_matrix_comparison(
        inplace_result, fw, "In-place FASTER-APSP", "Floyd-Warshall"
    )


def try_to_find_counterexample():
    """
    Systematically try to find a graph where in-place gives WRONG final answer.

    Hypothesis: This is impossible (without negative cycles) because:
    1. In-place only decreases values (relaxations)
    2. Values can't go below true shortest paths
    3. After enough iterations, we reach the fixpoint
    """
    print("\n" + "=" * 70)
    print("SEARCHING FOR COUNTEREXAMPLE (in-place gives wrong final answer)")
    print("=" * 70)

    import random

    random.seed(12345)

    found_counterexample = False
    tests_run = 0

    for _ in range(1000):
        n = random.randint(4, 12)
        num_edges = random.randint(n, n * (n - 1) // 2)

        edges = []
        edge_set = set()
        for _ in range(num_edges):
            u, v = random.randint(0, n - 1), random.randint(0, n - 1)
            if u != v and (u, v) not in edge_set:
                w = random.randint(1, 20)  # Positive weights only
                edges.append((u, v, w))
                edge_set.add((u, v))

        W = create_weight_matrix(edges, n)

        true_result, _ = faster_apsp_with_trace(W, n, inplace=False)
        inplace_result, _ = faster_apsp_with_trace(W, n, inplace=True)
        fw = floyd_warshall(W, n)

        tests_run += 1

        # Check if in-place gives wrong answer
        for i in range(n):
            for j in range(n):
                if inplace_result[i][j] != fw[i][j]:
                    print(f"\n❌ COUNTEREXAMPLE FOUND!")
                    print(f"   n={n}, edges={len(edges)}")
                    print(
                        f"   In-place[{i}][{j}]={inplace_result[i][j]}, correct={fw[i][j]}"
                    )
                    found_counterexample = True
                    break
            if found_counterexample:
                break
        if found_counterexample:
            break

    if not found_counterexample:
        print(f"\n✅ No counterexample found in {tests_run} random graphs!")
        print("   This supports the claim that in-place still converges correctly.")


def demonstrate_invariant_violation():
    """
    Show exactly how the invariant W^(2^k) is violated, even though final answer is correct.
    """
    print("\n" + "=" * 70)
    print("INVARIANT VIOLATION DEMONSTRATION")
    print("=" * 70)

    # Use professor's example
    n = 4
    edges = [
        (0, 1, 1),
        (1, 2, 1),
        (2, 3, 1),
        (0, 3, 10),
    ]
    W = create_weight_matrix(edges, n)

    print("\nAfter 1 iteration (should be W² = paths of ≤2 edges):")
    print("\nFor L[0][3]:")
    print("  - TRUE W²: Can only reach 0→3 via 2-edge paths")
    print("    - 0→1→3: needs edge 1→3 (doesn't exist) → ∞")
    print("    - 0→2→3: needs edge 0→2 (doesn't exist) → ∞")
    print("    - Direct 0→3: weight 10")
    print("    - Result: L[0][3] = 10")
    print()
    print("  - IN-PLACE: Order of computation matters!")
    print("    - First computes L[0][2] = L[0][1] + L[1][2] = 1 + 1 = 2")
    print("    - Then L[0][3] = min(10, L[0][2] + L[2][3]) = min(10, 2+1) = 3")
    print("    - Result: L[0][3] = 3 (a 3-edge path!)")
    print()
    print("  The in-place version 'cheats' by using the updated L[0][2]=2")
    print("  which represents a 2-edge path, to build a 3-edge path to L[0][3].")
    print()
    print("  This VIOLATES the invariant 'L = W^2 = paths of at most 2 edges'")
    print("  But it's still a VALID shortest path estimate (just computed early)!")


if __name__ == "__main__":
    test_professors_chain_example()
    test_longer_chain()
    demonstrate_invariant_violation()
    try_to_find_counterexample()

    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print(
        """
Your professor is correct:

1. INTERMEDIATE MATRICES DIFFER: In-place doesn't compute true W^(2^k)
   - It "leaks" information from longer paths into earlier iterations
   - The invariant "L = W^r after iteration log(r)" is BROKEN

2. FINAL RESULT IS STILL CORRECT: Despite breaking the invariant,
   in-place converges to the same final shortest paths because:
   - Each update is a valid relaxation (can't go below true shortest path)
   - We do ≥ the minimum required number of relaxation "opportunities"
   - The in-place version might even converge FASTER

3. WHAT'S LOST: The clean O(n³ log n) analysis that relies on
   "after k iterations, we have exactly W^(2^k)"

The M matrix isn't needed for CORRECTNESS, but it IS needed for
the THEORETICAL ANALYSIS of why O(log n) iterations suffice.
"""
    )
