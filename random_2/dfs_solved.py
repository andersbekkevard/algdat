class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)


def dfs(G: list[Node]):
    BLACK = -1
    GREY = 1
    WHITE = 0

    n = len(G)
    d = {G[i]: -1 for i in range(n)}
    f = {G[i]: -1 for i in range(n)}
    pi = {G[i]: None for i in range(n)}
    color = {G[i]: WHITE for i in range(n)}
    time = 0

    def dfs_visit(u):
        nonlocal time
        time += 1
        d[u] = time
        color[u] = GREY
        for v in u.neighbors:
            if color[v] == WHITE:
                pi[v] = u
                dfs_visit(v)
        time += 1
        f[u] = time
        color[u] = BLACK

    for i in range(n):
        if color[G[i]] == WHITE:
            dfs_visit(G[i])

    return d, f, pi, color


if __name__ == "__main__":
    # Create a simple graph: A -> B -> C, A -> D
    A = Node("A")
    B = Node("B")
    C = Node("C")
    D = Node("D")

    A.add_neighbor(B)
    A.add_neighbor(D)
    B.add_neighbor(C)

    G = [A, B, C, D]

    d, f, pi, color = dfs(G)

    print("DFS Results:")
    print("-" * 50)
    for node in G:
        print(f"Node {node.name}:")
        print(f"  Discovery time (d): {d[node]}")
        print(f"  Finish time (f): {f[node]}")
        parent = pi[node]
        parent_name = parent.name if parent is not None else None
        print(f"  Parent (pi): {parent_name}")
        print(f"  Color: {color[node]}")
        print()
