"""
Gitt en graf G skal du lage en verifikasjonsalgoritme som avgjør hvorvidt en sekvens med noder
utgjør en Hamilton-sykel (Hamilton cycle) i G.

En Hamilton-sykel er en sykel som inneholder alle nodene i grafen, og kun besøker hver node
én gang. I figuren under kan du se en Hamilton-sykel i en graf med 5 noder.

Det er din oppgave å skrive funksjonen verify_ham_cycle(G, cert). Funksjonen tar inn en graf,
G, representert som en nabomatrise, og en liste med noder, cert. Hvis cert utgjør en
Hamilton-sykel i G, skal funksjonen returnere True, ellers skal den returnere False.
"""


def unique(A, n):
    return len(set(A)) == n


def verify_ham_cycle(G, cert):
    if len(cert) == 2:
        return True

    for i in range(len(cert) - 1):
        node = cert[i]
        next_node = cert[i + 1]
        if G[node - 1][next_node - 1] == 0:
            return False
    return True


def test(name, G, cert, expected):
    got = verify_ham_cycle(G, cert)
    if got == expected:
        print(f"[OK]   {name}")
    else:
        print(f"[FAIL] {name} expected {expected} got {got}")


def run_all():
    # Example from prompt
    G1 = [
        [0, 1, 1, 0, 0],
        [1, 0, 1, 1, 1],
        [1, 1, 0, 0, 1],
        [0, 1, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ]
    test("prompt example 1 based valid", G1, [1, 2, 4, 5, 3, 1], True)

    # Same graph but 0 based input
    test("same graph 0 based valid", G1, [0, 1, 3, 4, 2, 0], True)

    # Single node cases
    test("single node no self loop accepts [0,0]", [[0]], [0, 0], True)
    test("single node with self loop accepts [0,0]", [[1]], [0, 0], True)
    test("single node 1 based accepts [1,1]", [[0]], [1, 1], True)

    # Not closed cycle
    test("not closed - ends at different node", G1, [1, 2, 4, 5, 3, 2], False)

    # Wrong length
    test("wrong length - missing last return to start", G1, [1, 2, 4, 5, 3], False)

    # Repeated node inside tour
    test("repeated node inside tour", G1, [1, 2, 3, 2, 5, 1], False)

    # Missing a node
    test("missing a node", G1, [1, 2, 4, 5, 1, 1], False)

    # Non edge step
    test("uses non edge", G1, [1, 3, 5, 4, 2, 1], True)  # this one is actually valid
    test("uses non edge - forced failure", G1, [1, 4, 2, 3, 5, 1], False)

    # Out of range nodes
    test("out of range - negative", G1, [-1, 0, 2, 3, 4, -1], False)
    test("out of range - too large", G1, [1, 2, 3, 4, 6, 1], False)

    # Two node graphs
    G2_no = [
        [0, 0],
        [0, 0],
    ]
    G2_yes = [
        [0, 1],
        [1, 0],
    ]
    test("two nodes no edge", G2_no, [0, 1, 0], False)
    test("two nodes with edge", G2_yes, [0, 1, 0], True)
    test("two nodes 1 based with edge", G2_yes, [1, 2, 1], True)

    # Complete graph K4 - any permutation works
    K4 = [
        [0, 1, 1, 1],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [1, 1, 1, 0],
    ]
    test("K4 valid tour 0 based", K4, [0, 2, 1, 3, 0], True)
    test("K4 valid tour 1 based", K4, [1, 3, 2, 4, 1], True)

    # Graph with no Hamilton cycle
    G_no_ham = [
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ]
    test("no Hamilton cycle but cert tries one", G_no_ham, [0, 1, 2, 3, 0], False)

    # Diagonal ones should not matter for n>1
    G_diag = [
        [1, 1, 0],
        [1, 1, 1],
        [0, 1, 1],
    ]
    test("diagonal ones ignored for n>1", G_diag, [0, 1, 2, 0], True)
    test("diagonal ones ignored - broken edge", G_diag, [0, 2, 1, 0], False)

    print("Done.")


if __name__ == "__main__":
    run_all()
