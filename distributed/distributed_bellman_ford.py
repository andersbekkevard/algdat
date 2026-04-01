"""Distributed Bellman–Ford (distance-vector) vs. global Bellman–Ford (CLRS 24.1).

Contrasts two approaches that compute the same all-pairs shortest paths:

  1. Distributed — each Router knows only its own distance vector d[] and its
     direct links.  Routers call notify() on each other; the receiver RELAXes
     through the link cost and, if anything improved, propagates to its own
     neighbors.  No central coordinator.

  2. Global (CLRS 24.1) — a single procedure sees the full edge list E and
     runs BELLMAN-FORD(G, w, s) for every source s.

Both produce the same |V| x |V| weight matrix.
"""

INF = float("inf")
N = 5


# ── Distributed: distance-vector routing ────────────────────────────────


class Router:
    """A node that knows only its direct links and its distance vector."""

    def __init__(self, uid: int):
        self.id = uid
        self.link: dict[int, int] = {}
        self.peer: dict[int, "Router"] = {}
        self.d: list[float] = [INF] * N
        self.d[uid] = 0

    def add_link(self, other: "Router", w: int):
        self.link[other.id] = w
        self.peer[other.id] = other
        self.d[other.id] = w

    def notify(self, sender_id: int, d_sender: list[float]):
        """Receive a neighbor's distance vector.  RELAX each entry through
        the link cost.  If anything improved, notify all own neighbors."""
        c = self.link[sender_id]
        changed = False
        for v in range(N):
            if d_sender[v] + c < self.d[v]:
                self.d[v] = d_sender[v] + c
                changed = True
        if changed:
            for peer in self.peer.values():
                peer.notify(self.id, self.d)


# ── Global: CLRS 24.1 Bellman-Ford ──────────────────────────────────────


def bellman_ford(
    edges: list[tuple[int, int, int]], s: int
) -> list[float]:
    """BELLMAN-FORD(G, w, s) -- CLRS 24.1.

    INITIALIZE-SINGLE-SOURCE then |V|-1 passes of RELAX over every edge.
    Returns d[0..N-1].  Raises on negative-weight cycle.
    """
    d: list[float] = [INF] * N
    d[s] = 0
    for _ in range(N - 1):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    for u, v, w in edges:
        if d[u] + w < d[v]:
            raise ValueError("negative-weight cycle")
    return d


# ── Shared topology ─────────────────────────────────────────────────────


def build_network() -> tuple[list[Router], list[tuple[int, int, int]]]:
    """
        0 ---1--- 1 ---1--- 3
        |         |         |
        3         1         1
        |         |         |
        +-------- 2 --------+

        4  (isolated)
    """
    routers = [Router(i) for i in range(N)]

    def link(a: int, b: int, w: int):
        routers[a].add_link(routers[b], w)
        routers[b].add_link(routers[a], w)

    link(0, 1, 1)
    link(0, 2, 3)
    link(1, 2, 1)
    link(1, 3, 1)
    link(2, 3, 1)

    edges = [(r.id, nid, w) for r in routers for nid, w in r.link.items()]
    return routers, edges


# ── Display ─────────────────────────────────────────────────────────────


def print_matrix(matrix: list[list[float]], title: str):
    def fmt(x: float) -> str:
        return "\u221e" if x == INF else str(int(x))

    cw = 4
    hdr = "     \u2502 " + " ".join(f"{j:^{cw}}" for j in range(N))
    print(title)
    print(hdr)
    print("\u2500" * len(hdr))
    for i, row in enumerate(matrix):
        print(f"  {i}  \u2502 " + " ".join(f"{fmt(v):^{cw}}" for v in row))
    print()


# ── Main ────────────────────────────────────────────────────────────────


def main():
    # -- distributed: each router notifies its neighbors to start --
    routers, edges = build_network()
    for r in routers:
        for peer in r.peer.values():
            peer.notify(r.id, r.d)
    dist_matrix = [list(routers[i].d) for i in range(N)]

    # -- global CLRS --
    global_matrix = [bellman_ford(edges, s) for s in range(N)]

    print_matrix(dist_matrix, "Distributed (synchronous distance-vector)")
    print_matrix(global_matrix, "Global (CLRS 24.1 Bellman-Ford)")

    if dist_matrix == global_matrix:
        print("✅ Matrices match: distributed converges to global shortest paths.")
    else:
        print("🚫 Matrices differ!")


if __name__ == "__main__":
    main()
