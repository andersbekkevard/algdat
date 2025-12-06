#!/usr/bin/python3
# coding=utf-8
import random

# Lokale testparametere (samme stil som andre exam-filer)
generate_random_tests = True
random_tests = 8
elements_lower = 2
elements_upper = 8
seed = 7  # Sett til 0 for ferske tilfeldige instanser hver gang


def solve(A, B, X):
    dp = [
        [[False] * (len(B) + 1) for _ in range(len(A) + 1)] for _ in range(len(X) + 1)
    ]
    dp[0][0][0] = True
    for k in range(1, len(X) + 1):
        for i in range(k + 1):
            j = k - i
            if i > len(A) or j > len(B):
                continue

            if i > 0 and dp[k - 1][i - 1][j] and X[k - 1] == A[i - 1]:
                dp[k][i][j] = True

            if j > 0 and dp[k - 1][i][j - 1] and X[k - 1] == B[j - 1]:
                dp[k][i][j] = True

    return dp[len(X)][len(A)][len(B)]


def get_feedback(student_answer, expected_answer, A, B, X):
    if student_answer == expected_answer:
        return None
    if expected_answer:
        return "X er en gyldig sammenfletting, men algoritmen returnerte False."
    return "X er ikke en gyldig sammenfletting, men algoritmen returnerte True."


# Hardkodete tester: (A, B, X, expected, description)
tests = [
    # Grunnleggende
    ([1, 2, 3], [4, 5], [1, 2, 3, 4, 5], True, "A før B"),
    ([1, 2, 3], [4, 5], [4, 5, 1, 2, 3], True, "B før A"),
    ([1, 2, 3], [4, 5], [1, 4, 2, 5, 3], True, "Alternering"),
    ([1, 2, 3], [4, 5], [1, 2, 4, 3, 5], True, "Split A"),
    # Negativ med brutt rekkefølge
    ([1, 2, 3], [4, 5], [1, 3, 2, 4, 5], False, "Feil rekkefølge i A"),
    ([1, 2, 3], [4, 5], [1, 2, 3, 5, 4], False, "Feil rekkefølge i B"),
    # Lengdefeil
    ([1, 2], [3], [1, 2], False, "For kort"),
    ([1, 2], [3], [1, 2, 3, 4], False, "For lang"),
    # Duplikater og tvetydige valg
    ([1, 1, 2], [1, 2], [1, 1, 1, 2, 2], True, "Duplikater - gyldig"),
    ([1, 1, 2], [1, 2], [1, 2, 1, 1, 2], True, "Duplikater - gyldig 2"),
    ([1, 1, 2], [1, 2], [1, 2, 2, 1, 1], False, "Duplikater - feil rekkefølge"),
    # Edge cases
    ([], [], [], True, "Tomme lister"),
    ([], [1, 2], [1, 2], True, "A tom"),
    ([1, 2], [], [1, 2], True, "B tom"),
]


def generate_random_test():
    """Lag en tilfeldig gyldig eller ugyldig instans."""
    if seed != 0:
        random.seed(seed)

    m = random.randint(elements_lower, elements_upper)
    n = random.randint(elements_lower, elements_upper)
    A = [random.randint(0, 5) for _ in range(m)]
    B = [random.randint(0, 5) for _ in range(n)]

    make_valid = random.choice([True, False])
    if make_valid:
        # Flett A og B til en gyldig X
        X = []
        i = j = 0
        while i < m or j < n:
            pick_A = i < m and (j >= n or random.choice([True, False]))
            if pick_A:
                X.append(A[i])
                i += 1
            else:
                X.append(B[j])
                j += 1
        expected = True
        desc = f"Tilfeldig gyldig (m={m}, n={n})"
    else:
        # Start fra en gyldig X og ødelegg den
        X = []
        i = j = 0
        while i < m or j < n:
            if i < m and (j >= n or random.choice([True, False])):
                X.append(A[i])
                i += 1
            else:
                X.append(B[j])
                j += 1

        choice = random.randint(1, 3)
        if choice == 1 and X:
            # Fjern et element
            X.pop(random.randrange(len(X)))
            desc = "Tilfeldig ugyldig (fjernet element)"
        elif choice == 2:
            # Legg til ekstra element
            X.insert(random.randrange(len(X) + 1), random.randint(0, 5))
            desc = "Tilfeldig ugyldig (ekstra element)"
        else:
            # Reverser en midtre subsekvens for å bryte rekkefølge
            if len(X) >= 3:
                start = random.randint(0, len(X) - 3)
                end = random.randint(start + 2, len(X))
                X[start:end] = reversed(X[start:end])
            desc = "Tilfeldig ugyldig (rekkefølge brutt)"
        expected = False

    return A, B, X, expected, desc


def print_sequences(A, B, X):
    return f"A={A}, B={B}, X={X}"


if __name__ == "__main__":
    failed = False
    all_tests = list(tests)

    if generate_random_tests:
        for _ in range(random_tests):
            all_tests.append(generate_random_test())

    for i, (A, B, X, expected, desc) in enumerate(all_tests, 1):
        student_answer = solve(A[:], B[:], X[:])
        feedback = get_feedback(student_answer, expected, A, B, X)
        if feedback is not None:
            if failed:
                print("-" * 70)
            failed = True
            print(
                f"""
Test {i} feilet: {desc}
{print_sequences(A, B, X)}

Ditt svar: {student_answer}
Forventet: {expected}
Feilmelding: {feedback}
"""
            )

    if not failed:
        print(f"Koden fungerte for alle {len(all_tests)} testene! ✓")
