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
generate_random_tests = True
# Antall tilfeldige tester som genereres.
random_tests = 100
# Lavest mulig antall mynter i generert instans (må være partall).
coins_lower = 2
# Høyest mulig antall mynter i generert instans (må være partall).
coins_upper = 20
# Lavest mulig verdi på en mynt.
value_lower = 1
# Høyest mulig verdi på en mynt.
value_upper = 100
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


def solve(coins):
    """
    Du har en rad v1, ..., vn med mynter, der n er et partall.
    Du og en motspiller skal, annenhver gang, forsyne dere med
    enten den første eller siste mynten av dem som er igjen.

    Finn ut hvor mye du kan være garantert å vinne, dersom du begynner.
    Motspilleren spiller også optimalt.

    Args:
        coins: Liste med myntverdier [v1, v2, ..., vn] der n er partall.
               Eksempel: [5, 3, 7, 10] betyr fire mynter med verdier 5, 3, 7, 10.

    Returns:
        Den maksimale summen du kan garantert vinne som første spiller.

    Eksempel:
        coins = [8, 15, 3, 7]

        Hvis du tar 8 først, kan motspiller ta 7, da tar du 15, motspiller tar 3.
        Du får: 8 + 15 = 23, motspiller får: 7 + 3 = 10.

        Hvis du tar 7 først, kan motspiller ta 8, da tar du 15, motspiller tar 3.
        Du får: 7 + 15 = 22, motspiller får: 8 + 3 = 11.

        Beste strategi gir deg 22 (eller 23 avhengig av motspillers valg).

    Hint:
        Dette er et klassisk dynamisk programmeringsproblem.
        La dp[i][j] være den maksimale verdien første spiller kan oppnå
        fra delproblemet med mynter fra indeks i til j.

        Tenk på hva som skjer når du velger venstre vs høyre mynt,
        og husk at motspilleren også spiller optimalt.
    """
    n = len(coins)
    # dp[p, d] hvor d er distanse til siste inkluderte mynt og p er peker til første
    dp = [[0] * n for _ in range(n)]
    for d in range(1, n):
        for p in range(n):
            if p + d >= n:
                continue

            if d % 2 == 1:  # Partall mynter, min tur
                dp[p][d] = max(coins[p] + dp[p + 1][d - 1], coins[p + d] + dp[p][d - 1])

            else:  # Oddetall mynter, deres tur
                dp[p][d] = min(dp[p + 1][d - 1], dp[p][d - 1])

    return dp[0][n - 1]


# Hardkodete tester på format: (coins, expected_max_guaranteed_win)
tests = [
    # Enkle tilfeller med 2 mynter
    ([1, 2], 2),  # Velg den største
    ([5, 5], 5),  # Begge like
    ([10, 1], 10),  # Velg venstre
    ([1, 10], 10),  # Velg høyre
    # Fire mynter
    ([8, 15, 3, 7], 22),  # Klassisk eksempel
    ([1, 2, 3, 4], 6),  # 4 + 2 = 6 (velg 4, motspiller tar 1, velg 3, motspiller tar 2)
    ([4, 3, 2, 1], 6),  # Symmetrisk
    ([5, 3, 7, 10], 15),  # 5 + 10 = 15 eller 10 + 5 = 15
    ([20, 30, 2, 2, 2, 10], 42),  # Seks mynter
    # Like verdier
    ([5, 5, 5, 5], 10),  # Alle like, hver får halvparten
    ([1, 1, 1, 1, 1, 1], 3),  # Seks enere
    # Ekstreme verdier
    ([100, 1, 1, 1, 1, 100], 102),  # Store på kantene
    ([1, 1, 1, 100, 1, 1], 102),  # Stor i midten
    # Større eksempler
    ([3, 9, 1, 2], 11),  # Ta 2, motsp tar 3, ta 9, motsp tar 1 -> 2+9=11
    ([2, 1, 9, 3], 11),  # Symmetrisk
    # To mynter med ulike verdier
    ([7, 3], 7),
    ([3, 7], 7),
]


def coin_game_bruteforce(coins):
    """
    Brute force løsning med minimax.
    Brukes for å verifisere korrekthet i tilfeldige tester.
    """
    n = len(coins)
    if n == 0:
        return 0

    # Memoization cache
    cache = {}

    def max_value(i, j, is_my_turn):
        """
        Returnerer (min_verdi, maks_verdi) som spiller 1 kan oppnå
        fra mynter[i..j] gitt hvem sin tur det er.
        """
        if i > j:
            return 0

        if (i, j, is_my_turn) in cache:
            return cache[(i, j, is_my_turn)]

        if is_my_turn:
            # Min tur: velg den som maksimerer min gevinst
            take_left = coins[i] + max_value(i + 1, j, False)
            take_right = coins[j] + max_value(i, j - 1, False)
            result = max(take_left, take_right)
        else:
            # Motspillers tur: de velger det som minimerer min gevinst
            # (motspiller spiller optimalt for seg selv)
            take_left = max_value(i + 1, j, True)  # Motspiller tar venstre
            take_right = max_value(i, j - 1, True)  # Motspiller tar høyre
            result = min(take_left, take_right)

        cache[(i, j, is_my_turn)] = result
        return result

    return max_value(0, n - 1, True)


def coin_game_dp(coins):
    """
    Effektiv DP-løsning for myntspillet.
    Brukes som fasit for testing.

    dp[i][j] = maksimal verdi første spiller kan oppnå fra coins[i..j]
    """
    n = len(coins)
    if n == 0:
        return 0

    # dp[i][j] representerer beste mulige utfall for spiller som skal velge
    # fra coins[i..j] (relativt til hva de selv får)
    dp = [[0] * n for _ in range(n)]

    # Basetilfelle: ett element
    for i in range(n):
        dp[i][i] = coins[i]

    # Fyll inn diagonalt (økende lengde på intervall)
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            # Hvis jeg tar coins[i], får jeg coins[i] og motspiller velger optimalt fra [i+1..j]
            # Summen av coins[i+1..j] er total - coins[i], og motspiller får dp[i+1][j] av dette
            # Så jeg får: coins[i] + (sum[i+1..j] - dp[i+1][j])

            # Alternativ: bruk formelen direkte
            # Når jeg velger, velger jeg max, når motspiller velger, velger de min (for meg)

            # Ta venstre: jeg får coins[i], så er det motspillers tur på [i+1..j]
            # Ta høyre: jeg får coins[j], så er det motspillers tur på [i..j-1]

            # Motspiller vil velge det som gir dem selv mest, som betyr minst for meg
            # Etter at motspiller velger fra [i+1..j], får jeg det som er igjen

            # Enklere formulering:
            # dp[i][j] = max(coins[i] + min(dp[i+2][j], dp[i+1][j-1]),
            #                coins[j] + min(dp[i+1][j-1], dp[i][j-2]))

            # Hvis jeg tar coins[i]:
            #   Motspiller kan ta coins[i+1] -> jeg spiller videre på [i+2..j] og får dp[i+2][j]
            #   Motspiller kan ta coins[j] -> jeg spiller videre på [i+1..j-1] og får dp[i+1][j-1]
            #   Motspiller velger det som er dårligst for meg: min av disse

            # Hvis jeg tar coins[j]:
            #   Motspiller kan ta coins[i] -> jeg spiller videre på [i+1..j-1] og får dp[i+1][j-1]
            #   Motspiller kan ta coins[j-1] -> jeg spiller videre på [i..j-2] og får dp[i][j-2]
            #   Motspiller velger det som er dårligst for meg: min av disse

            # Håndter grensetilfeller
            val_i_plus_2_j = dp[i + 2][j] if i + 2 <= j else 0
            val_i_plus_1_j_minus_1 = dp[i + 1][j - 1] if i + 1 <= j - 1 else 0
            val_i_j_minus_2 = dp[i][j - 2] if i <= j - 2 else 0

            take_left = coins[i] + min(val_i_plus_2_j, val_i_plus_1_j_minus_1)
            take_right = coins[j] + min(val_i_plus_1_j_minus_1, val_i_j_minus_2)

            dp[i][j] = max(take_left, take_right)

    return dp[0][n - 1]


def gen_examples(k, cl, cu, vl, vu):
    """Generer tilfeldige testinstanser."""
    for _ in range(k):
        # Sørg for at n er partall
        n = random.randint(max(2, cl), cu)
        if n % 2 != 0:
            n += 1
        if n > cu:
            n -= 2

        # Generer tilfeldige myntverdier
        coins = [random.randint(vl, vu) for _ in range(n)]

        # Beregn forventet svar
        expected = coin_game_dp(coins)

        yield coins, expected


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests = list(tests)  # Konverter til liste hvis nødvendig
    tests += list(
        gen_examples(
            random_tests,
            coins_lower,
            coins_upper,
            value_lower,
            value_upper,
        )
    )


def get_feedback(student, answer, coins):
    """Gi tilbakemelding på studentens løsning."""
    if student is None:
        return "Du returnerte None. Husk å implementere solve-funksjonen."

    if not isinstance(student, (int, float)):
        return f"Du returnerte ikke et tall, men {type(student).__name__}"

    if student != answer:
        total = sum(coins)
        opponent_gets = total - answer
        return (
            f"Feil svar.\n"
            f"  Ditt svar: {student}\n"
            f"  Forventet: {answer}\n"
            f"  (Total verdi: {total}, motspiller får optimalt: {opponent_gets})"
        )

    return None


def print_coins(coins):
    """Hjelpefunksjon for å skrive ut mynter i lesbart format."""
    if not coins:
        return "[]"
    return "[" + ", ".join(str(c) for c in coins) + "]"


failed = False
num_passed = 0

for i, (coins, expected_answer) in enumerate(tests, 1):
    student_answer = solve(coins[:])  # Kopier listen
    response = get_feedback(student_answer, expected_answer, coins)

    if response is not None:
        if not failed:
            print("=" * 60)
            print("FEIL FUNNET")
            print("=" * 60)
        elif num_passed > 0:
            print("-" * 60)
        failed = True

        # Begrens visning for lange lister
        coins_str = (
            print_coins(coins)
            if len(coins) <= 10
            else f"[{coins[0]}, {coins[1]}, ..., {coins[-2]}, {coins[-1]}] ({len(coins)} mynter)"
        )

        print(
            f"""
Test {i} feilet:
Mynter: {coins_str}
{response}
"""
        )
        num_passed = 0

        # Stopp etter 3 feil for å ikke overvelde
        if (
            sum(1 for c, e in tests[:i] if get_feedback(solve(c[:]), e, c) is not None)
            >= 3
        ):
            remaining = len(tests) - i
            if remaining > 0:
                print(f"... stopper etter 3 feil ({remaining} tester gjenstår)")
            break
    else:
        num_passed += 1

if not failed:
    print(f"✓ Koden fungerte for alle {len(tests)} testene!")
