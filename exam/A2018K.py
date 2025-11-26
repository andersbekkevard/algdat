from queue import Queue


class Graph:
    def __init__(self, n: int):
        self.n = n
        self.adj = [[0] * n for _ in range(n)]

    def add_edge(self, u: int, v: int):
        self.adj[u][v] = 1
        self.adj[v][u] = 1


def bfs(G: Graph, start: int):
    Q = Queue()
    Q.put(start)
    visited = [False] * G.n
    visited[start] = True
    while not Q.empty():
        current = Q.get()
        print(current)
        for j in range(G.n):
            if not visited[j] and G.adj[current][j] == 1:
                visited[j] = True
                Q.put(j)


G = Graph(5)
G.add_edge(0, 1)
G.add_edge(0, 2)
G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(2, 3)
G.add_edge(3, 4)

bfs(G, 0)
