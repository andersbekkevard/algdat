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
    Counts the number of paths from i to j for all pairs (i, j) in a DAG.

    Args:
        adj_matrix: List of lists representing adjacency matrix of directed acyclic graph.
                    adj_matrix[i][j] = True if there's an edge from i to j, False otherwise.

    Returns:
        A matrix T where T[i][j] is the number of paths from vertex i to vertex j.
        Note: T[i][i] = 1 (one path from a vertex to itself).

    Complexity: Should be O(V^3) where V is the number of vertices.
    """
    n = len(adj_matrix)

    C = [[1 if adj_matrix[i][j] or i == j else 0 for j in range(n)] for i in range(n)]

    for k in range(n):
        C_next = [row[:] for row in C]

        for i in range(n):
            if i == k:
                continue
            for j in range(n):
                if j == k or j == i:
                    continue
                C_next[i][j] = C[i][j] + C[i][k] * C[k][j]

        C = C_next

    return C


# Hardkodete tester på format: (adjacency_matrix, expected_result_matrix)
# expected_result_matrix[i][j] = number of paths from i to j
tests = [
    # Empty graph (no vertices)
    ([], []),
    # Single vertex, no edges
    ([[False]], [[1]]),
    # Single vertex with self-loop (should still be 1, as self-loops don't create new paths in DAG context)
    # Note: In a DAG, self-loops shouldn't exist, but we test edge cases
    ([[True]], [[1]]),
    # Two vertices, no edges
    (
        [[False, False], [False, False]],
        [[1, 0], [0, 1]],
    ),
    # Two vertices, one edge: 0 -> 1
    (
        [[False, True], [False, False]],
        [[1, 1], [0, 1]],
    ),
    # Two vertices, one edge: 1 -> 0
    (
        [[False, False], [True, False]],
        [[1, 0], [1, 1]],
    ),
    # Three vertices, linear chain: 0 -> 1 -> 2
    (
        [[False, True, False], [False, False, True], [False, False, False]],
        [[1, 1, 1], [0, 1, 1], [0, 0, 1]],
    ),
    # Three vertices, fork: 0 -> 1, 0 -> 2
    (
        [[False, True, True], [False, False, False], [False, False, False]],
        [[1, 1, 1], [0, 1, 0], [0, 0, 1]],
    ),
    # Three vertices, merge: 0 -> 2, 1 -> 2
    (
        [[False, False, True], [False, False, True], [False, False, False]],
        [[1, 0, 1], [0, 1, 1], [0, 0, 1]],
    ),
    # Three vertices, diamond: 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3 (wait, that's 4 vertices)
    # Let's do: 0 -> 1, 0 -> 2, 1 -> 2
    (
        [[False, True, True], [False, False, True], [False, False, False]],
        [[1, 1, 2], [0, 1, 1], [0, 0, 1]],
    ),
    # Four vertices, linear: 0 -> 1 -> 2 -> 3
    (
        [
            [False, True, False, False],
            [False, False, True, False],
            [False, False, False, True],
            [False, False, False, False],
        ],
        [[1, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1]],
    ),
    # Four vertices, diamond: 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3
    (
        [
            [False, True, True, False],
            [False, False, False, True],
            [False, False, False, True],
            [False, False, False, False],
        ],
        [[1, 1, 1, 2], [0, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 1]],
    ),
    # Four vertices, multiple paths: 0 -> 1 -> 3, 0 -> 2 -> 3, 1 -> 2
    (
        [
            [False, True, True, False],
            [False, False, True, True],
            [False, False, False, True],
            [False, False, False, False],
        ],
        [[1, 1, 2, 3], [0, 1, 1, 2], [0, 0, 1, 1], [0, 0, 0, 1]],
    ),
    # Five vertices, complex DAG
    (
        [
            [False, True, True, False, False],
            [False, False, False, True, False],
            [False, False, False, True, True],
            [False, False, False, False, True],
            [False, False, False, False, False],
        ],
        [
            [1, 1, 1, 2, 3],
            [0, 1, 0, 1, 1],
            [0, 0, 1, 1, 2],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1],
        ],
    ),
    # Disconnected graph (two components)
    (
        [
            [False, True, False, False],
            [False, False, False, False],
            [False, False, False, True],
            [False, False, False, False],
        ],
        [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]],
    ),
    # Single isolated vertex
    (
        [[False]],
        [[1]],
    ),
    # Two isolated vertices
    (
        [[False, False], [False, False]],
        [[1, 0], [0, 1]],
    ),
]


def count_paths_bruteforce(adj_matrix):
    """
    Brute force solution to count paths by enumerating all paths.
    Uses DFS to find all paths from each vertex to each vertex.
    """
    V = len(adj_matrix)
    if V == 0:
        return []

    result = [[0] * V for _ in range(V)]

    def dfs_count_paths(start, current, target, visited):
        """Count paths from start to target, using DFS."""
        if current == target:
            return 1

        # Mark current as visited to avoid cycles (shouldn't happen in DAG)
        visited.add(current)
        count = 0

        for neighbor in range(V):
            if adj_matrix[current][neighbor] and neighbor not in visited:
                count += dfs_count_paths(start, neighbor, target, visited)

        visited.remove(current)
        return count

    # For each pair (i, j), count paths
    for i in range(V):
        for j in range(V):
            if i == j:
                result[i][j] = 1  # One path from vertex to itself
            else:
                visited = set()
                result[i][j] = dfs_count_paths(i, i, j, visited)

    return result


def is_dag(adj_matrix):
    """Check if graph is a DAG using topological sort."""
    V = len(adj_matrix)
    if V == 0:
        return True

    # Calculate in-degrees
    in_degree = [0] * V
    for i in range(V):
        for j in range(V):
            if adj_matrix[i][j]:
                in_degree[j] += 1

    # Find vertices with no incoming edges
    queue = [i for i in range(V) if in_degree[i] == 0]
    processed = 0

    while queue:
        u = queue.pop(0)
        processed += 1

        for v in range(V):
            if adj_matrix[u][v]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

    # If we processed all vertices, it's a DAG
    return processed == V


def gen_examples(k, nl, nu):
    """Generate random DAG test instances."""
    for _ in range(k):
        V = random.randint(max(3, nl), nu)

        # Create random DAG by ensuring topological order
        # Number vertices and only allow edges from lower to higher indices
        adj_matrix = [[False] * V for _ in range(V)]

        # Add some random edges (only from i to j where i < j)
        num_edges = random.randint(V - 1, min(V * (V - 1) // 2, V * 2))
        edges_added = 0

        while edges_added < num_edges:
            i = random.randint(0, V - 2)
            j = random.randint(i + 1, V - 1)
            if not adj_matrix[i][j]:
                adj_matrix[i][j] = True
                edges_added += 1

        # Verify it's a DAG (should always be true, but check anyway)
        if not is_dag(adj_matrix):
            continue  # Skip if somehow not a DAG

        # Compute expected answer using brute force
        expected = count_paths_bruteforce(adj_matrix)

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
    if type(student) != list:
        return f"Du returnerte ikke en liste, men {type(student).__name__}"

    V = len(adj_matrix)

    if V == 0:
        if student != []:
            return f"For tom graf, forventet [], men fikk {student}"
        return None

    if len(student) != V:
        return f"Matrisen din har {len(student)} rader, men forventet {V}"

    for i in range(V):
        if type(student[i]) != list:
            return f"Rad {i} er ikke en liste, men {type(student[i]).__name__}"
        if len(student[i]) != V:
            return f"Rad {i} har {len(student[i])} kolonner, men forventet {V}"

    # Check each cell
    for i in range(V):
        for j in range(V):
            if type(student[i][j]) != int:
                return f"Element [{i}][{j}] er ikke et heltall, men {type(student[i][j]).__name__}"
            if student[i][j] != answer[i][j]:
                edges = []
                for x in range(V):
                    for y in range(V):
                        if adj_matrix[x][y]:
                            edges.append(f"{x} -> {y}")

                return (
                    f"Element [{i}][{j}] er feil.\n"
                    f"  Ditt svar: {student[i][j]}\n"
                    f"  Forventet: {answer[i][j]}\n"
                    f"  Graf: {', '.join(edges) if edges else 'ingen kanter'}"
                )

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


def print_matrix(matrix):
    """Helper function to print matrix in readable format."""
    if not matrix:
        return "[]"

    lines = []
    for row in matrix:
        lines.append("[" + ", ".join(str(x) for x in row) + "]")
    return "\n".join(lines)


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

Ditt svar:
{print_matrix(student_answer)}

Forventet svar:
{print_matrix(expected_answer)}

Feilmelding: {response}
"""
        )


if not failed:
    print("Koden fungerte for alle eksempeltestene.")
