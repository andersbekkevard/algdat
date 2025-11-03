INF = float("inf")


def floyd_warshall(W: list[list[float]]):
    n = len(W)
    D = [[0 if i == j else W[i][j] for j in range(n)] for i in range(n)]
    PI = [[i if W[i][j] != INF else None for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if D[i][j] > D[i][k] + D[k][j]:
                    D[i][j] = D[i][k] + D[k][j]
                    PI[i][j] = PI[k][j]
    return D, PI

    # Example of a simple graph weight matrix


def print_path(PI, i, j):
    if i == j:
        print(i, end=" ")
    elif PI[i][j] is None:
        print("No path exists")
    else:
        print_path(PI, i, PI[i][j])
        print(j, end=" ")


def plot_graph(W: list[list[float]]):
    """
    Plot a directed graph from an adjacency matrix.

    Args:
        W: Adjacency matrix (weight matrix) of the graph. INF values indicate no edge.
    """
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except ImportError:
        print("Visualization requires networkx and matplotlib.")
        print("Install with: pip install networkx matplotlib")
        return

    n = len(W)
    G = nx.DiGraph()

    # Add nodes
    G.add_nodes_from(range(n))

    # Add edges with weights (skip INF edges)
    for i in range(n):
        for j in range(n):
            if W[i][j] != INF:
                G.add_edge(i, j, weight=W[i][j])

    # Create figure
    plt.figure(figsize=(10, 8))

    # Use spring layout for nice positioning
    pos = nx.spring_layout(G, seed=42)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=1500, alpha=0.9)

    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=16, font_weight="bold")

    # Draw edges with arrows
    # For bidirectional edges, use different curvatures to make them visible
    edges = list(G.edges())
    bidirectional_pairs = set()
    single_direction_edges = []

    for edge in edges:
        reverse = (edge[1], edge[0])
        if reverse in edges and edge not in bidirectional_pairs:
            # Mark both directions as bidirectional
            bidirectional_pairs.add(edge)
            bidirectional_pairs.add(reverse)
        elif edge not in bidirectional_pairs:
            single_direction_edges.append(edge)

    # Draw bidirectional edges with stronger curvature (one up, one down)
    bidirectional_list = list(bidirectional_pairs)
    for edge in bidirectional_list:
        if edge[0] < edge[1]:
            # First edge - curve upward
            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=[edge],
                edge_color="darkblue",
                width=2.5,
                alpha=0.8,
                arrows=True,
                arrowsize=25,
                arrowstyle="->",
                connectionstyle="arc3,rad=0.3",
                min_source_margin=15,
                min_target_margin=15,
            )
        else:
            # Reverse edge - curve downward
            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=[edge],
                edge_color="darkblue",
                width=2.5,
                alpha=0.8,
                arrows=True,
                arrowsize=25,
                arrowstyle="->",
                connectionstyle="arc3,rad=-0.3",
                min_source_margin=15,
                min_target_margin=15,
            )

    # Draw single-direction edges with slight curvature
    if single_direction_edges:
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=single_direction_edges,
            edge_color="darkblue",
            width=2.5,
            alpha=0.8,
            arrows=True,
            arrowsize=25,
            arrowstyle="->",
            connectionstyle="arc3,rad=0.1",
            min_source_margin=15,
            min_target_margin=15,
        )

    # Draw edge labels (weights) with better positioning
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=11,
        font_color="darkred",
        font_weight="bold",
        bbox=dict(
            boxstyle="round,pad=0.3", facecolor="white", edgecolor="none", alpha=0.9
        ),
        rotate=False,  # Keep labels horizontal for readability
    )

    plt.title("Directed Graph Visualization", fontsize=18, fontweight="bold", pad=20)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


simple_graph = [
    [INF, 3, INF, 7],
    [8, INF, 2, INF],
    [5, INF, INF, 1],
    [2, INF, INF, INF],
]


def print_matrix(matrix):
    print()
    for i in range(len(matrix)):
        print("[", end="")
        for j in range(len(matrix[i])):
            print(matrix[i][j], end="")
            if j < len(matrix[i]) - 1:
                print(" ", end="")
        print("]", end="")
        print()


if __name__ == "__main__":
    print("\nSimple graph:")
    print_matrix(simple_graph)
    print("\nPlotting graph:")
    print("\nRunning Floyd-Warshall algorithm:")
    D, PI = floyd_warshall(simple_graph)
    print("\nDistance matrix:")
    print_matrix(D)
    print("\nPredecessor matrix:")
    print_matrix(PI)
    print("\nPath from 0 to 2:")
    print_path(PI, 0, 2)
    print()
    plot_graph(simple_graph)
