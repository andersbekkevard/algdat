INF = float("inf")


def transitive_closure(W):
    n = len(W)
    T = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(n + 1)]
    T[0] = [[1 if W[i][j] or i == j else 0 for j in range(n)] for i in range(n)]
    for k in range(1, n + 1):
        for i in range(n):
            for j in range(n):
                T[k][i][j] = T[k - 1][i][j] or (
                    T[k - 1][i][k - 1] and T[k - 1][k - 1][j]
                )
    return T[n]


def simple_transitive_closure(W):
    n = len(W)
    T = [[1 if (i == j or W[i][j] != INF) else 0 for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                T[i][j] = T[i][j] or (T[i][k] and T[k][j])
    return T


def plot_transitive_closure(W, T, title="Transitive Closure"):
    """Plot the original graph and its transitive closure side by side."""
    import matplotlib.pyplot as plt
    import networkx as nx

    # Create graphs
    G_original = nx.DiGraph()
    G_closure = nx.DiGraph()

    n = len(W)
    # Track original edges
    original_edges = set()
    for i in range(n):
        for j in range(n):
            if W[i][j]:
                G_original.add_edge(i, j)
                original_edges.add((i, j))
            if T[i][j] and i != j:  # Don't show self-loops in visualization
                G_closure.add_edge(i, j)

    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Original graph
    pos = nx.spring_layout(G_original, seed=42)
    nx.draw(
        G_original,
        pos,
        ax=ax1,
        with_labels=True,
        node_color="lightblue",
        node_size=1000,
        font_size=16,
        font_weight="bold",
        arrows=True,
        edge_color="black",
    )
    ax1.set_title("Original Graph", fontsize=16, fontweight="bold")

    # Transitive closure graph with different colors for original vs transitively added edges
    # Create edge color mapping
    edge_color_map = {}
    for edge in G_closure.edges():
        if edge in original_edges:
            edge_color_map[edge] = "black"  # Original edges in black
        else:
            edge_color_map[edge] = "red"  # Transitively added edges in red

    # Get edges in the order NetworkX will draw them
    edges_list = list(G_closure.edges())
    edge_colors = [edge_color_map[edge] for edge in edges_list]

    nx.draw(
        G_closure,
        pos,
        ax=ax2,
        with_labels=True,
        node_color="lightgreen",
        node_size=1000,
        font_size=16,
        font_weight="bold",
        arrows=True,
        edge_color=edge_colors,
    )
    ax2.set_title("Transitive Closure", fontsize=16, fontweight="bold")

    # Add legend to explain the colors
    from matplotlib.patches import Patch

    legend_elements = [
        Patch(facecolor="black", label="Original edges"),
        Patch(facecolor="red", label="Transitively added edges"),
    ]
    ax2.legend(handles=legend_elements, loc="upper right")

    plt.suptitle(title, fontsize=18, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.show()


def demo(number_of_examples=12):
    import numpy as np

    # Define multiple example graphs
    examples = [
        {
            "name": "Example 1: Simple Chain",
            "description": "0 -> 1 -> 2 -> 3, and 0 -> 3",
            "W": [
                [0, 1, 0, 1],  # 0 -> 1, 0 -> 3
                [0, 0, 1, 0],  # 1 -> 2
                [0, 0, 0, 1],  # 2 -> 3
                [0, 0, 0, 0],  # 3 has no outgoing edges
            ],
        },
        {
            "name": "Example 2: Cycle",
            "description": "0 -> 1 -> 2 -> 0 (cycle)",
            "W": [
                [0, 1, 0],  # 0 -> 1
                [0, 0, 1],  # 1 -> 2
                [1, 0, 0],  # 2 -> 0
            ],
        },
        {
            "name": "Example 3: Disconnected Components",
            "description": "Two separate chains: 0 -> 1 and 2 -> 3",
            "W": [
                [0, 1, 0, 0],  # 0 -> 1
                [0, 0, 0, 0],  # 1 isolated
                [0, 0, 0, 1],  # 2 -> 3
                [0, 0, 0, 0],  # 3 isolated
            ],
        },
        {
            "name": "Example 4: Diamond Shape",
            "description": "0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3",
            "W": [
                [0, 1, 1, 0],  # 0 -> 1, 0 -> 2
                [0, 0, 0, 1],  # 1 -> 3
                [0, 0, 0, 1],  # 2 -> 3
                [0, 0, 0, 0],  # 3 sink
            ],
        },
        {
            "name": "Example 5: Complete Acyclic",
            "description": "All paths forward: 0 -> 1,2,3; 1 -> 2,3; 2 -> 3",
            "W": [
                [0, 1, 1, 1],  # 0 -> 1,2,3
                [0, 0, 1, 1],  # 1 -> 2,3
                [0, 0, 0, 1],  # 2 -> 3
                [0, 0, 0, 0],  # 3 sink
            ],
        },
        {
            "name": "Example 6: Multi-Level Hierarchy",
            "description": "5-level hierarchy: 0 -> 1,2 -> 3,4 -> 5,6 -> 7",
            "W": [
                [0, 1, 1, 0, 0, 0, 0, 0],  # 0 -> 1,2
                [0, 0, 0, 1, 1, 0, 0, 0],  # 1 -> 3,4
                [0, 0, 0, 1, 1, 0, 0, 0],  # 2 -> 3,4
                [0, 0, 0, 0, 0, 1, 1, 0],  # 3 -> 5,6
                [0, 0, 0, 0, 0, 1, 1, 0],  # 4 -> 5,6
                [0, 0, 0, 0, 0, 0, 0, 1],  # 5 -> 7
                [0, 0, 0, 0, 0, 0, 0, 1],  # 6 -> 7
                [0, 0, 0, 0, 0, 0, 0, 0],  # 7 sink
            ],
        },
        {
            "name": "Example 7: Strongly Connected Component",
            "description": "SCC (0,1,2) with connections to external nodes",
            "W": [
                [0, 1, 0, 1, 0],  # 0 -> 1, 0 -> 3
                [0, 0, 1, 0, 0],  # 1 -> 2
                [1, 0, 0, 0, 1],  # 2 -> 0, 2 -> 4
                [0, 0, 0, 0, 1],  # 3 -> 4
                [0, 0, 0, 0, 0],  # 4 sink
            ],
        },
        {
            "name": "Example 8: Multiple Cycles",
            "description": "Two cycles (0-1-2) and (3-4-5) connected via 2->3",
            "W": [
                [0, 1, 0, 0, 0, 0],  # 0 -> 1
                [0, 0, 1, 0, 0, 0],  # 1 -> 2
                [1, 0, 0, 1, 0, 0],  # 2 -> 0, 2 -> 3
                [0, 0, 0, 0, 1, 0],  # 3 -> 4
                [0, 0, 0, 0, 0, 1],  # 4 -> 5
                [1, 0, 0, 1, 0, 0],  # 5 -> 0, 5 -> 3
            ],
        },
        {
            "name": "Example 9: Complex DAG with Cross-Edges",
            "description": "Layered graph with cross-layer connections",
            "W": [
                [0, 1, 1, 0, 0, 0, 0, 0],  # 0 -> 1,2
                [0, 0, 0, 1, 1, 0, 0, 0],  # 1 -> 3,4
                [0, 0, 0, 0, 1, 1, 0, 0],  # 2 -> 4,5
                [0, 0, 0, 0, 0, 0, 1, 1],  # 3 -> 6,7
                [0, 0, 0, 0, 0, 0, 1, 1],  # 4 -> 6,7
                [0, 0, 0, 0, 0, 0, 0, 1],  # 5 -> 7
                [0, 0, 0, 0, 0, 0, 0, 0],  # 6 sink
                [0, 0, 0, 0, 0, 0, 0, 0],  # 7 sink
            ],
        },
        {
            "name": "Example 10: Fork-Join Pattern",
            "description": "Fork from 0, converge at 4, then fork again",
            "W": [
                [0, 1, 1, 1, 0, 0, 0, 0],  # 0 -> 1,2,3
                [0, 0, 0, 0, 1, 0, 0, 0],  # 1 -> 4
                [0, 0, 0, 0, 1, 0, 0, 0],  # 2 -> 4
                [0, 0, 0, 0, 1, 0, 0, 0],  # 3 -> 4
                [0, 0, 0, 0, 0, 1, 1, 1],  # 4 -> 5,6,7
                [0, 0, 0, 0, 0, 0, 0, 0],  # 5 sink
                [0, 0, 0, 0, 0, 0, 0, 0],  # 6 sink
                [0, 0, 0, 0, 0, 0, 0, 0],  # 7 sink
            ],
        },
        {
            "name": "Example 11: Mixed Structure",
            "description": "Combination of cycles, chains, and branches",
            "W": [
                [0, 1, 0, 0, 0, 0, 0],  # 0 -> 1
                [0, 0, 1, 1, 0, 0, 0],  # 1 -> 2,3
                [1, 0, 0, 0, 1, 0, 0],  # 2 -> 0, 2 -> 4
                [0, 0, 0, 0, 1, 0, 0],  # 3 -> 4
                [0, 0, 0, 0, 0, 1, 1],  # 4 -> 5,6
                [0, 0, 0, 0, 0, 0, 0],  # 5 sink
                [0, 0, 0, 0, 0, 0, 0],  # 6 sink
            ],
        },
        {
            "name": "Example 12: Large Sparse Graph",
            "description": "10-node graph with sparse connections",
            "W": [
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 0 -> 1
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # 1 -> 2
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # 2 -> 3
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],  # 3 -> 4,5
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],  # 4 -> 6
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # 5 -> 7
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # 6 -> 8
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 7 -> 9
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 8 -> 9
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 9 sink
            ],
        },
    ]

    for idx, example in enumerate(examples[:number_of_examples], 1):
        print("=" * 60)
        print(f"{example['name']}")
        print(f"{example['description']}")
        print("=" * 60)

        W = example["W"]
        print("\nOriginal adjacency matrix:")
        print(np.array(W))
        print("\nComputing transitive closure...\n")

        T = transitive_closure(W)

        print("Transitive closure matrix:")
        print(np.array(T))
        print("\n(1 means there's a path from row i to column j)\n")

        plot_transitive_closure(W, T, title=example["name"])

        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    demo(3)
