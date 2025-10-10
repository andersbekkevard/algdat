#!/usr/bin/python3
# coding=utf-8

# Testsettet på serveren er større og mer omfattende enn dette.
# Hvis programmet ditt fungerer lokalt, men ikke når du laster det opp,
# er det gode sjanser for at det er tilfeller du ikke har tatt høyde for.

# Kontrollerer om koden skal kjøres på større hardkodete tester.
large_tests = False


def knapsack(weights, values, capacity):
    """
    Løs 0/1 knapsack-problemet ved hjelp av dynamisk programmering.

    Args:
        weights: Liste med vekter for hver gjenstand
        values: Liste med verdier for hver gjenstand
        capacity: Maksimal kapasitet i sekken

    Returns:
        Maksimal verdi som kan oppnås
    """
    return solve_memo(dict(), weights, values, len(weights), capacity)


def solve_naive(weights, values, n, W):
    if n == 0 or W == 0:
        return 0
    x = solve_naive(weights, values, n - 1, W)
    if weights[n - 1] > W:
        return x
    y = solve_naive(weights, values, n - 1, W - weights[n - 1]) + values[n - 1]
    return max(x, y)


def solve_memo(table, weights, values, n, W):
    if (n, W) in table:
        return table[(n, W)]
    if n == 0 or W == 0:
        result = 0
    elif weights[n - 1] > W:
        result = solve_memo(table, weights, values, n - 1, W)
    else:
        exclude = solve_memo(table, weights, values, n - 1, W)
        include = (
            solve_memo(table, weights, values, n - 1, W - weights[n - 1])
            + values[n - 1]
        )

        result = max(exclude, include)
    table[(n, W)] = result
    return result


def solve_table(weights, values, n, W):
    # Create 2D table with dimensions (n+1) x (W+1)
    table = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    # Fill table bottom-up
    for i in range(1, n + 1):
        if W == 0:
            break
        for w in range(W + 1):
            if weights[i - 1] > w:
                table[i][w] = table[i - 1][w]
            else:
                exclude = table[i - 1][w]
                include = table[i - 1][w - weights[i - 1]] + values[i - 1]
                table[i][w] = max(exclude, include)

    return table[n][W]


# region tests
# Hardkodete tester på formatet: (weights, values, capacity, svar)
tests = [
    ([2, 3, 4, 5], [3, 4, 5, 6], 5, 7),
    ([1, 2, 3], [6, 10, 12], 5, 22),
    ([10, 20, 30], [60, 100, 120], 50, 220),
    ([5, 4, 6, 3], [10, 40, 30, 50], 10, 90),
    ([2, 2, 2, 2], [5, 5, 5, 5], 4, 10),
    ([1], [10], 1, 10),
    ([1, 2], [1, 2], 1, 1),
    ([3, 4, 5], [30, 50, 60], 8, 90),
    ([1, 3, 4, 5], [1, 4, 5, 7], 7, 9),
    ([2, 3, 4, 5], [3, 4, 5, 6], 0, 0),
]

# Store hardkodete tester
if large_tests:
    tests += [
        ([7, 3, 4, 5, 6, 8, 2, 9, 1], [10, 5, 6, 8, 12, 15, 3, 18, 2], 20, 46),
        ([10, 15, 20, 25, 30], [100, 90, 120, 80, 70], 40, 210),
        ([5, 10, 15, 20, 25], [50, 60, 70, 80, 90], 50, 280),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 5, 8, 9, 10, 17, 17, 20, 24, 30], 25, 80),
        ([2, 3, 5, 7, 11, 13], [5, 8, 14, 20, 30, 35], 20, 62),
        ([4, 5, 6, 7, 8, 9, 10], [8, 10, 12, 14, 16, 18, 20], 30, 66),
        ([3, 4, 5, 6, 7, 8], [6, 8, 10, 12, 14, 16], 18, 42),
        ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2], 5, 10),
        ([5, 5, 5, 5, 5], [10, 10, 10, 10, 10], 12, 20),
        ([8, 9, 10, 11, 12], [16, 18, 20, 22, 24], 25, 54),
    ]

failed = False
for weights, values, capacity, answer in tests:
    student = knapsack(weights, values, capacity)
    if student != answer:
        if failed:
            print("-" * 50)
        failed = True

        print(
            f"""
Koden feilet for følgende instans:
weights: {weights}
values: {values}
capacity: {capacity}

Ditt svar: {student}
Riktig svar: {answer}
"""
        )

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")


def benchmark_comparison():
    """
    Sammenlign hastigheten mellom solve_naive, solve_memo og solve_table med ulike størrelser.
    """
    import time
    import random

    print("\n" + "=" * 100)
    print("HASTIGHETSBENCHMARK: solve_naive vs solve_memo vs solve_table")
    print("=" * 100)

    # Generer test cases av ulike størrelser
    test_sizes = [5, 8, 10, 12, 15, 18, 20, 25, 30, 40, 50, 100, 200]

    results = []
    skip_naive = False  # Starter å hoppe over naive når den tar > 1 sekund

    for n in test_sizes:
        # Generer tilfeldige vekter og verdier
        random.seed(42 + n)  # For reproduserbarhet (unik seed per størrelse)
        weights = [random.randint(1, 10) for _ in range(n)]
        values = [random.randint(1, 20) for _ in range(n)]
        capacity = sum(weights) // 2  # Halvparten av total vekt

        # Test solve_naive
        if not skip_naive:
            start_naive = time.perf_counter()
            result_naive = solve_naive(weights, values, n, capacity)
            time_naive = time.perf_counter() - start_naive

            # Hvis det tok mer enn 1 sekund, hopp over naive for større størrelser
            if time_naive > 1.0:
                skip_naive = True
        else:
            time_naive = None
            result_naive = None

        # Test solve_memo (memoized)
        start_memo = time.perf_counter()
        table = dict()
        result_memo = solve_memo(table, weights, values, n, capacity)
        time_memo = time.perf_counter() - start_memo

        # Test solve_table (tabulation)
        start_table = time.perf_counter()
        result_table = solve_table(weights, values, n, capacity)
        time_table = time.perf_counter() - start_table

        # Verifiser at resultatene er like
        if time_naive is not None and result_naive != result_memo:
            print(f"⚠️  ADVARSEL: Ulike resultater mellom naive og memo for n={n}!")
        if result_memo != result_table:
            print(f"⚠️  ADVARSEL: Ulike resultater mellom memo og table for n={n}!")

        results.append(
            {
                "n": n,
                "capacity": capacity,
                "time_naive": time_naive,
                "time_memo": time_memo,
                "time_table": time_table,
                "speedup_memo": time_naive / time_memo if time_naive else None,
                "speedup_table": time_naive / time_table if time_naive else None,
                "memo_vs_table": time_memo / time_table if time_table > 0 else None,
            }
        )

    # Print resultatene i en pen tabell
    print("\n┌" + "─" * 98 + "┐")
    print("│" + " " * 42 + "RESULTATER" + " " * 46 + "│")
    print(
        "├"
        + "─" * 6
        + "┬"
        + "─" * 10
        + "┬"
        + "─" * 14
        + "┬"
        + "─" * 14
        + "┬"
        + "─" * 14
        + "┬"
        + "─" * 12
        + "┬"
        + "─" * 12
        + "┬"
        + "─" * 12
        + "┤"
    )
    print(
        f"│ {'n':^4} │ {'Kap.':^8} │ {'Naive (s)':^12} │ {'Memo (s)':^12} │ {'Table (s)':^12} │ {'N→M':^10} │ {'N→T':^10} │ {'M/T':^10} │"
    )
    print(
        "├"
        + "─" * 6
        + "┼"
        + "─" * 10
        + "┼"
        + "─" * 14
        + "┼"
        + "─" * 14
        + "┼"
        + "─" * 14
        + "┼"
        + "─" * 12
        + "┼"
        + "─" * 12
        + "┼"
        + "─" * 12
        + "┤"
    )

    for r in results:
        n_str = f"{r['n']}"
        cap_str = f"{r['capacity']}"

        if r["time_naive"] is not None:
            naive_str = f"{r['time_naive']:.6f}"
            speedup_memo_str = f"{r['speedup_memo']:.2f}x"
            speedup_table_str = f"{r['speedup_table']:.2f}x"
        else:
            naive_str = "TOO SLOW"
            speedup_memo_str = "N/A"
            speedup_table_str = "N/A"

        memo_str = f"{r['time_memo']:.6f}"
        table_str = f"{r['time_table']:.6f}"
        memo_vs_table_str = (
            f"{r['memo_vs_table']:.2f}x" if r["memo_vs_table"] else "N/A"
        )

        print(
            f"│ {n_str:>4} │ {cap_str:>8} │ {naive_str:>12} │ {memo_str:>12} │ {table_str:>12} │ {speedup_memo_str:>10} │ {speedup_table_str:>10} │ {memo_vs_table_str:>10} │"
        )

    print(
        "└"
        + "─" * 6
        + "┴"
        + "─" * 10
        + "┴"
        + "─" * 14
        + "┴"
        + "─" * 14
        + "┴"
        + "─" * 14
        + "┴"
        + "─" * 12
        + "┴"
        + "─" * 12
        + "┴"
        + "─" * 12
        + "┘"
    )

    # Print forklaring
    print("\n📝 N→M: Speedup fra Naive til Memoization")
    print("📝 N→T: Speedup fra Naive til Tabulation")
    print("📝 M/T: Ratio Memoization/Tabulation (>1 betyr Tabulation er raskere)")

    # Print oppsummering
    print("\n" + "=" * 100)
    print("OPPSUMMERING:")
    print("=" * 100)

    valid_memo_speedups = [
        r["speedup_memo"] for r in results if r["speedup_memo"] is not None
    ]
    valid_table_speedups = [
        r["speedup_table"] for r in results if r["speedup_table"] is not None
    ]
    valid_memo_vs_table = [
        r["memo_vs_table"] for r in results if r["memo_vs_table"] is not None
    ]

    if valid_memo_speedups:
        avg_memo_speedup = sum(valid_memo_speedups) / len(valid_memo_speedups)
        max_memo_speedup = max(valid_memo_speedups)
        print(
            f"📊 Memoization - Gjennomsnittlig speedup vs Naive: {avg_memo_speedup:.2f}x"
        )
        print(f"🚀 Memoization - Maksimal speedup vs Naive: {max_memo_speedup:.2f}x")

    if valid_table_speedups:
        avg_table_speedup = sum(valid_table_speedups) / len(valid_table_speedups)
        max_table_speedup = max(valid_table_speedups)
        print(
            f"📊 Tabulation - Gjennomsnittlig speedup vs Naive: {avg_table_speedup:.2f}x"
        )
        print(f"🚀 Tabulation - Maksimal speedup vs Naive: {max_table_speedup:.2f}x")

    if valid_memo_vs_table:
        avg_ratio = sum(valid_memo_vs_table) / len(valid_memo_vs_table)
        if avg_ratio > 1:
            print(
                f"\n⚡ Tabulation er i gjennomsnitt {avg_ratio:.2f}x raskere enn Memoization"
            )
        elif avg_ratio < 1:
            print(
                f"\n⚡ Memoization er i gjennomsnitt {1/avg_ratio:.2f}x raskere enn Tabulation"
            )
        else:
            print(f"\n⚖️  Memoization og Tabulation har omtrent samme hastighet")

    print("=" * 100 + "\n")


# endregion


# Kjør benchmark hvis du vil
# Uncomment linjen under for å kjøre benchmarken:
benchmark_comparison()
