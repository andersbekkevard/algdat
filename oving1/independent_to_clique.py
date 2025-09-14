"""
Gitt en urettet graf graf G=(V,E)
G=(V,E) og et positivt heltall k
k skal vi finne ut om det finnes en delmengde av V
V med k
k noder hvor ingen av nodene har en kant mellom seg. I figuren under kan du se en graf med en uavhengig mengde av størrelse 2.
"""


def independent_set_to_clique(G, k):
    new_G = []
    for l in G:
        new_G.append([0 if n == 1 else 1 for n in l])

    for i in range(len(new_G)):
        new_G[i][i] = 0  # set the diagonal to 0
    return clique(new_G, k)


"""
Gitt en urettet graf G=(V,E)
G=(V,E) og et positivt heltall k
k skal vi finne ut om det finnes en klikk i G
G av størrelse k
k. En klikk er en delmengde V′
V 
′
  av noder fra V
V hvor det er en kant mellom hvert par med noder (en komplett graf med k
k noder). I figuren under kan du se du en graf med en klikk av størrelse 3.
"""


def clique(G, k):
    """
    Check if graph G contains a clique of size k.
    G must be represented as an adjacency matrix: list of lists where G[i][j] == 1 if edge exists
    """
    if k <= 0:
        return True
    if k == 1:
        return len(G) >= 1

    n = len(G)
    if n < k:
        return False

    # Helper function to check if a subset forms a clique
    def is_clique(subset):
        for i in range(len(subset)):
            for j in range(i + 1, len(subset)):
                v1, v2 = subset[i], subset[j]
                # Check if edge exists between v1 and v2
                if G[v1][v2] != 1:
                    return False
        return True

    # Backtracking function to find clique
    def find_clique(current, start, remaining):
        if len(current) == k:
            return is_clique(current)

        if len(current) + (n - start) < k:
            return False

        for i in range(start, n):
            if remaining > 0:
                current.append(i)
                if find_clique(current, i + 1, remaining - 1):
                    return True
                current.pop()

        return False

    return find_clique([], 0, k)


# --------------- TESTS (print-only, no pytest) ---------------

import itertools
import random


def _is_clique_matrix(G, subset):
    for i, j in itertools.combinations(subset, 2):
        if G[i][j] != 1:
            return False
    return True


def _is_independent_matrix(G, subset):
    for i, j in itertools.combinations(subset, 2):
        if G[i][j] != 0:
            return False
    return True


def _clique_exists_oracle(G, k):
    n = len(G)
    for subset in itertools.combinations(range(n), k):
        if _is_clique_matrix(G, subset):
            return True
    return False


def _independent_exists_oracle(G, k):
    n = len(G)
    for subset in itertools.combinations(range(n), k):
        if _is_independent_matrix(G, subset):
            return True
    return False


def _complement(G):
    n = len(G)
    return [[0 if i == j else 1 - G[i][j] for j in range(n)] for i in range(n)]


# Harness
TOTAL = 0
PASSED = 0


def check(name, cond, explain_ok="", explain_bad=""):
    global TOTAL, PASSED
    TOTAL += 1
    if cond:
        PASSED += 1
        print(f"[PASS] {name} {explain_ok}")
    else:
        print(f"[FAIL] {name} {explain_bad}")


def check_equivalence_IS_to_Clique(G, k):
    want = _independent_exists_oracle(G, k)
    got = independent_set_to_clique(G, k)
    ok = got == want
    return ok, want, got


def check_clique_oracle(G, k):
    want = _clique_exists_oracle(G, k)
    got = clique(G, k)
    ok = got == want
    return ok, want, got


print("\n=== Deterministic tests ===")

# 1) Single vertex
G = [[0]]
ok1, want1, got1 = check_equivalence_IS_to_Clique(G, 1)
check(
    "Independent set reduction on 1-node graph, k=1",
    ok1,
    explain_ok=f"(expected {want1}, got {got1})",
    explain_bad=f"(expected {want1}, got {got1})",
)

ok1c, want1c, got1c = check_clique_oracle(_complement(G), 1)
check(
    "Clique oracle agreement on complement, k=1",
    ok1c,
    explain_ok=f"(expected {want1c}, got {got1c})",
    explain_bad=f"(expected {want1c}, got {got1c})",
)

# 2) Two isolated vertices
G = [
    [0, 0],
    [0, 0],
]
ok2, want2, got2 = check_equivalence_IS_to_Clique(G, 2)
check(
    "Two isolated vertices have independent set of size 2 and clique of size 2 in complement",
    ok2,
    explain_ok=f"(expected {want2}, got {got2})",
    explain_bad=f"(expected {want2}, got {got2})",
)

# 3) Two vertices with an edge
G = [
    [0, 1],
    [1, 0],
]
ok3a, want3a, got3a = check_equivalence_IS_to_Clique(G, 2)
check(
    "Two vertices with an edge do not have independent set of size 2",
    ok3a,
    explain_ok=f"(expected {want3a}, got {got3a})",
    explain_bad=f"(expected {want3a}, got {got3a})",
)
ok3b, want3b, got3b = check_equivalence_IS_to_Clique(G, 1)
check(
    "Any nonempty graph has independent set of size 1",
    ok3b,
    explain_ok=f"(expected {want3b}, got {got3b})",
    explain_bad=f"(expected {want3b}, got {got3b})",
)

# 4) Triangle K3
G = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0],
]
ok4a, want4a, got4a = check_equivalence_IS_to_Clique(G, 2)
check(
    "K3 has no independent set of size 2",
    ok4a,
    explain_ok=f"(expected {want4a}, got {got4a})",
    explain_bad=f"(expected {want4a}, got {got4a})",
)
ok4b, want4b, got4b = check_equivalence_IS_to_Clique(G, 1)
check(
    "K3 has independent set of size 1",
    ok4b,
    explain_ok=f"(expected {want4b}, got {got4b})",
    explain_bad=f"(expected {want4b}, got {got4b})",
)

# 5) 4-cycle C4
G = [
    [0, 1, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 1, 0],
]
ok5a, want5a, got5a = check_equivalence_IS_to_Clique(G, 2)
check(
    "C4 has independent set of size 2",
    ok5a,
    explain_ok=f"(expected {want5a}, got {got5a})",
    explain_bad=f"(expected {want5a}, got {got5a})",
)
ok5b, want5b, got5b = check_equivalence_IS_to_Clique(G, 3)
check(
    "C4 does not have independent set of size 3",
    ok5b,
    explain_ok=f"(expected {want5b}, got {got5b})",
    explain_bad=f"(expected {want5b}, got {got5b})",
)

# 6) Complete graph K4
G = [
    [0, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 0],
]
ok6a, want6a, got6a = check_equivalence_IS_to_Clique(G, 2)
check(
    "K4 has no independent set of size 2",
    ok6a,
    explain_ok=f"(expected {want6a}, got {got6a})",
    explain_bad=f"(expected {want6a}, got {got6a})",
)
ok6b, want6b, got6b = check_equivalence_IS_to_Clique(G, 1)
check(
    "K4 has independent set of size 1",
    ok6b,
    explain_ok=f"(expected {want6b}, got {got6b})",
    explain_bad=f"(expected {want6b}, got {got6b})",
)

# 7) Input with self loops should still produce complement with 0 diagonal and correct decision
G = [
    [1, 0, 0],
    [0, 1, 1],
    [0, 1, 1],
]
H = _complement(G)
diag_ok = all(H[i][i] == 0 for i in range(len(H)))
check("Complement diagonal is zero even if input had self loops", diag_ok)

ok7, want7, got7 = check_equivalence_IS_to_Clique(G, 2)
check(
    "Decision equivalence holds when input had self loops",
    ok7,
    explain_ok=f"(expected {want7}, got {got7})",
    explain_bad=f"(expected {want7}, got {got7})",
)

# 8) Symmetry preserved
G = [
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0],
]
H = _complement(G)
sym_ok = all(H[i][j] == H[j][i] for i in range(len(H)) for j in range(len(H)))
check("Complement preserves symmetry on undirected matrices", sym_ok)

print("\n=== Randomized spot checks ===")
random.seed(123)
for idx, (n, k) in enumerate([(5, 2), (5, 3), (6, 3), (7, 3), (7, 4)], start=1):
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            bit = random.randint(0, 1)
            G[i][j] = G[j][i] = bit
    okR, wantR, gotR = check_equivalence_IS_to_Clique(G, k)
    check(
        f"Random graph {idx} on n={n}, k={k}",
        okR,
        explain_ok=f"(expected {wantR}, got {gotR})",
        explain_bad=f"(expected {wantR}, got {gotR})",
    )

print("\n=== Direct clique oracle agreement checks ===")
# Compare your clique(G,k) against a brute force oracle on a few cases
cases = [
    ([[0]], 1),
    ([[0, 1], [1, 0]], 2),
    ([[0, 0], [0, 0]], 2),
    ([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 3),
    ([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]], 3),
]
for idx, (GG, kk) in enumerate(cases, start=1):
    okC, wantC, gotC = check_clique_oracle(GG, kk)
    check(
        f"Clique implementation vs oracle case {idx}",
        okC,
        explain_ok=f"(expected {wantC}, got {gotC})",
        explain_bad=f"(expected {wantC}, got {gotC})",
    )

print("\n=== Summary ===")
print(f"Passed {PASSED} of {TOTAL} tests")
if PASSED == TOTAL:
    print("ALL TESTS PASSED")
else:
    print("SOME TESTS FAILED")
