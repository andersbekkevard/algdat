"""

Anta at vi har en lesesal som er helt fylt opp av studenter. Hver student har en favorittplass
i lesesalen og ønsker å flytte ditt, om de ikke allerede sitter på denne plassen. Siden det er
tar litt tid å bytte plass, er hver student kun villig til å flytte til en annen plass om de
får favorittplassen sin. For å gjøre så mange som mulig fornøyde ønsker vi å finne en
maksimal delmengde av studenter, slik at alle disse kan reise seg opp og bytte til
favorittplassen sin.

I denne oppgaven skal du implementere funksjonen max_permutations. Denne tar inn en liste M
over favorittplassene til studentene. Tallet på plass i i listen, M[i], indikerer at studenten
som sitter på plass i har favorittplass M[i]. Funksjonen skal returnere en mengde (set) av
studenter som kan reise seg opp og bytte plass, slik at alle får favorittplassen sin.
Mengden skal inneholde flest mulig studenter, men ingen som allerede sitter på favorittplassen
sin.

For eksempel, om M = [2, 0, 1, 1, 5, 4, 6] skal funksjonen returnere {0, 1, 2, 4, 5}.
Dette siden studentene på plassene 0, 1 og 2 kan bytte plasser seg i mellom og studentene
på plassene 4 og 5 kan bytte seg i mellom. Studentene på plass 2 og 3 har begge samme
favorittplass, så begge kan ikke være med i løsningen. Studenten på plass 6 sitter allerede
på favorittplassen sin og skal ikke være med i løsningen.

"""

"""
Tanker:
- Hvordan modellere rekursjon (?), hashmaps ble tricky

Metode:
- Fjerner alle som sitter på riktig plass
- For hver av deres plasser, fjerner vi alle som ønsker å sitte der
Nå har vi forenklet problemet vårt
- Finner alle konfliktfylte plasser (plasser to ønsker seg)
- Løser problemet rekursivt to steder: Fjerner en konfliktskaper for hver. Velger settet med flest medlemmer
Returnerer
"""


def max_permutations(M):
    solved_seats = {i for i in range(len(M)) if M[i] == i}
    # Finner alle på riktige plasser
    considering = [M[i] not in solved_seats for i in range(len(M))]
    # Fjerner alle som vil på en slik plass
    for i in range(len(M)):
        if not considering[i]:
            continue
        if M[i] in solved_seats:
            considering[i] = False

    return solve(M, considering)


def solve(M, considering):
    for i in range(len(M)):
        if not considering[M[i]]:
            considering[i] = False

    to_consider = [M[i] for i in range(len(M)) if considering[i]]
    duplicates = set([item for item in to_consider if to_consider.count(item) > 1])

    if len(duplicates) == 0:
        return set([i for i in range(len(M)) if considering[i]])

    best_set = set()
    for dupe in duplicates:
        for i in range(len(M)):
            if not considering[i]:
                continue
            if M[i] == dupe:
                new_considering = considering.copy()
                new_considering[i] = False
                possible_set = solve(M, new_considering)
                if len(possible_set) > len(best_set):
                    best_set = possible_set
    return best_set


# def max_permutations_with_map(M):
#     if len(M) == 0:
#         return set(M)

#     map = {i: M[i] for i in range(len(M))}

#     # Ønsker å fjerne alle på riktig plass:
#     # 1. Finner alle slike verdier
#     solved_vals = {v for k, v in map.items() if k == v}
#     # 2. Fjerner alle par med en verdi fra solved_vals
#     map = {k: v for k, v in map.items() if v not in solved_vals}

#     # Hvis det nå finnes duplikater løser vi disse rekursivt


def test_max_permutations():
    """Test cases for max_permutations function"""

    # Test case 1: Example from problem description
    M1 = [2, 0, 1, 1, 5, 4, 6]
    expected1 = {0, 1, 2, 4, 5}
    result1 = max_permutations(M1)
    print(f"Test 1: M = {M1}")
    print(f"Expected: {expected1}, Got: {result1}")
    print(f"Pass: {result1 == expected1}")
    print()

    # Test case 2: All students already in correct positions
    M2 = [0, 1, 2, 3, 4]
    expected2 = set()
    result2 = max_permutations(M2)
    print(f"Test 2: M = {M2}")
    print(f"Expected: {expected2}, Got: {result2}")
    print(f"Pass: {result2 == expected2}")
    print()

    # Test case 3: Simple swap (2 students)
    M3 = [1, 0]
    expected3 = {0, 1}
    result3 = max_permutations(M3)
    print(f"Test 3: M = {M3}")
    print(f"Expected: {expected3}, Got: {result3}")
    print(f"Pass: {result3 == expected3}")
    print()

    # Test case 4: Three-way cycle
    M4 = [1, 2, 0]
    expected4 = {0, 1, 2}
    result4 = max_permutations(M4)
    print(f"Test 4: M = {M4}")
    print(f"Expected: {expected4}, Got: {result4}")
    print(f"Pass: {result4 == expected4}")
    print()

    # Test case 5: Single student
    M5 = [0]
    expected5 = set()
    result5 = max_permutations(M5)
    print(f"Test 5: M = {M5}")
    print(f"Expected: {expected5}, Got: {result5}")
    print(f"Pass: {result5 == expected5}")
    print()

    # Test case 6: Empty list
    M6 = []
    expected6 = set()
    result6 = max_permutations(M6)
    print(f"Test 6: M = {M6}")
    print(f"Expected: {expected6}, Got: {result6}")
    print(f"Pass: {result6 == expected6}")
    print()

    # Test case 7: Multiple conflicts - choose largest set
    M7 = [1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # Students 0,1 can swap, students 2,3,4,5,6,7,8,9 can form a cycle
    # Should choose the larger set
    expected7 = {2, 3, 4, 5, 6, 7, 8, 9}
    result7 = max_permutations(M7)
    print(f"Test 7: M = {M7}")
    print(f"Expected: {expected7}, Got: {result7}")
    print(f"Pass: {result7 == expected7}")
    print()

    # Test case 8: Complex case with multiple cycles and conflicts
    M8 = [1, 2, 0, 4, 3, 6, 5, 7, 8, 9, 10, 11]
    # Cycle 1: 0->1->2->0 (3 students)
    # Cycle 2: 3->4->3 (2 students)
    # Cycle 3: 5->6->5 (2 students)
    # Students 7,8,9,10,11 already in correct positions
    expected8 = {0, 1, 2, 3, 4, 5, 6}  # All cycles combined
    result8 = max_permutations(M8)
    print(f"Test 8: M = {M8}")
    print(f"Expected: {expected8}, Got: {result8}")
    print(f"Pass: {result8 == expected8}")
    print()

    # Test case 9: All students want the same seat (impossible)
    M9 = [0, 0, 0, 0]
    expected9 = set()  # No valid swaps possible
    result9 = max_permutations(M9)
    print(f"Test 9: M = {M9}")
    print(f"Expected: {expected9}, Got: {result9}")
    print(f"Pass: {result9 == expected9}")
    print()

    # Test case 10: Two students want same seat, others can swap
    M10 = [1, 0, 1, 3, 2]
    # Students 0,1 can swap (2 students)
    # Students 2,3,4 can form cycle (3 students) - but student 2 conflicts with student 0
    # Should choose the larger valid set
    expected10 = {2, 3, 4}  # The 3-student cycle
    result10 = max_permutations(M10)
    print(f"Test 10: M = {M10}")
    print(f"Expected: {expected10}, Got: {result10}")
    print(f"Pass: {result10 == expected10}")
    print()


from typing import List, Set


# ---------- Fasit ----------


def _truth_max_permutations(M: List[int]) -> Set[int]:
    """
    Unionen av alle sykler med lengde minst 2 i funksjonsgrafen i -> M[i].
    Selvsløyfer ekskluderes.
    """
    n = len(M)
    color = [0] * n  # 0=unseen, 1=visiting, 2=done
    stack_pos = [-1] * n
    stack = []
    res = set()

    def dfs(u: int):
        color[u] = 1
        stack_pos[u] = len(stack)
        stack.append(u)
        v = M[u]
        if color[v] == 0:
            dfs(v)
        elif color[v] == 1:
            start = stack_pos[v]
            cycle = stack[start:]
            if len(cycle) >= 2:
                res.update(cycle)
        stack.pop()
        stack_pos[u] = -1
        color[u] = 2

    for i in range(n):
        if color[i] == 0:
            dfs(i)
    return res


def _valid_solution(M: List[int], S: Set[int]) -> bool:
    if any(M[i] == i for i in S):
        return False
    if any(M[i] not in S for i in S):
        return False
    return {M[i] for i in S} == S


def run_one_test(name: str, M: List[int], expected: Set[int]):
    # Verifiser at forventet fasit faktisk er korrekt i henhold til definisjonen
    truth = _truth_max_permutations(M)
    if expected != truth:
        print(f"[ADVARSEL] Testsettet for '{name}' er ikke konsistent med fasit")
        print(f"  M: {M}")
        print(f"  Forventet: {sorted(expected)}")
        print(f"  Fasit:     {sorted(truth)}")
        print("  Avbryter for å sikre korrekte tester.")
        raise SystemExit(1)

    try:
        got = max_permutations(M.copy())
    except NotImplementedError as e:
        print(f"[{name}] NotImplementedError: {e}")
        return

    ok_shape = _valid_solution(M, got)
    ok_optimal = got == expected
    status = "PASS" if ok_shape and ok_optimal else "FAIL"

    print(f"Test: {name}")
    print(f"Input M: {M}")
    print(f"Forventet: {sorted(expected)}")
    print(f"Fikk:      {sorted(got)}")
    print(f"Gyldig permutasjon: {ok_shape}")
    print(f"Korrekt maksimum: {ok_optimal}")
    print(f"Resultat: {status}")
    print("-" * 60)


# ---------- Deterministiske tester ----------


def deterministic_tests():
    tests = [
        # 1. Oppgavens eksempel
        ("Oppgavens eksempel", [2, 0, 1, 1, 5, 4, 6], {0, 1, 2, 4, 5}),
        # 2. Alle selvsløyfer
        ("Alle selvsløyfe", [0, 1, 2, 3], set()),
        # 3. 2-syklus med haler inn
        ("2-syklus med haler", [1, 0, 1, 2, 3], {0, 1}),
        # 4. To disjunkte sykler
        ("To disjunkte sykler 2 og 3", [1, 0, 3, 4, 2, 5], {0, 1, 2, 3, 4}),
        # 5. Stjerne uten syklus
        ("Stjerne uten syklus", [1, 1, 1, 1], set()),
        # 6. Ren 3-syklus
        ("Ren 3-syklus", [1, 2, 0], {0, 1, 2}),
        # 7. 3-syklus med haler
        ("3-syklus med haler", [1, 2, 0, 2, 3], {0, 1, 2}),
        # 8. To 2-sykler og en selvsløyfe
        ("To 2-sykler og selvsløyfe", [1, 0, 3, 2, 4], {0, 1, 2, 3}),
        # 9. Begge peker til samme favoritt som er selvsløyfe
        ("Alle til selvsløyfe, ingen syklus>=2", [1, 1], set()),
        # 10. Duplikat mot en 2-syklus
        ("Duplikat inn i 2-syklus", [1, 0, 0], {0, 1}),
    ]

    for name, M, expected in tests:
        run_one_test(name, M, expected)


if __name__ == "__main__":
    print("Starter deterministiske tester for max_permutations")
    print("=" * 60)
    deterministic_tests()
    print("Ferdig.")
    M = [2, 0, 1, 1, 5, 4, 6]
    print("actual=", max_permutations(M), ", expected=", {0, 1, 2, 4, 5})
