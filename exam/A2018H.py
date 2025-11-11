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
# Lavest mulig antall elementer i generert instans.
elements_lower = 5
# Høyest mulig antall elementer i generert instans.
elements_upper = 20
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


def solve(rotated_list):
    """
    Finner det største elementet i en rotert sortert liste.

    Args:
        rotated_list: En liste av tall som er sortert, men rotert.
                     Eksempel: [4, 5, 6, 7, 1, 2, 3] er en rotert versjon
                     av [1, 2, 3, 4, 5, 6, 7] hvor breakpointet er mellom 7 og 1.

    Returns:
        Verdien til det største elementet i listen.

    """
    return bisect_rotated(rotated_list, 0, len(rotated_list) - 1)


def bisect_rotated(A, p, r):
    if r - p < 2:
        return max(A[p], A[r])
    q = p + (r - p) // 2
    if A[r] > A[q] and A[r] > A[p]:  # Not rotated
        return A[r]
    elif A[q] > A[r]:  # Breakpoint is in right part
        return bisect_rotated(A, q, r)
    elif A[p] > A[q]:  # Breakpoint is in left part
        return bisect_rotated(A, p, q)


# Hardkodete tester på format: (rotated_list, expected_max_value)
tests = [
    # Ett element
    ([2, 3, 1], 3),
    ([5], 5),
    # To elementer, ikke rotert
    ([1, 2], 2),
    # To elementer, rotert
    ([2, 1], 2),
    # Tre elementer, ikke rotert
    ([1, 2, 3], 3),
    # Tre elementer, rotert en gang
    ([3, 1, 2], 3),
    # Tre elementer, rotert to ganger
    # Fire elementer, ikke rotert
    ([1, 2, 3, 4], 4),
    # Fire elementer, rotert
    ([4, 1, 2, 3], 4),
    ([3, 4, 1, 2], 4),
    ([2, 3, 4, 1], 4),
    # Eksempel fra oppgaven
    ([4, 5, 6, 7, 1, 2, 3], 7),
    # Større eksempel
    ([10, 11, 12, 13, 14, 1, 2, 3, 4, 5], 14),
    # Negative tall
    ([-3, -2, -1, -5, -4], -1),
    # Blandet positive og negative
    ([3, 4, 5, -2, -1, 0, 1, 2], 5),
]


def find_max_bruteforce(rotated_list):
    """
    Brute force løsning for å verifisere korrekthet.
    """
    if not rotated_list:
        return None
    return max(rotated_list)


def rotate_list(sorted_list, k):
    """
    Roterer en sortert liste k posisjoner til høyre.
    """
    if not sorted_list:
        return []
    k = k % len(sorted_list)
    return sorted_list[-k:] + sorted_list[:-k]


def gen_examples(k, el, eu):
    """Generer tilfeldige testinstanser."""
    for _ in range(k):
        n = random.randint(max(1, el), eu)

        # Generer en sortert liste med tilfeldige tall
        sorted_list = sorted([random.randint(-100, 100) for _ in range(n)])

        # Roter listen med tilfeldig antall posisjoner
        rotation = random.randint(0, n - 1)
        rotated_list = rotate_list(sorted_list, rotation)

        # Beregn forventet svar (det største elementet)
        expected = max(sorted_list)

        yield rotated_list, expected


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(
        gen_examples(
            random_tests,
            elements_lower,
            elements_upper,
        )
    )


def get_feedback(student, answer, rotated_list):
    """Gi tilbakemelding på studentens løsning."""
    if not isinstance(student, (int, float)) and student is not None:
        return f"Du returnerte ikke et tall, men {type(student).__name__}"

    # Håndter tom liste
    if not rotated_list:
        if student != answer:
            return f"For tom liste, forventet {answer}, men fikk {student}"
        return None

    if student != answer:
        return (
            f"Feil svar for listen: {rotated_list}\n"
            f"  Ditt svar: {student}\n"
            f"  Forventet: {answer}"
        )

    return None


def print_list(lst):
    """Hjelpefunksjon for å skrive ut liste i lesbart format."""
    if not lst:
        return "[]"
    return "[" + ", ".join(str(x) for x in lst) + "]"


failed = False
for rotated_list, expected_answer in tests:
    student_answer = solve(rotated_list[:])  # Kopier listen
    response = get_feedback(student_answer, expected_answer, rotated_list)

    if response is not None:
        if failed:
            print("-" * 50)
        failed = True
        print(
            f"""
Koden feilet for følgende instans.
Liste: {print_list(rotated_list)}

Ditt svar: {student_answer}
Forventet svar: {expected_answer}
Feilmelding: {response}
"""
        )


if not failed:
    print("Koden fungerte for alle eksempeltestene.")
