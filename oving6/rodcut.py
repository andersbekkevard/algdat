#!/usr/bin/python3
# coding=utf-8

# Testsettet på serveren er større og mer omfattende enn dette.
# Hvis programmet ditt fungerer lokalt, men ikke når du laster det opp,
# er det gode sjanser for at det er tilfeller du ikke har tatt høyde for.

# Kontrollerer om koden skal kjøres på større hardkodete tester.
large_tests = True


def rodcut(n, prices):
    """
    Løs rod cutting-problemet ved hjelp av dynamisk programmering.

    Finn lengdene l_1, ..., l_k der summen av lengder l_1 + ... + l_k er n
    og totalprisen r_n = p_l1 + ... + p_lk er maksimal.

    Args:
        n: Lengden på stangen som skal kuttes
        prices: Liste med priser der prices[i] er prisen for lengde i+1

    Returns:
        Maksimal totalpris som kan oppnås
    """
    return rodcut_naive(n, prices)
    # memo = dict()
    # return rodcut_memo(n, prices, memo)


def rodcut_naive(n, prices):
    """
    Naiv rekursiv løsning for rod cutting-problemet.
    """
    if n == 0:
        return 0
    return max([rodcut_naive(n - i, prices) + prices[i - 1] for i in range(1, n + 1)])


def rodcut_memo(n, prices, memo):
    if n == 0:
        return 0
    elif n in memo.keys():
        return memo[n]
    memo[n] = max(
        [rodcut_memo(n - i, prices, memo) + prices[i - 1] for i in range(1, n + 1)]
    )
    return memo[n]


# region tests
# Hardkodete tester på formatet: (n, prices, svar)
tests = [
    (1, [1], 1),
    (2, [1, 5], 5),
    (3, [1, 5, 8], 8),
    (4, [1, 5, 8, 9], 10),
    (5, [1, 5, 8, 9, 10], 13),
    (6, [1, 5, 8, 9, 10, 17], 17),
    (7, [1, 5, 8, 9, 10, 17, 17], 18),
    (8, [1, 5, 8, 9, 10, 17, 17, 20], 22),
    (9, [1, 5, 8, 9, 10, 17, 17, 20, 24], 25),
    (10, [1, 5, 8, 9, 10, 17, 17, 20, 24, 30], 30),
]

# Store hardkodete tester
if large_tests:
    tests += [
        (15, [1, 5, 8, 9, 10, 17, 17, 20, 24, 30, 31, 32, 33, 34, 35], 43),
        (
            20,
            [
                1,
                5,
                8,
                9,
                10,
                17,
                17,
                20,
                24,
                30,
                31,
                32,
                33,
                34,
                35,
                36,
                37,
                38,
                39,
                40,
            ],
            60,
        ),
        (12, [3, 5, 8, 9, 10, 17, 17, 20, 24, 30, 31, 32], 36),
        (8, [2, 5, 7, 8, 10, 15, 16, 18], 20),
        (10, [2, 5, 7, 8, 10, 15, 16, 18, 20, 25], 27),
        (7, [3, 7, 10, 13, 16, 20, 23], 23),
        (5, [2, 4, 6, 8, 10], 10),
        (6, [3, 6, 9, 12, 15, 18], 18),
        (9, [4, 8, 12, 16, 20, 24, 28, 32, 36], 36),
        (11, [1, 5, 8, 9, 10, 17, 17, 20, 24, 30, 31], 33),
    ]

failed = False
for n, prices, answer in tests:
    student = rodcut(n, prices)
    if student != answer:
        if failed:
            print("-" * 50)
        failed = True

        print(
            f"""
Koden feilet for følgende instans:
n: {n}
prices: {prices}

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
    print("HASTIGHETSBENCHMARK: rodcut_naive vs rodcut_memo vs rodcut_table")
    print("=" * 100)

    # Generer test cases av ulike størrelser
    test_sizes = [5, 8, 10, 12, 15, 18, 20, 22, 25, 30, 40, 50, 100]

    results = []
    skip_naive = False  # Starter å hoppe over naive når den tar > 1 sekund

    for n in test_sizes:
        # Generer tilfeldige priser
        random.seed(42 + n)  # For reproduserbarhet (unik seed per størrelse)
        prices = [random.randint(1, n * 2) for _ in range(n)]

        # Test rodcut_naive
        if not skip_naive and n <= 20:  # Hopp over naive for store n
            start_naive = time.perf_counter()
            result_naive = rodcut_naive(n, prices)
            time_naive = time.perf_counter() - start_naive

            # Hvis det tok mer enn 1 sekund, hopp over naive for større størrelser
            if time_naive > 1.0:
                skip_naive = True
        else:
            time_naive = None
            result_naive = None

        # Test rodcut_memo (memoized)
        start_memo = time.perf_counter()
        result_memo = rodcut_memo(n, prices)
        time_memo = time.perf_counter() - start_memo

        # Test rodcut_table (tabulation)
        start_table = time.perf_counter()
        result_table = rodcut_table(n, prices)
        time_table = time.perf_counter() - start_table

        # Verifiser at resultatene er like
        if time_naive is not None and result_naive != result_memo:
            print(f"⚠️  ADVARSEL: Ulike resultater mellom naive og memo for n={n}!")
        if result_memo != result_table:
            print(f"⚠️  ADVARSEL: Ulike resultater mellom memo og table for n={n}!")

        results.append(
            {
                "n": n,
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
        f"│ {'n':^4} │ {'Naive (s)':^12} │ {'Memo (s)':^12} │ {'Table (s)':^12} │ {'N→M':^10} │ {'N→T':^10} │ {'M/T':^10} │"
    )
    print(
        "├"
        + "─" * 6
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
            f"│ {n_str:>4} │ {naive_str:>12} │ {memo_str:>12} │ {table_str:>12} │ {speedup_memo_str:>10} │ {speedup_table_str:>10} │ {memo_vs_table_str:>10} │"
        )

    print(
        "└"
        + "─" * 6
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
# benchmark_comparison()
