# !/usr/bin/python3
# coding=utf-8

import random

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = True
# Antall tilfeldige tester som genereres.
random_tests = 1_000
# Lavest mulig antall ruter i generert instans.
cells_lower = 3
# Høyest mulig antall ruter i generert instans.
cells_upper = 20
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


def solve_dp(board):
    """
    Finner minimum antall trekk for å komme fra første til siste rute.

    Du starter på rute 0 (helt til venstre) og skal nå rute n-1 (helt til høyre).
    Hver rute inneholder et tall som angir maksimalt hvor langt du kan flytte
    i ett trekk når du står på den ruten.

    Args:
        board: Liste av positive heltall der board[i] angir maks antall ruter
               du kan flytte fremover fra rute i.
               Lengde n >= 3.
               Det er alltid mulig å nå siste rute.

    Returns:
        Minimum antall trekk for å nå siste rute (int).

    Eksempel:
        board = [3, 5, 5, 3, 1, 4, 1, 2, 5, 3, 5, 2, 1, 1, 0]
        (Tilsvarer figur 3 i oppgaven: A=3, B=5, C=5, ..., O=★)

        Fra rute 0 (verdi 3) kan du hoppe til rute 1, 2 eller 3.
        Målet er å finne færrest mulig hopp for å nå rute 14.
    """
    INF = 1e9
    n = len(board)
    dp = [INF] * n
    dp[n - 1] = 0
    for i in range(n - 2, -1, -1):
        d = dp[i]
        for s in range(1, board[i] + 1):
            if i + s >= n:
                break
            d = min(d, dp[i + s] + 1)
        dp[i] = d
    return dp[0]


class Queue:
    def __init__(self, capacity):
        self.items = [0] * capacity
        self.capacity = capacity
        self.head = 0
        self.tail = 0
        self.size = 0

    def enqueue(self, item):
        if self.size == self.capacity:
            raise Exception("Queue is full")
        self.items[self.tail] = item
        self.tail = (self.tail + 1) % self.capacity
        self.size += 1

    def dequeue(self):
        if self.size == 0:
            raise Exception("Queue is empty")
        item = self.items[self.head]
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return item

    def empty(self):
        return self.size == 0


def solve(board):
    # Build graph, O(s * n)
    n = len(board)
    G = [[] for _ in range(n)]
    for i in range(n):
        for step in range(1, board[i] + 1):
            if i + step >= n:
                break
            G[i].append(i + step)

    # BFS, O(V + E) = O(s * n)
    s, f = 0, n - 1
    visited = [False] * n
    pred = [-1] * n
    Q = Queue(n)
    Q.enqueue(s)

    while not Q.empty():
        current = Q.dequeue()
        for neighbor in G[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                pred[neighbor] = current
                Q.enqueue(neighbor)

    # Backtrack length of shortest path
    steps = 1
    pi = f
    if pred[pi] == -1:
        return -1
    while (pi := pred[pi]) != s:
        steps += 1

    return steps


def solve_lf(board):
    """
    La antall trekk t være 1, la k = m = r[1] og gjenta det følgende for i = 2 til n - 1:
    La k = k - 1. La m være maks av m og i + r[i]. Hvis k = 0, la k = m - i og t = t + 1
    """
    n = len(board)
    t = 1
    k = m = board[0]

    for i in range(1, n - 1):
        k -= 1
        m = max(m, i + board[i])
        if k == 0:
            k = m - i
            t += 1

    return t


# Hardkodete tester på format: (board, expected_moves)
STATIC_TESTS = [
    ([2, 1, 0], 1),
    ([1, 1, 0], 2),
    ([5, 0, 0, 0, 0, 0], 1),
    ([1, 1, 1, 1, 0], 4),
    ([2, 3, 1, 1, 4, 0], 3),
    ([3, 5, 5, 3, 1, 4, 1, 2, 5, 3, 5, 2, 1, 1, 0], 5),
    ([2, 1, 3, 1, 1, 1, 0], 3),
    ([4, 1, 1, 1, 2, 1, 0], 2),
    ([1, 2, 1, 1, 1, 0], 4),
    ([2, 2, 2, 2, 2, 2, 0], 3),
]


def min_moves_bruteforce(board):
    """Brute force BFS for å verifisere korrekthet."""
    from collections import deque

    n = len(board)
    if n <= 1:
        return 0

    visited = [False] * n
    queue = deque([(0, 0)])
    visited[0] = True

    while queue:
        pos, moves = queue.popleft()
        for jump in range(1, board[pos] + 1):
            next_pos = pos + jump
            if next_pos >= n - 1:
                return moves + 1
            if not visited[next_pos]:
                visited[next_pos] = True
                queue.append((next_pos, moves + 1))

    return -1


def gen_random_board(n, max_step=5):
    """Generer tilfeldig brett med n ruter."""
    board = []
    for i in range(n - 1):
        remaining = n - 1 - i
        max_jump = min(remaining, random.randint(1, max_step))
        board.append(random.randint(1, max(1, max_jump)))
    board.append(0)
    return board


def test_solutions(*solvers):
    """Test en eller flere løsningsfunksjoner mot testene."""
    if not solvers:
        solvers = [solve]

    tests = STATIC_TESTS[:]
    if generate_random_tests:
        if seed:
            random.seed(seed)
        for _ in range(random_tests):
            board = gen_random_board(random.randint(cells_lower, cells_upper))
            expected = min_moves_bruteforce(board)
            tests.append((board, expected))

    for fn in solvers:
        failed = 0
        for board, expected in tests:
            result = fn(board[:])
            if result != expected:
                failed += 1
                if failed <= 3:
                    print(
                        f"{fn.__name__}: Feil for {board[:10]}{'...' if len(board) > 10 else ''}"
                    )
                    print(f"  Forventet: {expected}, Fikk: {result}")

        if failed == 0:
            print(f"✓ {fn.__name__}: Alle {len(tests)} tester bestått")
        else:
            print(f"✗ {fn.__name__}: {failed}/{len(tests)} tester feilet")


def benchmark(*solvers, sizes=None, runs=5):
    """Benchmark løsningsfunksjoner på store instanser."""
    import time

    if not solvers:
        raise ValueError("Må oppgi minst én funksjon å benchmarke")
    if sizes is None:
        sizes = [100, 1_000, 10_000, 50_000]

    # Samle resultater: {n: {fn_name: tid_ms}}
    results = {n: {} for n in sizes}

    for n in sizes:
        boards = [gen_random_board(n) for _ in range(runs)]
        for fn in solvers:
            start = time.perf_counter()
            for board in boards:
                fn(board[:])
            elapsed = (time.perf_counter() - start) / runs * 1000
            results[n][fn.__name__] = elapsed

    # Pretty print
    names = [fn.__name__ for fn in solvers]
    col_width = max(12, max(len(name) for name in names) + 2)

    print()
    print(
        "┌"
        + "─" * 10
        + "┬"
        + ("─" * col_width + "┬") * (len(names) - 1)
        + "─" * col_width
        + "┐"
    )
    print(
        "│"
        + "n".center(10)
        + "│"
        + "│".join(name.center(col_width) for name in names)
        + "│"
    )
    print(
        "├"
        + "─" * 10
        + "┼"
        + ("─" * col_width + "┼") * (len(names) - 1)
        + "─" * col_width
        + "┤"
    )

    for n in sizes:
        times = [results[n][name] for name in names]
        min_time = min(times)

        cells = []
        for t in times:
            formatted = f"{t:.3f} ms"
            if t == min_time and len(times) > 1:
                formatted = f"⚡{t:.3f} ms"
            cells.append(formatted.center(col_width))

        print("│" + f"{n:,}".center(10) + "│" + "│".join(cells) + "│")

    print(
        "└"
        + "─" * 10
        + "┴"
        + ("─" * col_width + "┴") * (len(names) - 1)
        + "─" * col_width
        + "┘"
    )

    # Speedup summary
    if len(solvers) > 1:
        print()
        baseline = names[0]
        for n in sizes:
            base_time = results[n][baseline]
            speedups = [f"{base_time / results[n][name]:.1f}x" for name in names[1:]]
            print(
                f"n={n:,}: {', '.join(names[1:])} er {', '.join(speedups)} vs {baseline}"
            )
    print()


if __name__ == "__main__":
    # Kjør tester på alle løsninger
    # test_solutions(solve_dp, solve, solve_lf)

    # Uncomment for benchmark:
    benchmark(solve_dp, solve, solve_lf)
