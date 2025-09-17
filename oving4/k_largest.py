#!/usr/bin/python3
# coding=utf-8
import random
import numpy as np

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
# Laveste mulige antall tall i generert instans.
numbers_lower = 3
# Høyest mulig antall tall i generert instans.
numbers_upper = 8
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


def partition(A, p, r):
    x = A[r]
    i = p
    for j in range(p, r):
        if A[j] < x:
            A[i], A[j] = A[j], A[i]
            i += 1
    A[i], A[r] = A[r], A[i]
    return i


def rand_partition(A, p, r):
    if p >= r:
        return r
    q = np.random.randint(p, r)
    A[q], A[r] = A[r], A[q]
    return partition(A, p, r)


def rand_select(A, p, r, i):
    if p == r:
        return A[p]
    if p > r:
        return None  # Invalid range
    q = rand_partition(A, p, r)
    k = q - p + 1
    if i == k:
        return A[q]
    elif i < k:
        return rand_select(A, p, q - 1, i)
    else:
        return rand_select(A, q + 1, r, i - k)


def rand_select_index(A, p, r, i):
    if p == r:
        return p
    if p > r:
        return -1  # Invalid range
    q = rand_partition(A, p, r)
    k = q - p + 1
    if i == k:
        return q
    elif i < k:
        return rand_select_index(A, p, q - 1, i)
    else:
        return rand_select_index(A, q + 1, r, i - k)


def k_largest(A, n, k):
    if k == 0:
        return []
    if n <= 1:
        return A
    q = rand_select_index(A, 0, n - 1, n - k)
    return A[q + 1 :]


# Sett med hardkodete tester på format: (A, k)
tests = [
    ([], 0),
    ([1], 0),
    ([1], 1),
    ([1, 2], 1),
    ([-1, -2], 1),
    ([-1, -2, 3], 2),
    ([1, 2, 3], 2),
    ([3, 2, 1], 2),
    ([3, 3, 3, 3], 2),
    ([4, 1, 3, 2, 3], 2),
    ([4, 5, 1, 3, 2, 3], 4),
    ([9, 3, 6, 1, 7, 3, 4, 5], 4),
]


def gen_examples(k, lower, upper):
    for _ in range(k):
        A = [random.randint(-50, 50) for _ in range(random.randint(lower, upper))]
        yield A, random.randint(0, len(A))


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(
        gen_examples(
            random_tests,
            numbers_lower,
            numbers_upper,
        )
    )

failed = False
for A, k in tests:
    answer = sorted(A, reverse=True)[:k][::-1]
    student = k_largest(A[:], len(A), k)

    if type(student) != list:
        if failed:
            print("-" * 50)
        failed = True
        print(
            f"""
Koden feilet for følgende instans:
A: {A}
n: {len(A)}
k: {k}

Metoden må returnere en liste
Ditt svar: {student}
"""
        )
    else:
        student.sort()
        if student != answer:
            if failed:
                print("-" * 50)
            failed = True
            print(
                f"""
Koden feilet for følgende instans:
A: {A}
n: {len(A)}
k: {k}

Ditt svar: {student}
Riktig svar: {answer}
"""
            )

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")
