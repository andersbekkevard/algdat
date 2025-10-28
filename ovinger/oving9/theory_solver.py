# !/usr/bin/python3
# coding=utf-8

from collections import defaultdict

# Testsettet på serveren er større og mer omfattende enn dette.
# Hvis programmet ditt fungerer lokalt, men ikke når du laster det opp,
# er det gode sjanser for at det er tilfeller du ikke har tatt høyde for.

# De lokale testene består av to deler. Et lite sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for å teste på
# et større sett med 1000 genererte instanser. For å teste på det
# større settet med genererte instanser, må du (1) laste ned filen med
# testene fra øvingssystemet, (2) legge den samme plass som denne
# python-filen og (3) sette variabelen under til True.
use_extra_tests = True


class Node:
    def __init__(self, name):
        self.name = name
        self.e = self
        self.g = self
        self.rank = 0

    def __str__(self) -> str:
        return f"Node(name={self.name}, e={self.e.name}, g={self.g.name}, rank={self.rank})"

    def __repr__(self) -> str:
        return self.__str__()


def find_greater(node: Node) -> Node:
    if node.g != node:
        node.g = find_greater(node.g)
    return node.g


def link_greater(a: Node, b: Node) -> bool:
    """
    Performs a union of two nodes. Returns true if a change was made
    (False then means "was already in same set, we have a cycle")
    """
    root_a = find_greater(a)
    root_b = find_greater(b)

    if root_a == root_b:
        return True  # Already in same chain, constraint is satisfied

    root_a.g = root_b
    return True


def find_equivalence(node: Node) -> Node:
    if node.e != node:
        node.e = find_equivalence(node.e)
    return node.e


def equivalence(a: Node, b: Node) -> bool:
    """
    Performs a union of two nodes. Returns true if a change was made
    (False then means "was already in same set, we have a cycle")
    """
    root_a = find_equivalence(a)
    root_b = find_equivalence(b)

    if root_a == root_b:
        return False

    if root_a.rank > root_b.rank:
        root_b.e = root_a
    else:
        root_a.e = root_b
    if root_a.rank == root_b.rank:
        root_b.rank += 1
    return True


def check(variables, constraints):
    """
    `variables` er en liste med tekststrenger som hver representerer en variabel.
    `constraints` er en liste med tupler på formen `(a, comp, b)`, der `a` og `b`
    er tekststrenger fra `variables` og `comp` kan være `"="`, `"<"` eller `">"`.

    Funksjonen skal returnere `True` hvis det er mulig å gi variablene i `variables`
    tallverdier som overholder restriksjonene i `constraints`, og `False` ellers.
    """
    # Dersom "=", så er variablene like, og kan derfor slås sammen
    node_map = {var: Node(var) for var in variables}

    # First pass: process equality constraints
    for a, comp, b in constraints:
        if comp == "=":
            equivalence(node_map[a], node_map[b])

    # Build graph of inequality constraints using representatives

    graph = defaultdict(set)

    for a, comp, b in constraints:
        if comp != "=":
            n1 = find_equivalence(node_map[a])
            n2 = find_equivalence(node_map[b])

            # Check for immediate contradiction (x < x or x > x)
            if n1 == n2:
                return False

            if comp == "<":
                graph[n1].add(n2)
            else:  # comp == ">"
                graph[n2].add(n1)

    # Check for cycles using DFS
    def has_cycle():
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {}

        def dfs(node):
            if node in color:
                return color[node] == GRAY  # Cycle if we hit a gray node

            color[node] = GRAY
            for neighbor in graph[node]:
                if dfs(neighbor):
                    return True
            color[node] = BLACK
            return False

        for node in list(graph.keys()):
            if node not in color:
                if dfs(node):
                    return True
        return False

    return not has_cycle()


# Hardkodete tester på format: (variables, constraints), riktig svar
tests = [
    ((["x1"], []), True),
    ((["x1", "x2"], [("x1", "=", "x2")]), True),
    ((["x1"], [("x1", ">", "x1")]), False),
    ((["x1"], [("x1", "=", "x1")]), True),
    ((["x1", "x2"], [("x1", "<", "x2")]), True),
    ((["x1", "x2"], [("x2", "<", "x1"), ("x1", "=", "x2")]), False),
    ((["x1", "x2"], [("x2", ">", "x1"), ("x1", "<", "x2")]), True),
    ((["x1", "x2"], [("x1", ">", "x2"), ("x2", ">", "x1")]), False),
    (
        (
            ["x1", "x2", "x3"],
            [("x1", "<", "x2"), ("x2", "<", "x3"), ("x1", ">", "x3")],
        ),
        False,
    ),
    (
        (
            ["x1", "x2", "x3"],
            [("x1", "<", "x2"), ("x3", "=", "x1"), ("x2", "<", "x3")],
        ),
        False,
    ),
    ((["x4", "x0", "x1"], [("x1", "<", "x0")]), True),
    ((["x5", "x8"], [("x8", "<", "x5"), ("x8", "<", "x5")]), True),
    ((["x1", "x0", "x2"], []), True),
    (
        (
            ["x4", "x8", "x5"],
            [("x4", "<", "x5"), ("x8", ">", "x5"), ("x5", "<", "x8")],
        ),
        True,
    ),
    (
        (
            ["x5", "x9", "x0"],
            [
                ("x9", ">", "x5"),
                ("x9", "=", "x0"),
                ("x0", "=", "x9"),
                ("x0", "=", "x9"),
            ],
        ),
        True,
    ),
    (
        (
            ["x0", "x6", "x7"],
            [("x7", "=", "x0"), ("x7", ">", "x0"), ("x6", ">", "x0")],
        ),
        False,
    ),
    ((["x8", "x6", "x0"], []), True),
    (
        (
            ["x8", "x7", "x0"],
            [("x8", "=", "x0"), ("x0", "=", "x8"), ("x0", "=", "x8")],
        ),
        True,
    ),
    (
        (
            ["x8", "x4"],
            [
                ("x4", ">", "x8"),
                ("x4", ">", "x8"),
                ("x8", "<", "x4"),
                ("x4", ">", "x8"),
                ("x8", "=", "x4"),
            ],
        ),
        False,
    ),
    ((["x3", "x8", "x5"], [("x3", ">", "x8")]), True),
]


failed = False
for test_case, answer in tests:
    variables, constraints = test_case
    if variables == ["x1", "x2"] and constraints == [
        ("x2", ">", "x1"),
        ("x1", "<", "x2"),
    ]:
        pass  # Breakpoint: First failing test case
    student = check(variables, constraints)
    if student != answer:
        if failed:
            print("-" * 50)
        failed = True
        print(
            f"""
Koden feilet for følgende instans:
variables: {', '.join(variables)}
constraints:
    {(chr(10) + '    ').join(' '.join(x) for x in constraints)}

Ditt svar: {student}
Riktig svar: {answer}
"""
        )

if use_extra_tests:
    with open("ovinger/oving9/tests_theory_solver.txt") as extra_tests_data:
        extra_tests = []
        for line in extra_tests_data:
            variables, constraints, answer = line.strip().split(" | ")
            variables = variables.split(",")
            constraints = [x.split(" ") for x in constraints.split(",")]
            extra_tests.append(((variables, constraints), bool(int(answer))))

    n_failed = 0
    for test_case, answer in extra_tests:
        variables, constraints = test_case
        student = check(variables, constraints)
        if student != answer:
            n_failed += 1
            if failed and n_failed <= 5:
                print("-" * 50)

            failed = True
            if n_failed <= 5:
                print(
                    f"""
Koden feilet for følgende instans:
variables: {', '.join(variables)}
constraints:
    {(chr(10) + '    ').join(' '.join(x) for x in constraints)}

Ditt svar: {student}
Riktig svar: {answer}
"""
                )
            elif n_failed == 6:
                print("Koden har feilet for mer enn 5 av de ekstra testene.")
                print("De resterende feilene vil ikke skrives ut.")

    if n_failed > 0:
        print(f"Koden feilet for {n_failed} av de ekstra testene.")

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")
