#!/usr/bin/python3
# coding=utf-8
import random
from string import ascii_lowercase

# region Comments
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
# Laveste mulige antall strenger i generert instans.
n_strings_lower = 3
# Høyest mulig antall strenger i generert instans.
n_strings_upper = 8
# Laveste mulige antall tegn i hver streng i generert instans.
n_chars_lower = 3
# Høyest mulig antall tegn i hver streng i generert instans.
n_chars_upper = 15
# Antall forskjellige bokstaver som kan brukes i strengene. Må være mellom 1 og
# 26. Plukker de første `n_diff_chars` bokstavene i alfabetet.
n_diff_chars = 5
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0
# endregion


def char_to_int(char):
    return ord(char) - 97


def counting_sort_by_char(A, n, c):
    """
    A: list of integers
    n: length of A
    c: character index (0 = leftmost)
    """
    B, C = [0] * n, [0] * 26  # 26 characters in the english alphabet
    # Count occurrences
    for i in range(n):
        C[char_to_int(A[i][c])] = C[char_to_int(A[i][c])] + 1
    # Make cumulative
    for i in range(1, 26):
        C[i] = C[i] + C[i - 1]
    # Place elements
    for i in range(n - 1, -1, -1):
        val = A[i][c]
        B[C[val] - 1] = A[i]
        C[val] = C[val] - 1
    return B


def sort_by_length(A, n, d):
    """
    Problemet er mye lettere å løse dersom jeg har navnene sortert etter lengde
    Det er fordi:
    Anta sortert slik at korte navn til venstre, lange til høyre.
    Sorterer på LSB med radix sort. Bruker her en counting sort som heller teller fra høyre til venstre.
    Ved første len < digit_index så breaker vi og husker denne indeksen.
    Kan dermed sortere bare elementer som er lange nok
    """
    B, C = [None] * n, [0] * d
    # Teller antall per lengde
    for i in range(n):
        length = len(A[i])
        C[length - 1] = C[length - 1] + 1
    # Gjør kumulativ
    for i in range(1, d):
        C[i] = C[i - 1] + C[i]
    # Sorterer
    for i in range(n - 1, -1, -1):
        length = len(A[i])
        B[C[length - 1] - 1] = A[i]
        C[length - 1] = C[length - 1] - 1
    return B


def dynamic_counting_sort(A, n, c):
    """
    A = listen (sortert med korteste strenger først)
    n = lengden av listen
    c = indeksen til den bokstaven vi skal sortere på

    Husk: Denne må telle fra høyre til venstre. Stopper når strengene er for korte
    """
    B = A[:]
    C = [0] * 26  # 26 bokstaver i alfabetet
    p = -1
    for i in range(n - 1, -1, -1):
        if len(A[i]) <= c:
            p = i  # p er indeks på første element som ikke er telt i C
            break
        C[char_to_int(A[i][c])] = C[char_to_int(A[i][c])] + 1

    for i in range(1, 26):
        C[i] = C[i] + C[i - 1]

    for i in range(n - 1, p, -1):
        val = char_to_int(A[i][c])
        B[p + C[val]] = A[i]
        C[val] = C[val] - 1
    return B


def flexradix(A, n, d):
    # A = sort_by_length(A, n, d)
    # for i in range(d - 1, -1, -1):
    #     A = dynamic_counting_sort(A, n, i)
    # return A
    d_observed = max(map(len, A)) if A else 0
    if n == 0 or d_observed == 0:
        return A
    A = sort_by_length(A, n, d_observed)
    for i in range(d_observed - 1, -1, -1):
        A = dynamic_counting_sort(A, n, i)
    return A


def test_flexradix():
    # Hardkodete instanser på format: (A, d)
    tests = [
        ([], 1),
        (["a"], 1),
        (["a", "b"], 1),
        (["b", "a"], 1),
        (["a", "z"], 1),
        (["z", "a"], 1),
        (["ba", "ab"], 2),
        (["b", "ab"], 2),
        (["ab", "a"], 2),
        (["zb", "za"], 2),
        (["abc", "b"], 3),
        (["xyz", "y"], 3),
        (["abc", "b"], 4),
        (["xyz", "y"], 4),
        (["zyxy", "yxz"], 4),
        (["ab", "aaa"], 3),
        (["abc", "b", "bbbb"], 4),
        (["abcd", "abcd", "bbbb"], 4),
        (["abcd", "wxyz", "bbbb"], 4),
        (["abcd", "wxyz", "bazy"], 4),
        (["ab", "aab", "aaab", "aaaab", "aaaaab"], 6),
        (["a", "b", "c", "babcbababa"], 10),
        (["a", "b", "c", "babcbababa"], 10),
        (["w", "x", "y", "xxyzxyzxyz"], 10),
        (["b", "a", "y", "xxyzxyzxyz"], 10),
        (["jfiqdopvak", "nzvoquirej", "jfibopvmcq"], 10),
    ]

    def gen_examples(k, nsl, nsu, ncl, ncu):
        for _ in range(k):
            strings = [
                "".join(random.choices(ascii_lowercase, k=random.randint(ncl, ncu)))
                for _ in range(random.randint(nsl, nsu))
            ]
            yield (strings, max(map(len, strings)))

    if generate_random_tests:
        global ascii_lowercase
        ascii_lowercase = ascii_lowercase[:n_diff_chars]
        if seed:
            random.seed(seed)
        tests += list(
            gen_examples(
                random_tests,
                n_strings_lower,
                n_strings_upper,
                n_chars_lower,
                n_chars_upper,
            )
        )

    failed = False
    for A, d in tests:
        answer = sorted(A)
        student = flexradix(A[:], len(A), d)
        if student != answer:
            if failed:
                print("-" * 50)
            failed = True

            print(
                f"""
    Koden feilet for følgende instans:
    A: {A}
    n: {len(A)}
    d: {d}

    Ditt svar: {student}
    Riktig svar: {answer}
    """
            )

    if not failed:
        print("Koden ga riktig svar for alle eksempeltestene")


test_flexradix()
