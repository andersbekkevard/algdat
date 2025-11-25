# !/usr/bin/python3
# coding=utf-8
import random
from itertools import product

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
# Lavest mulig brettstørrelse i generert instans.
board_size_lower = 3
# Høyest mulig brettstørrelse i generert instans.
board_size_upper = 8
# Lavest mulig antall trekk i generert instans.
moves_lower = 1
# Høyest mulig antall trekk i generert instans.
moves_upper = 10
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


def solve(n, k):
    """
    Beregner sannsynligheten for at en springer fortsatt er på brettet
    etter k trekk, når springeren starter i rute a1 (øverst til venstre).

    Args:
        n: Størrelse på sjakkbrettet (n×n). Springeren starter i (0, 0).
        k: Antall trekk springeren skal gjøre.
    """
    # Base case: after 0 moves, probability is 1.0
    if k == 0:
        return 1.0

    # Knight move offsets: (±2, ±1) og (±1, ±2)
    KNIGHT_MOVES = [
        (2, 1),
        (2, -1),
        (-2, 1),
        (-2, -1),
        (1, 2),
        (1, -2),
        (-1, 2),
        (-1, -2),
    ]

    def is_on_board(i: int, j: int) -> bool:
        """Check if position (i, j) is on the board."""
        return 0 <= i < n and 0 <= j < n

    def get_valid_moves(i: int, j: int) -> list[tuple[int, int]]:
        """Get all valid knight moves from position (i, j)."""
        return [
            (i + di, j + dj) for di, dj in KNIGHT_MOVES if is_on_board(i + di, j + dj)
        ]

    # Memoize valid moves for all board positions
    moves_memo = {(i, j): get_valid_moves(i, j) for i, j in product(range(n), repeat=2)}

    # Initialize DP table: P[move_num][i][j] = probability after (move_num+1) moves from (i,j)
    P = [[[-1.0 for _ in range(n)] for _ in range(n)] for _ in range(k)]

    # Calculate P[0]: probability after 1 move from each position
    for i, j in product(range(n), repeat=2):
        P[0][i][j] = len(moves_memo[(i, j)]) / 8

    # Fill DP table for moves 2 through k
    for move_num in range(1, k):
        for i, j in product(range(n), repeat=2):
            # Sum probabilities from all valid destination squares
            total = sum(P[move_num - 1][ni][nj] for ni, nj in moves_memo[(i, j)])
            P[move_num][i][j] = total / 8

    # Return probability after k moves starting from (0, 0)
    return P[k - 1][0][0]


def knight_probability_bruteforce(n, k):
    """
    Brute force løsning ved å simulere alle mulige sekvenser av trekk.
    Dette er for tregt for store verdier, men nyttig for verifisering.
    """
    if k == 0:
        return 1.0

    # Alle mulige springertrekk (dx, dy)
    moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n

    def count_valid_sequences(x, y, remaining_moves):
        # Check validity BEFORE checking remaining_moves
        # We want to count sequences where the knight stays on board
        if not is_valid(x, y):
            return 0

        if remaining_moves == 0:
            return 1

        total = 0
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            total += count_valid_sequences(nx, ny, remaining_moves - 1)

        return total

    total_sequences = count_valid_sequences(0, 0, k)
    total_possible = 8**k

    return total_sequences / total_possible


# Hardkodete tester på format: (n, k, expected_probability)
# expected_probability er sannsynligheten for at springeren fortsatt er på brettet

tests = [
    # --- Base cases ---
    (1, 0, 1.0),  # On 1x1 board, 0 moves → always on board
    (1, 1, 0.0),  # Any move leaves board
    (2, 0, 1.0),  # Always on board before moving
    (3, 0, 1.0),  # Always on board before moving
    # --- 1 move ---
    # From (0,0) on n×n board, only 2 moves are valid: (2,1) and (1,2)
    (3, 1, 0.25),  # 2 valid of 8
    (4, 1, 0.25),  # 2 valid of 8
    (5, 1, 0.25),  # 2 valid of 8
    (6, 1, 0.25),  # 2 valid of 8
    (8, 1, 0.25),  # 2 valid of 8
    # --- 2 moves ---
    # Computed via corrected bruteforce simulation
    (3, 2, 0.0625),
    (4, 2, 0.125),
    (5, 2, 0.1875),
    (6, 2, 0.1875),
    (8, 2, 0.1875),
    # --- 3 moves ---
    (3, 3, 0.015625),
    (4, 3, 0.0390625),
    (5, 3, 0.078125),
    (6, 3, 0.11328125),
    (8, 3, 0.125),
    # --- 4 moves ---
    (3, 4, 0.00390625),
    (4, 4, 0.017578125),
    (5, 4, 0.046875),
    (6, 4, 0.06982421875),
    (8, 4, 0.0986328125),
]


def gen_examples(k, bs_lower, bs_upper, m_lower, m_upper):
    """Generer tilfeldige testinstanser."""
    for _ in range(k):
        n = random.randint(max(1, bs_lower), bs_upper)
        moves = random.randint(
            max(0, m_lower), min(m_upper, 5)
        )  # Begrens moves for bruteforce

        # Bruk bruteforce for å beregne forventet svar (kun for små verdier)
        if n <= 5 and moves <= 4:
            expected = knight_probability_bruteforce(n, moves)
        else:
            # For større verdier, bruk en tilnærming eller hopp over
            continue

        yield n, moves, expected


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(
        gen_examples(
            random_tests,
            board_size_lower,
            board_size_upper,
            moves_lower,
            moves_upper,
        )
    )


def get_feedback(student, answer, n, k):
    """Gi tilbakemelding på studentens løsning."""
    if not isinstance(student, (int, float)) and student is not None:
        return f"Du returnerte ikke et tall, men {type(student).__name__}"

    if student is None:
        return "Du returnerte None"

    if not (0.0 <= student <= 1.0):
        return f"Sannsynlighet må være mellom 0.0 og 1.0, men du returnerte {student}"

    # Sjekk om svaret er nær nok (bruk liten toleranse for flyttall)
    tolerance = 1e-6
    if abs(student - answer) > tolerance:
        return (
            f"Feil svar for n={n}, k={k}\n"
            f"  Ditt svar: {student}\n"
            f"  Forventet: {answer}\n"
            f"  Differanse: {abs(student - answer)}"
        )

    return None


failed = False
for n, k, expected_answer in tests:
    student_answer = solve(n, k)
    response = get_feedback(student_answer, expected_answer, n, k)

    if response is not None:
        if failed:
            print("-" * 50)
        failed = True
        print(
            f"""
Koden feilet for følgende instans.
Brettstørrelse (n): {n}
Antall trekk (k): {k}

Ditt svar: {student_answer}
Forventet svar: {expected_answer}
Feilmelding: {response}
"""
        )


if not failed:
    print("Koden fungerte for alle eksempeltestene.")
