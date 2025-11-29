# !/usr/bin/python3
# coding=utf-8

import random
from collections import deque
from typing import Deque

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = False
# Antall tilfeldige tester som genereres.
random_tests = 10
# Lavest mulig antall punkter i generert instans.
points_lower = 3
# Høyest mulig antall punkter i generert instans.
points_upper = 10
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


def solve(points):
    """
    Finner det største rektangelet med horisontale/vertikale sider som ligger
    innenfor regionen definert av punktene.

    Args:
        points: Liste av tupler (x, y) hvor hvert punkt har positive koordinater.
                Punktene er sortert slik at xi < xi+1 for i = 1...n-1.
                Format: [(x1, y1), (x2, y2), ..., (xn, yn)]

    Returns:
        Arealet til det største rektangelet (float eller int).

    """
    if len(points) < 2:
        return 0

    bars = [(0, 0)]
    max_area = 0
    for i in range(len(points)):
        x_i, y_i = points[i][0], points[i][1]
        if y_i >= bars[-1][1]:
            bars.append(points[i])
        else:
            last_popped_x = None
            while len(bars) > 1 and bars[-1][1] > y_i:
                popped_x, popped_y = bars.pop()
                last_popped_x = popped_x
                # Calculate rectangle ending at popped_x with height popped_y
                # The left boundary is bars[-1][0], but we need to verify validity
                # Actually, since bars has increasing heights, bars[-1] should be valid
                # But we need to check: can we have a rectangle from bars[-1][0] to popped_x with height popped_y?
                # This requires all points between to have y >= popped_y
                # For now, calculate it - the main loop should handle most cases correctly
                area = (popped_x - bars[-1][0]) * popped_y
                max_area = max(max_area, area)
            # Use the last popped x as left boundary if available, otherwise use bars[-1][0]
            left_x = last_popped_x if last_popped_x is not None else bars[-1][0]
            max_area = max(max_area, (x_i - left_x) * y_i)
            bars.append(points[i])

    # Process remaining bars - calculate rectangles extending to the last x
    if len(bars) > 1:
        last_x = points[-1][0]
        for i in range(1, len(bars)):
            bar_x, bar_y = bars[i]
            # Find leftmost x where rectangle from that x to last_x is valid
            # (all points in range have y >= bar_y)
            left_x = 0
            for j in range(len(points)):
                p_x = points[j][0]
                # Check if rectangle from p_x to last_x is valid
                min_y_in_range = min(points[k][1] for k in range(j, len(points)))
                if min_y_in_range >= bar_y:
                    left_x = p_x
                    break
            area = (last_x - left_x) * bar_y
            max_area = max(max_area, area)

    return max_area


# Hardkodete tester på format: (points_list, expected_area)
# points_list er en liste av (x, y) tupler, sortert etter x-koordinat
tests = [
    # Tom liste
    ([], 0),
    # Ett punkt - ingen rektangel mulig
    ([(1, 1)], 0),
    # To punkter - rektangel mellom dem
    ([(1, 2), (3, 1)], 2),  # Bredde: 3-1=2, Høyde: min(2,1)=1, Areal: 2*1=2
    # Tre punkter - enkel case
    (
        [(1, 3), (2, 1), (4, 2)],
        3,
    ),  # Rektangel fra x=1 til x=2, høyde=1, areal=1*1=1? Nei, la meg tenke...
    # Tre punkter - større rektangel
    (
        [(0, 5), (2, 2), (5, 3)],
        10,
    ),  # Rektangel fra x=0 til x=5, høyde=min(5,2,3)=2, areal=5*2=10
    # Fire punkter
    ([(1, 4), (2, 1), (3, 3), (5, 2)], 4),
    # Eksempel fra oppgaven
    ([(1, 3), (3, 1), (5, 4), (7, 2)], 6),
]


def largest_rectangle_bruteforce(points):
    """
    Brute force løsning for å verifisere korrekthet.
    Prøver alle mulige rektangler.
    """
    n = len(points)
    if n < 2:
        return 0

    max_area = 0

    # Prøv alle par av x-koordinater som kan være venstre og høyre side
    for i in range(n):
        for j in range(i + 1, n):
            x_left = points[i][0]
            x_right = points[j][0]
            width = x_right - x_left

            # Finn minimum y-koordinat mellom x_left og x_right
            # Dette er høyden på det største rektangelet med disse x-sidene
            min_y = min(points[k][1] for k in range(i, j + 1))

            area = width * min_y
            max_area = max(max_area, area)

    return max_area


def gen_examples(k, pl, pu):
    """Generer tilfeldige testinstanser."""
    for _ in range(k):
        n = random.randint(max(2, pl), pu)

        # Generer punkter med x-koordinater i stigende rekkefølge
        points = []
        x = 0
        for i in range(n):
            x += random.uniform(1, 5)  # Øk x med tilfeldig verdi
            y = random.uniform(1, 10)  # Tilfeldig y-koordinat
            points.append((x, y))

        # Beregn forventet svar ved hjelp av brute force
        expected = largest_rectangle_bruteforce(points)

        yield points, expected


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(
        gen_examples(
            random_tests,
            points_lower,
            points_upper,
        )
    )


def get_feedback(student, answer, points):
    """Gi tilbakemelding på studentens løsning."""
    if not isinstance(student, (int, float)):
        return f"Du returnerte ikke et tall, men {type(student).__name__}"

    # Tillat liten avvik pga flyttall-presisjon
    if abs(student - answer) > 1e-9:
        points_str = ", ".join(f"({x}, {y})" for x, y in points)
        return (
            f"Feil svar for punktene: [{points_str}]\n"
            f"  Ditt svar: {student}\n"
            f"  Forventet: {answer}"
        )

    return None


def print_points(points):
    """Hjelpefunksjon for å skrive ut punkter i lesbart format."""
    if not points:
        return "Ingen punkter"
    return ", ".join(f"({x}, {y})" for x, y in points)


failed = False
for points, expected_answer in tests:
    student_answer = solve(points[:])  # Kopier listen
    response = get_feedback(student_answer, expected_answer, points)

    if response is not None:
        if failed:
            print("-" * 50)
        failed = True
        print(
            f"""
Koden feilet for følgende instans.
Punkter: {print_points(points)}

Ditt svar: {student_answer}
Forventet svar: {expected_answer}
Feilmelding: {response}
"""
        )


if not failed:
    print("Koden fungerte for alle eksempeltestene.")
