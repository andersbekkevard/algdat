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
generate_random_tests = False
# Antall tilfeldige tester som genereres.
random_tests = 10
# Lavest mulig lengde på staven.
n_lower = 5
# Høyest mulig lengde på staven.
n_upper = 20
# Lavest mulig antall priser i prices-listen.
prices_lower = 3
# Høyest mulig antall priser i prices-listen.
prices_upper = 15
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


def solve(n, prices):
    """
    Løs stavkapping-problemet ved hjelp av dynamisk programmering.

    Finn lengdene l_1, ..., l_k der summen av lengder l_1 + ... + l_k er n
    og totalprisen r_n = p_l1 + ... + p_lk er maksimal.

    Args:
        n: Lengden på staven som skal kuttes
        prices: Liste med priser der prices[i] er prisen for lengde i+1

    Returns:
        Maksimal totalpris som kan oppnås
    """
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        for j in range(1, min(len(prices), i) + 1):
            dp[i] = max(dp[i], prices[j - 1] + dp[i - j])
    return dp[n]


def get_feedback(student_answer, expected_answer, n, prices):
    """Gi tilbakemelding på studentens løsning."""
    if not isinstance(student_answer, (int, float)) and student_answer is not None:
        return f"Du returnerte ikke et tall, men {type(student_answer).__name__}"

    if student_answer != expected_answer:
        return (
            f"Feil svar for n={n}, prices={prices}\n"
            f"  Ditt svar: {student_answer}\n"
            f"  Forventet: {expected_answer}"
        )

    return None


# Hardkodete tester på formatet: (n, prices, expected_max_price)
tests = [
    # Enkle tilfeller
    (1, [1], 1),
    (2, [1, 5], 5),
    (3, [1, 5, 8], 8),
    (4, [1, 5, 8, 9], 10),  # 2+2 gir 5+5=10
    (5, [1, 5, 8, 9, 10], 13),  # 2+3 gir 5+8=13
    (6, [1, 5, 8, 9, 10, 17], 17),  # 6 gir 17
    (7, [1, 5, 8, 9, 10, 17, 17], 18),  # 2+5 gir 5+13=18
    (8, [1, 5, 8, 9, 10, 17, 17, 20], 22),  # 2+6 gir 5+17=22
    (9, [1, 5, 8, 9, 10, 17, 17, 20, 24], 25),  # 2+7 gir 5+18=25
    (10, [1, 5, 8, 9, 10, 17, 17, 20, 24, 30], 30),  # 10 gir 30
    # Edge cases
    (1, [5], 5),
    (2, [3, 7], 7),
    (3, [2, 4, 6], 6),
]


def rodcut_naive(n, prices):
    """
    Naiv rekursiv løsning for rod cutting-problemet.
    Brukes for å generere forventede svar i tilfeldige tester.
    """
    if n == 0:
        return 0
    if n > len(prices):
        # Hvis n er større enn antall priser, bruk bare de tilgjengelige lengdene
        max_price = 0
        for i in range(1, min(len(prices), n) + 1):
            max_price = max(max_price, rodcut_naive(n - i, prices) + prices[i - 1])
        return max_price
    return max([rodcut_naive(n - i, prices) + prices[i - 1] for i in range(1, n + 1)])


def generate_random_test():
    """Genererer en tilfeldig test."""
    if seed != 0:
        random.seed(seed)

    n = random.randint(n_lower, n_upper)
    num_prices = random.randint(prices_lower, min(prices_upper, n))

    # Generer tilfeldige priser (sørg for at de er positive)
    prices = [random.randint(1, n * 2) for _ in range(num_prices)]

    # Beregn forventet svar ved hjelp av naive løsning
    expected = rodcut_naive(n, prices)

    return (n, prices, expected)


# Kjør testene
failed = False
all_tests = list(tests)

if generate_random_tests:
    for _ in range(random_tests):
        all_tests.append(generate_random_test())

for i, (n, prices, expected_answer) in enumerate(all_tests, 1):
    student_answer = solve(n, prices[:])  # Kopier prices-listen
    response = get_feedback(student_answer, expected_answer, n, prices)

    if response is not None:
        if failed:
            print("-" * 70)
        failed = True
        print(
            f"""
Test {i} feilet:
n: {n}
prices: {prices}

Ditt svar: {student_answer}
Forventet svar: {expected_answer}
Feilmelding: {response}
"""
        )

if not failed:
    print(f"Koden fungerte for alle {len(all_tests)} testene! ✓")
