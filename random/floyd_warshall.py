def floyd_warshall(G):
    n = len(G)
    INF = 1e9
    PI_old: list[list[int | None]] = [[None] * n for _ in range(n)]
    PI_new: list[list[int | None]] = [[None] * n for _ in range(n)]
    D_old = [[INF] * n for _ in range(n)]
    D_new = [[INF] * n for _ in range(n)]

    # Initialize: distances from graph, diagonal to 0, predecessors
    for i in range(n):
        D_old[i][i] = 0
        for j in range(n):
            if G[i][j] is not None and G[i][j] != INF:
                D_old[i][j] = G[i][j]
                PI_old[i][j] = i

    for k in range(n):
        for i in range(n):
            for j in range(n):
                direct = D_old[i][j]
                via_k = D_old[i][k] + D_old[k][j]
                D_new[i][j] = min(direct, via_k)
                PI_new[i][j] = PI_old[k][j] if via_k < direct else PI_old[i][j]
        PI_old, PI_new = PI_new, PI_old
        D_old, D_new = D_new, D_old

    return D_old, PI_old


def has_negative_cycle(D):
    """Check if graph has negative cycle: any diagonal element < 0."""
    for i in range(len(D)):
        if D[i][i] < 0:
            return True, i
    return False, None


def reconstruct_path(PI, D, i, j):
    """Reconstruct shortest path from i to j using predecessor matrix."""
    # Check if path exists (distance is finite)
    dist = D[i][j]
    if dist >= 1e9 or dist == float("inf"):
        return []  # No path exists
    if i == j:
        return [i]  # Self-loop
    if PI[i][j] is None:
        return []  # No path exists

    path = []
    curr = j
    while curr != i:
        path.append(curr)
        if PI[i][curr] is None:
            return []  # No path exists
        curr = PI[i][curr]
    path.append(i)
    return path[::-1]


if __name__ == "__main__":
    # Example graph: 4 nodes
    #   0 --3--> 1
    #   |        |
    #   8        1
    #   v        v
    #   2 --2--> 3
    #   ^        |
    #   |--------5

    INF = float("inf")
    G = [
        [0, 3, 8, INF],  # 0 -> 1: 3, 0 -> 2: 8
        [INF, 0, INF, 1],  # 1 -> 3: 1
        [INF, INF, 0, 2],  # 2 -> 3: 2
        [INF, INF, 5, 0],  # 3 -> 2: 5
    ]

    print("Graph (adjacency matrix):")
    for i, row in enumerate(G):
        print(f"  {i}: {[x if x != INF else 'INF' for x in row]}")

    D, PI = floyd_warshall(G)

    print("\nShortest distances:")
    n = len(D)
    print("   ", end="")
    for j in range(n):
        print(f"{j:>6}", end="")
    print()
    for i in range(n):
        print(f"{i}: ", end="")
        for j in range(n):
            if D[i][j] == 1e9:
                print("   INF", end="")
            else:
                print(f"{D[i][j]:>6.1f}", end="")
        print()

    print("\nExample paths:")
    for start, end in [(0, 3), (1, 2), (2, 1)]:
        path = reconstruct_path(PI, D, start, end)
        if path:
            path_str = " -> ".join(map(str, path))
            print(f"  {start} -> {end}: {path_str} (distance: {D[start][end]:.1f})")
        else:
            print(f"  {start} -> {end}: No path")

    # Negative cycle demonstration
    print("\n" + "=" * 60)
    print("NEGATIVE CYCLE DEMONSTRATION")
    print("=" * 60)

    # Graph with negative cycle: 0 -> 1 -> 2 -> 0 (cycle weight: 1 + 2 - 4 = -1)
    #   0 --1--> 1
    #   ^        |
    #   |        2
    #   |        v
    #   --(-4)-- 2
    INF = float("inf")
    G_neg = [
        [0, 1, INF],  # 0 -> 1: 1
        [INF, 0, 2],  # 1 -> 2: 2
        [-4, INF, 0],  # 2 -> 0: -4 (negative edge creates cycle)
    ]

    print("\nGraph with negative cycle (adjacency matrix):")
    for i, row in enumerate(G_neg):
        print(f"  {i}: {[x if x != INF else 'INF' for x in row]}")

    D_neg, PI_neg = floyd_warshall(G_neg)

    print("\nShortest distances (after Floyd-Warshall):")
    n_neg = len(D_neg)
    print("   ", end="")
    for j in range(n_neg):
        print(f"{j:>8}", end="")
    print()
    for i in range(n_neg):
        print(f"{i}: ", end="")
        for j in range(n_neg):
            if D_neg[i][j] >= 1e9:
                print("     INF", end="")
            else:
                print(f"{D_neg[i][j]:>8.1f}", end="")
        print()

    has_cycle, cycle_node = has_negative_cycle(D_neg)
    if has_cycle and cycle_node is not None:
        print(f"\n⚠️  NEGATIVE CYCLE DETECTED!")
        print(
            f"   Node {cycle_node} has negative self-distance: {D_neg[cycle_node][cycle_node]:.1f}"
        )
        print(
            "   This means there's a cycle through this node with negative total weight."
        )
        print(
            "   Shortest paths are undefined (can be made arbitrarily short by looping)."
        )
    else:
        print("\n✓ No negative cycles detected.")
