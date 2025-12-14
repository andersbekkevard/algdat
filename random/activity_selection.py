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
# Lavest mulig antall aktiviteter i generert instans.
activities_lower = 5
# Høyest mulig antall aktiviteter i generert instans.
activities_upper = 15
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


def solve(activities):
    """
    Velger maksimalt antall ikke-overlappende aktiviteter.

    Args:
        activities: Liste av tupler (start, finish) hvor hver tuppel representerer
                    en aktivitet med starttid og sluttid.
                    Eksempel: [(1, 4), (3, 5), (0, 6), (5, 7), (8, 9), (5, 9)]

    Returns:
        Heltall som representerer antall valgte aktiviteter.
        Dette skal være maksimalt antall ikke-overlappende aktiviteter.

    Complexity: Should be O(n log n) where n is the number of activities.
    """
    if not activities:
        return 0

    return solve_clrs(activities)

    n = len(activities)
    end = max(finish for start, finish in activities)
    # Create list of (finish, start, index) tuples and sort by finish time
    indexed = [(finish, start, idx) for idx, (start, finish) in enumerate(activities)]
    indexed.sort()

    # dp[i][j] = maximum number of activities using first i activities (sorted),
    # where j is the maximum finish time we can use (time constraint)
    # j represents the "earliest starting time of the remaining subproblem"
    # = the final ending time of the current solution
    dp = [[0] * (end + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        finish_i, start_i, _ = indexed[i - 1]
        for j in range(end + 1):
            # Don't take activity i-1
            dp[i][j] = dp[i - 1][j]
            # Take activity i-1 if it fits: finish_i <= j and we can schedule it
            if finish_i <= j:
                # Can take it if start_i >= the finish time of previous solution
                # Find the best solution that ends at or before start_i
                # This means checking dp[i-1][start_i] (best solution ending at start_i or earlier)
                prev_finish = min(start_i, end)
                prev_best = dp[i - 1][prev_finish]
                dp[i][j] = max(dp[i][j], prev_best + 1)

    return dp[n][end]


def solve_clrs(activities):
    """
    CLRS dynamic programming solution using the recurrence:
    c[i, j] = max {c[i, k] + c[k, j] + 1 : a_k ∈ S_ij} if S_ij ≠ ∅, else 0

    Where S_ij is the set of activities that start after a_i finishes
    and finish before a_j starts.
    """
    if not activities:
        return 0

    n = len(activities)

    # Add dummy activities a_0 (finishes at 0) and a_{n+1} (starts at infinity)
    # to bound the problem: a_0 finishes at 0, a_{n+1} starts at max_finish + 1
    max_finish = max(finish for _, finish in activities)
    extended_activities = [(0, 0)] + activities + [(max_finish + 1, max_finish + 1)]
    n_extended = len(extended_activities)

    # c[i][j] = size of optimal solution for S_ij
    # where S_ij = activities that start after a_i finishes and finish before a_j starts
    # Use bottom-up DP to avoid recursion issues
    c = [[0] * n_extended for _ in range(n_extended)]

    # Sort activities by finish time for efficient processing
    # We'll process pairs (i, j) where j > i
    # Process in order of increasing gap between i and j
    for gap in range(2, n_extended):
        for i in range(n_extended - gap):
            j = i + gap

            # Get finish time of a_i and start time of a_j
            _, finish_i = extended_activities[i]
            start_j, _ = extended_activities[j]

            # Find all activities a_k in S_ij
            # S_ij = activities that start after a_i finishes and finish before a_j starts
            activities_in_sij = []
            for k in range(1, n_extended - 1):  # Skip dummy activities
                start_k, finish_k = extended_activities[k]
                # Activity a_k is in S_ij if it starts after a_i finishes and finishes before a_j starts
                if start_k >= finish_i and finish_k <= start_j:
                    activities_in_sij.append(k)

            # If S_ij is empty, c[i, j] = 0 (already initialized)
            if activities_in_sij:
                # Otherwise, c[i, j] = max {c[i, k] + c[k, j] + 1 : a_k ∈ S_ij}
                max_val = 0
                for k in activities_in_sij:
                    # Ensure k is between i and j
                    if i < k < j:
                        val = c[i][k] + c[k][j] + 1
                        max_val = max(max_val, val)
                c[i][j] = max_val

    # Return c[0, n+1] which gives optimal solution for all activities
    return c[0][n_extended - 1]


def solve_greedy(activities):
    indexed = [(finish, start, idx) for idx, (start, finish) in enumerate(activities)]
    indexed.sort()
    current_finish = -1e9
    count = 0
    for finish, start, idx in indexed:
        if start >= current_finish:
            count += 1
            current_finish = finish
    return count


def get_feedback(student_answer, expected_answer, activities):
    """Provide feedback on student's solution."""
    if type(student_answer) != int:
        return f"Du returnerte ikke et heltall, men {type(student_answer).__name__}"

    if student_answer < 0:
        return f"Antall aktiviteter kan ikke være negativt, men du returnerte {student_answer}"

    n = len(activities)
    if n == 0:
        if student_answer != 0:
            return f"For tom liste, forventet 0, men fikk {student_answer}"
        return None

    if student_answer > n:
        return f"Du returnerte {student_answer} aktiviteter, men det finnes bare {n} aktiviteter totalt."

    # Check optimality (should have maximum number of activities)
    expected_count = expected_answer

    if student_answer < expected_count:
        return (
            f"Løsningen din har {student_answer} aktiviteter, men optimal løsning har {expected_count}.\n"
            f"Forventet antall: {expected_count}"
        )

    if student_answer == expected_count:
        return None  # Valid optimal solution

    # This shouldn't happen if expected_answer is optimal, but check anyway
    return (
        f"Løsningen din har {student_answer} aktiviteter, men optimal løsning har {expected_count}.\n"
        f"Forventet antall: {expected_count}"
    )


def greedy_activity_selection(activities):
    """
    Greedy algorithm for activity selection (for generating expected answers).
    Sorts by finish time and selects activities greedily.
    Returns the count of selected activities.
    """
    if not activities:
        return 0

    # Create list of (finish, start, index) tuples
    indexed = [(finish, start, idx) for idx, (start, finish) in enumerate(activities)]
    indexed.sort()

    count = 0
    last_finish = -1

    for finish, start, idx in indexed:
        if start >= last_finish:
            count += 1
            last_finish = finish

    return count


# Hardkodete tester på format: (activities, expected_count)
# activities er liste av (start, finish) tupler
# expected_count er antall aktiviteter i optimal løsning
tests = [
    # Tom liste
    ([], 0),
    # En aktivitet
    ([(1, 4)], 1),
    # To ikke-overlappende aktiviteter
    ([(1, 4), (5, 7)], 2),
    # To overlappende aktiviteter - velg en
    ([(1, 4), (3, 6)], 1),
    # Tre aktiviteter, to overlapper
    ([(1, 4), (3, 6), (5, 8)], 2),
    # Klassisk eksempel fra CLRS
    ([(1, 4), (3, 5), (0, 6), (5, 7), (8, 9), (5, 9)], 3),
    # Alle aktiviteter overlapper
    ([(1, 5), (2, 6), (3, 7), (4, 8)], 1),
    # Ingen overlapp
    ([(1, 2), (3, 4), (5, 6), (7, 8)], 4),
    # Aktiviteter som starter samtidig
    ([(1, 3), (1, 4), (1, 5), (2, 6)], 1),
    # Aktiviteter som slutter samtidig
    ([(1, 5), (2, 5), (3, 5), (4, 5)], 1),
    # Kompleks eksempel med flere mulige løsninger
    ([(1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8)], 3),
    # Aktiviteter med samme start og slutt
    ([(1, 1), (2, 2), (3, 3)], 3),
    # Aktiviteter som starter på 0
    ([(0, 1), (1, 2), (2, 3)], 3),
    # Stor mengde ikke-overlappende
    ([(i, i + 1) for i in range(10)], 10),
]


def gen_examples(k, nl, nu):
    """Generate random activity selection test instances."""
    for _ in range(k):
        n = random.randint(max(3, nl), nu)

        # Generate random activities
        # Ensure activities have valid start < finish
        activities = []
        for _ in range(n):
            start = random.randint(0, 20)
            finish = random.randint(start + 1, start + 10)
            activities.append((start, finish))

        # Compute expected answer using greedy algorithm
        expected = greedy_activity_selection(activities)

        yield activities, expected


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(
        gen_examples(
            random_tests,
            activities_lower,
            activities_upper,
        )
    )


def print_activities(activities):
    """Helper function to print activities in readable format."""
    if not activities:
        return "Tom liste (0 aktiviteter)"

    lines = []
    for i, (start, finish) in enumerate(activities):
        lines.append(f"  Aktivitet {i}: ({start}, {finish})")
    return f"{len(activities)} aktiviteter:\n" + "\n".join(lines)


def print_solution(count, activities):
    """Helper function to print solution in readable format."""
    return f"{count} aktiviteter"


failed = False
for activities, expected_answer in tests:
    student_answer = solve(activities[:])  # Copy list
    response = get_feedback(student_answer, expected_answer, activities)

    if response is not None:
        if failed:
            print("-" * 50)
        failed = True
        print(
            f"""
Koden feilet for følgende instans.
{print_activities(activities)}

Ditt svar: {student_answer}
Forventet svar: {expected_answer}

Feilmelding: {response}
"""
        )


if not failed:
    print("Koden fungerte for alle eksempeltestene.")
