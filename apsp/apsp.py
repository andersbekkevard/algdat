"""
All-Pairs Shortest Paths implementations.

This module contains:
1. Original SLOW-APSP and FASTER-APSP with separate M matrix
2. In-place versions without the M matrix
3. Floyd-Warshall for comparison

=============================================================================
WHY IN-PLACE WORKS (removing the M matrix)
=============================================================================

The textbook uses a separate matrix M to avoid "mixing" L(r-1) and L(r) values
during the matrix product L(r) = L(r-1) · W. But this is UNNECESSARY.

Key insight (similar to Floyd-Warshall's correctness):

1. MONOTONICITY: L(r)[i,j] <= L(r-1)[i,j] for all i,j
   - Adding more allowed edges can only make paths shorter or equal
   - We never increase shortest path estimates

2. RELAXATION VALIDITY: Every update L[i,j] = min(L[i,j], L[i,k] + W[k,j])
   is a valid path relaxation
   - If L[i,k] represents a valid path weight, then L[i,k] + W[k,j] is too
   - Using a "newer" (smaller) L[i,k] value just finds a valid shorter path

3. CONVERGENCE: Since shortest paths are simple (no negative cycles),
   they have at most n-1 edges
   - After n-1 iterations, we reach the fixpoint regardless of update order
   - In-place might converge faster (fewer iterations needed), never slower

The analogy to Floyd-Warshall is exact:
- In FW, d[i][k] and d[k][j] might already be updated when computing d[i][j]
- This doesn't matter because those values are still valid path weights
- The same reasoning applies to EXTEND-SHORTEST-PATHS

Exercise 23.1-6 in CLRS hints at this: "Relate line 5 of EXTEND-SHORTEST-PATHS
to RELAX" - the RELAX operation is order-independent for convergence.
=============================================================================
"""

import math
from typing import List

INF = float('inf')
Matrix = List[List[float]]


def extend_shortest_paths(L: Matrix, W: Matrix, M: Matrix, n: int) -> None:
    """
    Original EXTEND-SHORTEST-PATHS from the textbook.
    Computes M = L · W (matrix "product" for shortest paths).
    M should be initialized to INF before calling.
    """
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if L[i][k] + W[k][j] < M[i][j]:
                    M[i][j] = L[i][k] + W[k][j]


def extend_shortest_paths_inplace(L: Matrix, W: Matrix, n: int) -> None:
    """
    In-place version of EXTEND-SHORTEST-PATHS.
    Computes L := L · W without using a separate output matrix.

    Correctness argument:
    - When we update L[i][j], we may read L[i][k] values that were already updated
    - But L(r)[i][k] <= L(r-1)[i][k], so we get a valid (possibly shorter) path
    - This might cause faster convergence but never incorrect results
    """
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if L[i][k] + W[k][j] < L[i][j]:
                    L[i][j] = L[i][k] + W[k][j]


def slow_apsp(W: Matrix, n: int) -> Matrix:
    """
    Original SLOW-APSP from the textbook.
    Uses separate L and M matrices.
    Time: O(n^4), Space: O(n^2) for the extra M matrix.
    """
    # Initialize L = L(0) = identity for shortest paths
    L = [[INF] * n for _ in range(n)]
    for i in range(n):
        L[i][i] = 0

    # First multiplication: L(1) = L(0) · W = W
    # Actually, we start with L = W conceptually for r=1
    # Let's follow the textbook more closely:
    # L(0) has 0 on diagonal, inf elsewhere
    # L(1) = L(0) · W

    # Actually looking at the textbook again:
    # L(0) is the identity (0 on diagonal, inf elsewhere)
    # We compute L(1), L(2), ..., L(n-1)
    # L(r) = L(r-1) · W

    for r in range(1, n):
        M = [[INF] * n for _ in range(n)]
        extend_shortest_paths(L, W, M, n)
        L = M

    return L


def slow_apsp_inplace(W: Matrix, n: int) -> Matrix:
    """
    In-place SLOW-APSP without the M matrix.
    Directly updates L in place.
    """
    # Start with L = W (which is L(1) essentially)
    # But to be consistent, start with L(0)
    L = [[INF] * n for _ in range(n)]
    for i in range(n):
        L[i][i] = 0

    for r in range(1, n):
        extend_shortest_paths_inplace(L, W, n)

    return L


def faster_apsp(W: Matrix, n: int) -> Matrix:
    """
    Original FASTER-APSP with repeated squaring.
    Uses separate L and M matrices.
    Time: O(n^3 log n), Space: O(n^2) for the extra M matrix.
    """
    # L = W initially
    L = [row[:] for row in W]  # Deep copy

    r = 1
    while r < n - 1:
        M = [[INF] * n for _ in range(n)]
        extend_shortest_paths(L, L, M, n)  # M = L^2
        r = 2 * r
        L = M

    return L


def faster_apsp_inplace(W: Matrix, n: int) -> Matrix:
    """
    In-place FASTER-APSP with repeated squaring.
    No separate M matrix - updates L directly.

    IMPORTANT: This is trickier than SLOW-APSP because we're computing L := L · L
    When we update L[i][j], we read L[i][k] and L[k][j], which might have been updated.

    The question: Does this still converge to correct shortest paths?

    Argument for correctness:
    - Each update L[i][j] = min(L[i][j], L[i][k] + L[k][j]) is a valid relaxation
    - We never overestimate (only improve or stay same)
    - After enough iterations, we reach the fixpoint (true shortest paths)
    """
    L = [row[:] for row in W]  # Deep copy

    r = 1
    while r < n - 1:
        extend_shortest_paths_inplace(L, L, n)  # L := L · L
        r = 2 * r

    return L


def floyd_warshall(W: Matrix, n: int) -> Matrix:
    """
    Floyd-Warshall algorithm (ground truth for comparison).
    In-place updates are provably correct here.
    Time: O(n^3), Space: O(n^2).
    """
    D = [row[:] for row in W]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if D[i][k] + D[k][j] < D[i][j]:
                    D[i][j] = D[i][k] + D[k][j]

    return D


def create_weight_matrix(edges: List[tuple], n: int) -> Matrix:
    """
    Create weight matrix W from edge list.
    edges: list of (u, v, weight) tuples (0-indexed vertices)
    """
    W = [[INF] * n for _ in range(n)]
    for i in range(n):
        W[i][i] = 0
    for u, v, w in edges:
        W[u][v] = w
    return W


def matrices_equal(A: Matrix, B: Matrix, n: int) -> bool:
    """Check if two matrices are equal."""
    for i in range(n):
        for j in range(n):
            if A[i][j] != B[i][j]:
                # Handle inf comparison
                if not (A[i][j] == INF and B[i][j] == INF):
                    return False
    return True


def print_matrix(M: Matrix, name: str = "Matrix") -> None:
    """Pretty print a matrix."""
    n = len(M)
    print(f"{name}:")
    for i in range(n):
        row_str = []
        for j in range(n):
            if M[i][j] == INF:
                row_str.append("  ∞")
            else:
                row_str.append(f"{M[i][j]:3.0f}")
        print("  [" + ", ".join(row_str) + "]")
    print()
