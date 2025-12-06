#!/usr/bin/python3
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
generate_random_tests = True
# Antall tilfeldige tester som genereres.
random_tests = 10
# Lavest mulig antall elementer i A og B.
elements_lower = 3
# Høyest mulig antall elementer i A og B.
elements_upper = 10
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 42


def solve(A, B, X):
    """
    IMPLEMENT ME: Returner True dersom X er en sammenfletting av A og B, ellers False.
    """
    raise NotImplementedError("Implementer sammenflettings-sjekken her.")


def get_feedback(student_answer, expected_answer, A, B, X):
    if student_answer == expected_answer:
        return None

    if expected_answer:
        return f"X skulle vært en sammenfletting av A og B, men algoritmen returnerte False"
    else:
        return f"X er ikke en sammenfletting av A og B, men algoritmen returnerte True"


# Hardkodete tester på format: (A, B, X, expected_result)
tests = [
    # Enkle tilfeller
    ([1, 2, 3], [4, 5], [1, 2, 3, 4, 5], True, "A først, deretter B"),
    ([1, 2, 3], [4, 5], [4, 5, 1, 2, 3], True, "B først, deretter A"),
    ([1, 2, 3], [4, 5], [1, 2, 4, 3, 5], True, "Deling av A og B"),
    ([1, 2, 3], [4, 5], [1, 4, 2, 5, 3], True, "Alternerende"),
    # Negative tilfeller
    ([1, 2, 3], [4, 5], [1, 3, 2, 4, 5], False, "Feil rekkefølge i A (3 før 2)"),
    ([1, 2, 3], [4, 5], [1, 2, 3, 4, 4], False, "Feil element - 4 i stedet for 5"),
    ([1, 2, 3], [4, 5], [1, 2, 2, 4, 5], False, "Duplikat element - ekstra 2"),
    ([1, 2, 3], [4, 5], [1, 2, 3, 5, 4], False, "Feil rekkefølge i B (5 før 4)"),
    # Edge cases
    ([], [], [], True, "Tomme sekvenser"),
    ([1], [], [1], True, "B er tom"),
    ([], [1], [1], True, "A er tom"),
    ([1, 2], [3], [1, 2, 3], True, "En av sekvensene har ett element"),
    # Duplikater
    ([1, 1, 2], [1, 2], [1, 1, 1, 2, 2], True, "Duplikater - gyldig"),
    ([1, 1, 2], [1, 2], [1, 1, 2, 1, 2], True, "Duplikater - gyldig alternativ"),
    ([1, 1, 2], [1, 2], [1, 2, 1, 1, 2], True, "Duplikater - gyldig alternativ 2"),
    # Lengre sekvenser
    ([1, 2, 3, 4, 5], [6, 7, 8], [1, 2, 6, 3, 7, 4, 8, 5], True, "Lengre sekvenser"),
    ([1, 2, 3, 4], [5, 6, 7, 8], [1, 5, 2, 6, 3, 7, 4, 8], True, "Perfekt alternering"),
]


def generate_random_test():
    """Genererer en tilfeldig test."""
    if seed != 0:
        random.seed(seed)

    m = random.randint(elements_lower, elements_upper)
    n = random.randint(elements_lower, elements_upper)

    # Generer A og B med tilfeldige verdier
    A = [random.randint(1, 10) for _ in range(m)]
    B = [random.randint(1, 10) for _ in range(n)]

    # Bestem om vi skal lage en gyldig eller ugyldig sammenfletting
    is_valid = random.choice([True, False])

    if is_valid:
        # Lag en gyldig sammenfletting
        X = []
        i, j = 0, 0
        while i < m or j < n:
            if i < m and (j >= n or random.choice([True, False])):
                X.append(A[i])
                i += 1
            else:
                X.append(B[j])
                j += 1
        expected = True
    else:
        # Lag en ugyldig sammenfletting
        # Strategi: Enten endre lengden eller reverser en del av sekvensen
        choice = random.randint(1, 3)

        if choice == 1:
            # Fjern et tilfeldig element (feil lengde)
            X = []
            i, j = 0, 0
            while i < m or j < n:
                if i < m and (j >= n or random.choice([True, False])):
                    X.append(A[i])
                    i += 1
                else:
                    X.append(B[j])
                    j += 1
            if len(X) > 0:
                X.pop(random.randint(0, len(X) - 1))
        elif choice == 2:
            # Legg til et ekstra element (feil lengde)
            X = []
            i, j = 0, 0
            while i < m or j < n:
                if i < m and (j >= n or random.choice([True, False])):
                    X.append(A[i])
                    i += 1
                else:
                    X.append(B[j])
                    j += 1
            X.append(random.randint(1, 10))
        else:
            # Reverser en del av sekvensen (ødelegger rekkefølge)
            X = []
            i, j = 0, 0
            while i < m or j < n:
                if i < m and (j >= n or random.choice([True, False])):
                    X.append(A[i])
                    i += 1
                else:
                    X.append(B[j])
                    j += 1
            if len(X) >= 3:
                start = random.randint(0, len(X) - 3)
                end = random.randint(start + 2, len(X))
                X[start:end] = reversed(X[start:end])
        expected = False

    return (A, B, X, expected, f"Tilfeldig test (m={m}, n={n}, valid={is_valid})")


def print_sequences(A, B, X):
    """Formatterer sekvensene for utskrift."""
    return f"A = {A}, B = {B}, X = {X}"


# Kjør testene
failed = False
all_tests = list(tests)

if generate_random_tests:
    for _ in range(random_tests):
        all_tests.append(generate_random_test())

for i, (A, B, X, expected_answer, description) in enumerate(all_tests, 1):
    student_answer = solve(A[:], B[:], X[:])  # Kopier listene
    response = get_feedback(student_answer, expected_answer, A, B, X)

    if response is not None:
        if failed:
            print("-" * 70)
        failed = True
        print(
            f"""
Test {i} feilet: {description}
{print_sequences(A, B, X)}

Ditt svar: {student_answer}
Forventet svar: {expected_answer}
Feilmelding: {response}
"""
        )

if not failed:
    print(f"Koden fungerte for alle {len(all_tests)} testene! ✓")
