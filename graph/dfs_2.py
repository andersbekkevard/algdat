"""DFS-Visit(G, u)
1 time = time + 1
2 u.d = time
3 u.color = gray
4 for each v œ G.Adj[u]
5 if v.color == white
6 v.fi = u
7 DFS-Visit(G, v)
8 time = time + 1
9 u.f = time
10 u.color = black"""


"""
DFS(G)
1 for each vertex u œ G.V
2 u.color = white
3 u.fi = nil
4 time = 0 › global
5 for each vertex u œ G.V
6 if u.color == white
7 DFS-Visit(G, u)
"""

from typing import List, Dict, Any, Optional
from enum import Enum

class Color(Enum):
    WHITE = 0
    GRAY = 1
    BLACK = 2

class Vertex:
    def __init__(self, id: int):
        self.id = id
        self.color = Color.WHITE
        self.d: Optional[int] = None  # discovery time
        self.f: Optional[int] = None  # finish time
        self.pi: Optional['Vertex'] = None  # predecessor (parent)
    
    def __repr__(self):
        return f"Vertex({self.id}, d={self.d}, f={self.f}, pi={self.pi})"

class Graph:
    def __init__(self, vertices: List[Vertex], adj: Dict[int, List[Vertex]]):
        self.V = vertices
        self.Adj = adj
    
    def __repr__(self):
        return f"Graph({len(self.V)} vertices)"

def dfs_visit(G: Graph, u: Vertex, time: List[int]) -> None:
    """
    DFS-Visit(G, u) according to the pseudocode
    """
    # 1 time = time + 1
    time[0] += 1
    # 2 u.d = time
    u.d = time[0]
    # 3 u.color = gray
    u.color = Color.GRAY
    # 4 for each v œ G.Adj[u]
    for v in G.Adj[u.id]:
        # 5 if v.color == white
        if v.color == Color.WHITE:
            # 6 v.fi = u
            v.pi = u
            # 7 DFS-Visit(G, v)
            dfs_visit(G, v, time)
    # 8 time = time + 1
    time[0] += 1
    # 9 u.f = time
    u.f = time[0]
    # 10 u.color = black
    u.color = Color.BLACK

def dfs(G: Graph, start_index: Optional[int] = None) -> None:
    """
    DFS(G) according to the pseudocode, with optional start index
    If start_index is provided, that vertex is visited first, but all vertices are still visited.
    """
    # 1 for each vertex u œ G.V
    for u in G.V:
        # 2 u.color = white
        u.color = Color.WHITE
        # 3 u.fi = nil
        u.pi = None
    # 4 time = 0 › global
    time = [0]  # Using list to make it mutable reference
    
    # 5 for each vertex u œ G.V
    if start_index is not None:
        # Validate start_index
        if not (0 <= start_index < len(G.V)):
            raise ValueError(f"start_index {start_index} is out of range [0, {len(G.V)-1}]")
        
        # Visit start vertex first
        start_vertex = G.V[start_index]
        if start_vertex.color == Color.WHITE:
            dfs_visit(G, start_vertex, time)
        
        # Then visit all remaining white vertices
        for u in G.V:
            if u.color == Color.WHITE:
                dfs_visit(G, u, time)
    else:
        # Standard DFS: visit vertices in order
        for u in G.V:
            # 6 if u.color == white
            if u.color == Color.WHITE:
                # 7 DFS-Visit(G, u)
                dfs_visit(G, u, time)

# Example usage and test
if __name__ == "__main__":
    # Create vertices
    vertices = [Vertex(i) for i in range(4)]
    
    # Create adjacency list (example graph)
    adj = {
        0: [vertices[1]],
        1: [vertices[2]],
        2: [vertices[3]],
        3: []  # Vertex 3 has no outgoing edges
    }
    
    # Create graph
    G = Graph(vertices, adj)
    
    print("Before DFS:")
    for v in G.V:
        print(f"Vertex {v.id}: color={v.color.name}, d={v.d}, f={v.f}, pi={v.pi}")
    
    # Run DFS from vertex 1 (index 1)
    print("Running DFS from vertex 1:")
    dfs(G, start_index=1)
    
    print("\nAfter DFS:")
    # Print discovery and finish times in single lines
    d_times = [v.d for v in G.V]
    f_times = [v.f for v in G.V]
    print(f"d = {d_times}")
    print(f"f = {f_times}")
    