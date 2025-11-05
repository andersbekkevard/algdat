# !/usr/bin/python3
# coding=utf-8
import random

# Testsettet på serveren er større og mer omfattende enn dette.
# Hvis programmet ditt fungerer lokalt, men ikke når du laster det opp,
# er det gode sjanser for at det er tilfeller du ikke har tatt høyde for.

# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nedre, og muligheten for å generere
# tilfeldige instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å justere på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = False
# Antall tilfeldige tester som genereres.
random_tests = 10
# Lavest mulig antall noder i generert instans.
nodes_lower = 5
# Høyest mulig antall noder i generert instans.
nodes_upper = 10
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


def solve(adj_matrix):
    """
    Determines if a directed graph contains an odd cycle.

    Args:
        adj_matrix: List of lists representing adjacency matrix of directed graph.
                    adj_matrix[i][j] = True if there's an edge from i to j, False otherwise.

    Returns:
        True if the graph contains an odd cycle (cycle with odd number of edges), False otherwise.

    Complexity: Should be O(V^3) where V is the number of vertices.
    """
    n = len(adj_matrix)

    O = [[bool(adj_matrix[i][j]) for j in range(n)] for i in range(n)]
    E = [[i == j for j in range(n)] for i in range(n)]

    for k in range(n):
        O_next = [row[:] for row in O]
        E_next = [row[:] for row in E]

        for i in range(n):
            for j in range(n):
                O_next[i][j] = O[i][j] or (O[i][k] and E[k][j]) or (E[i][k] and O[k][j])
                E_next[i][j] = E[i][j] or (O[i][k] and O[k][j]) or (E[i][k] and E[k][j])

        O, E = O_next, E_next

    return any(O[i][i] for i in range(n))


# Hardkodete tester på format: (adjacency_matrix, expected_result)
# True = graph has odd cycle, False = no odd cycle

tests = [
    # Empty graph (no vertices)
    ([], False),
    # Single vertex, no edges
    ([[False]], False),
    # Single vertex with self-loop (odd cycle: 1 edge)
    ([[True]], True),
    # Two vertices, no edges
    ([[False, False], [False, False]], False),
    # Two vertices, one edge (no cycle)
    ([[False, True], [False, False]], False),
    # Two vertices, bidirectional edges (even cycle: 2 edges)
    ([[False, True], [True, False]], False),
    # Two vertices, both with self-loops (odd cycles: 1 edge each)
    ([[True, True], [True, True]], True),
    # Three vertices, triangle (odd cycle: 3 edges)
    ([[False, True, False], [False, False, True], [True, False, False]], True),
    # Three vertices, triangle with one more edge (still odd cycle)
    ([[False, True, True], [False, False, True], [True, False, False]], True),
    # Three vertices, path of length 2 (no cycle)
    ([[False, True, False], [False, False, True], [False, False, False]], False),
    # Three vertices, bidirectional path (even cycle: 2 edges)
    ([[False, True, False], [True, False, True], [False, True, False]], False),
    # Four vertices, square (even cycle: 4 edges)
    (
        [
            [False, True, False, False],
            [False, False, True, False],
            [False, False, False, True],
            [True, False, False, False],
        ],
        False,
    ),
    # Four vertices, square with a diagonal that creates an odd cycle (0->1->2->0)
    (
        [
            [False, True, False, False],
            [False, False, True, False],
            [True, False, False, True],
            [True, False, False, False],
        ],
        True,
    ),
    # Five vertices, pentagon (odd cycle: 5 edges)
    (
        [
            [False, True, False, False, False],
            [False, False, True, False, False],
            [False, False, False, True, False],
            [False, False, False, False, True],
            [True, False, False, False, False],
        ],
        True,
    ),
    # Disconnected graph, only even 2-cycle in one component
    (
        [
            [False, True, False, False],
            [True, False, False, False],
            [False, False, False, True],
            [False, False, False, False],
        ],
        False,
    ),
    # Disconnected graph, self-loop component gives odd cycle
    ([[True, False, False], [False, False, False], [False, False, False]], True),
    # Graph with multiple paths but no cycles
    (
        [
            [False, True, True, False],
            [False, False, False, True],
            [False, False, False, True],
            [False, False, False, False],
        ],
        False,
    ),
    # Complex graph: contains odd cycle via triangle
    (
        [
            [False, True, True, False],
            [False, False, True, True],
            [True, False, False, False],
            [False, False, False, False],
        ],
        True,
    ),
    # Complex graph with only even cycles
    (
        [
            [False, True, False, False],
            [True, False, False, True],
            [False, False, False, True],
            [False, False, True, False],
        ],
        False,
    ),
]


def has_odd_cycle_bruteforce(adj_matrix):
    """
    Brute force solution to verify correctness.
    Checks all possible cycles up to length V.
    """
    V = len(adj_matrix)
    if V == 0:
        return False

    # For each vertex, try to find cycles starting from it
    for start in range(V):
        # BFS to find cycles: track (vertex, parity)
        # parity: 0 = even length path, 1 = odd length path
        visited = set()
        queue = [(start, 0)]  # (vertex, parity of path length)

        while queue:
            v, parity = queue.pop(0)

            # Check if we can return to start with opposite parity
            if v == start and parity == 1:
                return True

            state = (v, parity)
            if state in visited:
                continue
            visited.add(state)

            # Explore neighbors
            for neighbor in range(V):
                if adj_matrix[v][neighbor]:
                    new_parity = 1 - parity  # Flip parity
                    queue.append((neighbor, new_parity))

    return False


def gen_examples(k, nl, nu):
    """Generate random test instances."""
    for _ in range(k):
        V = random.randint(max(3, nl), nu)

        # Create random directed graph
        adj_matrix = [[False] * V for _ in range(V)]

        # Add some random edges
        num_edges = random.randint(V, min(V * V // 2, V * 2))
        edges_added = 0

        while edges_added < num_edges:
            i = random.randint(0, V - 1)
            j = random.randint(0, V - 1)
            if not adj_matrix[i][j]:
                adj_matrix[i][j] = True
                edges_added += 1

        # Compute expected answer using brute force
        expected = has_odd_cycle_bruteforce(adj_matrix)

        yield adj_matrix, expected


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(
        gen_examples(
            random_tests,
            nodes_lower,
            nodes_upper,
        )
    )


def get_feedback(student, answer, adj_matrix):
    """Provide feedback on student's solution."""
    if type(student) != bool:
        return f"Du returnerte ikke en bool, men {type(student).__name__}"

    if student != answer:
        V = len(adj_matrix)
        edges = []
        for i in range(V):
            for j in range(V):
                if adj_matrix[i][j]:
                    edges.append(f"{i} -> {j}")

        if answer:
            return f"Grafen har en odde sykel, men du returnerte False"
        else:
            return f"Grafen har ingen odde sykel, men du returnerte True"

    return None


def print_graph(adj_matrix):
    """Helper function to print graph in readable format."""
    V = len(adj_matrix)
    if V == 0:
        return "Tom graf (0 noder)"

    edges = []
    for i in range(V):
        for j in range(V):
            if adj_matrix[i][j]:
                edges.append(f"{i} -> {j}")

    if not edges:
        return f"Graf med {V} noder, ingen kanter"

    return f"Graf med {V} noder, kanter: {', '.join(edges)}"


failed = False
for adj_matrix, expected_answer in tests:
    student_answer = solve([row[:] for row in adj_matrix])  # Copy matrix
    response = get_feedback(student_answer, expected_answer, adj_matrix)

    if response is not None:
        if failed:
            print("-" * 50)
        failed = True
        print(
            f"""
Koden feilet for følgende instans.
{print_graph(adj_matrix)}

Ditt svar: {student_answer}
Forventet svar: {expected_answer}
Feilmelding: {response}
"""
        )


if not failed:
    print("Koden fungerte for alle eksempeltestene.")
