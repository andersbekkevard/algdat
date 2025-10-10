import networkx as nx
import matplotlib.pyplot as plt


def create_simple_graph():
    """Create and visualize a simple graph using NetworkX."""
    # Create an undirected graph
    G = nx.Graph()

    # Add nodes (vertices)
    G.add_nodes_from([0, 1, 2, 3, 4])

    # Add edges
    G.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4)])

    # Print graph information
    print(f"Graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    print(f"Nodes: {list(G.nodes())}")
    print(f"Edges: {list(G.edges())}")
    print()

    # Visualize the graph
    plt.figure(figsize=(10, 8))

    # Use spring layout for nice positioning
    pos = nx.spring_layout(G, seed=42)

    # Draw the graph
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=1500,
        font_size=16,
        font_weight="bold",
        edge_color="gray",
        width=2,
        arrowsize=20,
    )

    plt.title("Simple NetworkX Graph", fontsize=18, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    return G


def create_weighted_graph():
    """Create and visualize a weighted graph."""
    G = nx.Graph()

    # Add weighted edges
    weighted_edges = [(0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5), (2, 3, 8), (3, 4, 3)]

    G.add_weighted_edges_from(weighted_edges)

    print("Weighted Graph:")
    print(f"Nodes: {list(G.nodes())}")
    print(f"Edges with weights:")
    for u, v, weight in G.edges(data="weight"):
        print(f"  {u} -- {v}: weight = {weight}")
    print()

    # Visualize
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)

    # Draw nodes and edges
    nx.draw_networkx_nodes(G, pos, node_color="lightcoral", node_size=1500)
    nx.draw_networkx_labels(G, pos, font_size=16, font_weight="bold")
    nx.draw_networkx_edges(G, pos, width=2, edge_color="gray")

    # Draw edge labels (weights)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=12)

    plt.title("Weighted NetworkX Graph", fontsize=18, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    return G


if __name__ == "__main__":
    print("=" * 50)
    print("Simple Graph Example")
    print("=" * 50)
    create_simple_graph()

    print("\n" + "=" * 50)
    print("Weighted Graph Example")
    print("=" * 50)
    create_weighted_graph()
