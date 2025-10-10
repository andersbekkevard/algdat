class Graph:
    def __init__(self, size):
        self.size = size
        self.adjacency_matrix = [[0 for _ in range(size)] for _ in range(size)]

    def add_edge(self, vertex1, vertex2):
        self.adjacency_matrix[vertex1][vertex2] = 1
        self.adjacency_matrix[vertex2][vertex1] = 1

    def remove_edge(self, vertex1, vertex2):
        self.adjacency_matrix[vertex1][vertex2] = 0
        self.adjacency_matrix[vertex2][vertex1] = 0

    def get_neighbors(self, vertex):
        return [i for i in range(self.size) if self.adjacency_matrix[vertex][i] == 1]

    def get_size(self):
        return self.size

    def get_adjacency_matrix(self):
        return self.adjacency_matrix

    def __str__(self):
        result = [f"Graph with {self.size} vertices"]
        result.append("")

        # List all vertices
        result.append("Vertices:")
        result.append("  " + ", ".join(str(i) for i in range(self.size)))
        result.append("")

        # List all edges (avoiding duplicates since it's an undirected graph)
        edges = []
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if self.adjacency_matrix[i][j] == 1:
                    edges.append(f"{i} -- {j}")

        result.append("Edges:")
        if edges:
            for edge in edges:
                result.append(f"  {edge}")
        else:
            result.append("  (no edges)")

        return "\n".join(result)


if __name__ == "__main__":
    g = Graph(5)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 3)
    print(g)
