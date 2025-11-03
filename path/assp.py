INF = float("inf")


def extend_shortest_paths(L, W, L_new):
    n = len(L)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                L_new[i][j] = min(L_new[i][j], L[i][k] + W[k][j])
    return L_new


def slow_assp(W):
    n = len(W)
    L = [[0 if i == j else INF for i in range(n)] for j in range(n)]
    for _ in range(n - 1):
        M = [[INF for _ in range(n)] for _ in range(n)]
        extend_shortest_paths(L, W, M)
        L = M
    return L


def faster_assp(W):
    n = len(W)
    L = W
    r = 1
    while r < n - 1:
        M = [[INF for _ in range(n)] for _ in range(n)]
        extend_shortest_paths(L, L, M)
        r *= 2
        L = M
    return L


def visualize_graph(W, shortest_paths=None):
    """
    Visualize a weighted graph from adjacency matrix W.

    Args:
        W: Adjacency matrix (weight matrix) of the graph
        shortest_paths: Optional matrix of shortest path distances to display
    """
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
        from matplotlib.gridspec import GridSpec
    except ImportError:
        print("Visualization requires networkx and matplotlib.")
        print("Install with: pip install networkx matplotlib")
        return

    n = len(W)
    G = nx.DiGraph()  # Use directed graph for adjacency matrix representation

    # Add nodes
    G.add_nodes_from(range(n))

    # Add edges with weights
    for i in range(n):
        for j in range(n):
            if i != j and W[i][j] != INF:
                G.add_edge(i, j, weight=W[i][j])

    # Create figure with subplots
    if shortest_paths is not None:
        fig = plt.figure(figsize=(18, 8))
        gs = GridSpec(1, 2, figure=fig, width_ratios=[1.2, 0.8])
        ax_graph = fig.add_subplot(gs[0])
        ax_table = fig.add_subplot(gs[1])
    else:
        fig, ax_graph = plt.subplots(figsize=(12, 8))
        ax_table = None

    # Use spring layout for nice positioning
    pos = nx.spring_layout(G, seed=42)

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos, ax=ax_graph, node_color="lightblue", node_size=1500, alpha=0.9
    )

    # Draw node labels
    nx.draw_networkx_labels(G, pos, ax=ax_graph, font_size=16, font_weight="bold")

    # Draw edges with better visibility for direction
    # Use curved edges to make direction clearer
    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax_graph,
        edge_color="darkblue",
        width=2.5,
        alpha=0.8,
        arrows=True,
        arrowsize=25,
        arrowstyle="->",
        connectionstyle="arc3,rad=0.1",  # Curved edges make direction clearer
        min_source_margin=15,
        min_target_margin=15,  # Add space around nodes for clearer arrows
    )

    # Draw edge labels (weights) with better visibility
    edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        ax=ax_graph,
        font_size=11,
        font_color="darkred",
        font_weight="bold",
        bbox=dict(
            boxstyle="round,pad=0.3", facecolor="white", edgecolor="none", alpha=0.8
        ),
    )

    # Add title
    title = "Graph Visualization"
    if shortest_paths is not None:
        title += " (with Shortest Path Distances)"
    ax_graph.set_title(title, fontsize=18, fontweight="bold", pad=20)

    ax_graph.axis("off")

    # Display shortest paths table if provided
    if shortest_paths is not None and ax_table is not None:
        # Prepare table data
        table_data = []
        headers = [f"To {j}" for j in range(n)]
        row_labels = [f"From {i}" for i in range(n)]

        for i in range(n):
            row = []
            for j in range(n):
                if shortest_paths[i][j] == INF:
                    row.append("∞")
                else:
                    # Format as integer if whole number, otherwise decimal
                    val = shortest_paths[i][j]
                    if val == int(val):
                        row.append(str(int(val)))
                    else:
                        row.append(f"{val:.1f}")
            table_data.append(row)

        # Create table with header row
        table = ax_table.table(
            cellText=table_data,
            rowLabels=row_labels,
            colLabels=headers,
            cellLoc="center",
            loc="center",
        )

        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 2)

        # Style header row - subtle gray, same height as data cells
        for i in range(len(headers)):
            cell = table[(0, i)]
            cell.set_facecolor("#E8E8E8")
            cell.set_text_props(weight="bold")
            # Don't set custom height - let it match data cells

        # Style row labels
        for i in range(len(row_labels)):
            cell = table[(i + 1, -1)]
            cell.set_facecolor("#E8E8E8")
            cell.set_text_props(weight="bold")
            cell.set_width(0.2)

        # Style data cells - alternate row colors
        for i in range(len(table_data)):
            for j in range(len(table_data[0])):
                cell = table[(i + 1, j)]
                if i % 2 == 0:
                    cell.set_facecolor("#F5F5F5")
                else:
                    cell.set_facecolor("#FFFFFF")
                # Highlight diagonal (self-distances)
                if i == j:
                    cell.set_facecolor("#FFE6E6")

        # Hide axes for table
        ax_table.axis("off")
        ax_table.set_title(
            "Shortest Path Distances\n(All Pairs)",
            fontsize=16,
            fontweight="bold",
            pad=20,
        )

    plt.tight_layout()
    plt.show()

    # Print shortest paths if provided (for console output)
    if shortest_paths is not None:
        print("\nShortest Path Distances Matrix:")
        print("=" * 50)
        print(f"{'From\\To':<8}", end="")
        for j in range(n):
            print(f"{j:>8}", end="")
        print()
        print("-" * 50)
        for i in range(n):
            print(f"{i:<8}", end="")
            for j in range(n):
                if shortest_paths[i][j] == INF:
                    print(f"{'INF':>8}", end="")
                else:
                    print(f"{shortest_paths[i][j]:>8.1f}", end="")
            print()
        print("=" * 50)

    return G


def example():
    """
    Boilerplate example demonstrating the All-Pairs Shortest Paths algorithm.
    """
    # Example: Weighted directed graph with 4 nodes
    # Adjacency matrix representation
    # INF represents no direct edge between nodes
    W = [
        [0, 3, 8, INF, -4],  # Node 0
        [INF, 0, INF, 1, 7],  # Node 1
        [INF, 4, 0, INF, INF],  # Node 2
        [2, INF, -5, 0, INF],  # Node 3
        [INF, INF, INF, 6, 0],  # Node 4
    ]

    print("=" * 60)
    print("All-Pairs Shortest Paths (APSP) - Boilerplate Example")
    print("=" * 60)
    print("\nInput Graph (Adjacency Matrix W):")
    print("-" * 60)
    n = len(W)
    print(f"{'From\\To':<8}", end="")
    for j in range(n):
        print(f"{j:>8}", end="")
    print()
    print("-" * 60)
    for i in range(n):
        print(f"{i:<8}", end="")
        for j in range(n):
            if W[i][j] == INF:
                print(f"{'INF':>8}", end="")
            else:
                print(f"{W[i][j]:>8.1f}", end="")
        print()
    print("-" * 60)

    # Compute shortest paths
    print("\nComputing shortest paths between all pairs...")
    shortest_paths = slow_assp(W)

    # Visualize the graph
    print("\nVisualizing graph...")
    visualize_graph(W, shortest_paths)

    return shortest_paths


if __name__ == "__main__":
    example()
    W = [
        [0, 3, 8],  # Node 0: edge to 1 (weight 3), edge to 2 (weight 8)
        [INF, 0, 1],  # Node 1: edge to 2 (weight 1)
        [INF, INF, 0],  # Node 2: no outgoing edges
    ]
    shortest_paths = faster_assp(W)
    visualize_graph(W, shortest_paths)
