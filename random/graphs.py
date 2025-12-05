from queue import Queue


def bfs(G, s):
    INF = 1e9
    n = len(G)
    pi = [None] * n
    d = [INF] * n
    visited = [False] * n

    Q = Queue()
    Q.put(s)
    visited[s] = True
    d[s] = 0

    while Q:
        u = Q.get()
        for v in G[u]:
            if not visited[v]:
                d[v] = d[u] + 1
                pi[v] = u
                visited[v] = True
                Q.put(v)
    return d, pi
