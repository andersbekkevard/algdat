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
    # dp = [0] * (n + 1)
    # for l in range(1, n + 1):
    #     m = -1e9
    #     for i in range(min(l, len(prices))):
    #         m = max(m, dp[l - (i + 1)] + prices[i])
    #     dp[l] = m
    # return dp[n]
    return rodcut_memo(n, prices)


def rodcut_memo(n, prices, memo={0: 0}):
    if n == 0:
        memo[n] = 0
    else:
        m = -1e9
        for i in range(min(n, len(prices))):
            m = max(m, rodcut_memo(n - (i + 1), prices, memo) + prices[i])
        memo[n] = m
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
        (10, [2, 5, 7, 8, 10, 15, 16, 18, 20, 25], 25),
        (7, [3, 7, 10, 13, 16, 20, 23], 24),
        (5, [2, 4, 6, 8, 10], 10),
        (6, [3, 6, 9, 12, 15, 18], 18),
        (9, [4, 8, 12, 16, 20, 24, 28, 32, 36], 36),
        (11, [1, 5, 8, 9, 10, 17, 17, 20, 24, 30, 31], 31),
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
    Sammenlign hastigheten mellom rodcut_naive, rodcut_memo og rodcut_table med ulike størrelser.
    """
    import time
    import random

    print("\n" + "=" * 110)
    print("🔬 HASTIGHETSBENCHMARK: Rod Cutting Algoritmer".center(110))
    print("=" * 110)

    # Generer test cases av ulike størrelser
    test_sizes = [5, 8, 10, 12, 15, 18, 20, 22, 25, 30, 40, 50, 100, 200]

    results = []
    skip_naive = False  # Starter å hoppe over naive når den tar > 1 sekund

    print("\n⏳ Kjører tester...\n")

    for n in test_sizes:
        # Generer tilfeldige priser (samme for alle tre metoder)
        random.seed(42 + n)  # For reproduserbarhet
        prices = [random.randint(1, n * 2) for _ in range(n)]

        result_data = {"n": n}

        # Test rodcut_naive (rekursiv)
        if not skip_naive and n <= 22:
            try:
                start = time.perf_counter()
                result_naive = rodcut_naive(n, prices)
                time_naive = time.perf_counter() - start
                result_data["time_naive"] = time_naive
                result_data["result_naive"] = result_naive

                # Skip naive hvis det tar mer enn 1 sekund
                if time_naive > 1.0:
                    skip_naive = True
                    print(f"⏭️  Hopper over naive for n > {n} (tar for lang tid)")
            except Exception as e:
                result_data["time_naive"] = None
                result_data["result_naive"] = None
                print(f"❌ Naive feilet for n={n}: {e}")
        else:
            result_data["time_naive"] = None
            result_data["result_naive"] = None

        # Test rodcut_memo (memoization)
        try:
            start = time.perf_counter()
            result_memo = rodcut_memo(n, prices, {})
            time_memo = time.perf_counter() - start
            result_data["time_memo"] = time_memo
            result_data["result_memo"] = result_memo
        except Exception as e:
            result_data["time_memo"] = None
            result_data["result_memo"] = None
            print(f"❌ Memo feilet for n={n}: {e}")

        # Test rodcut_table (tabulation)
        try:
            start = time.perf_counter()
            result_table = rodcut_table(n, prices)
            time_table = time.perf_counter() - start
            result_data["time_table"] = time_table
            result_data["result_table"] = result_table
        except Exception as e:
            result_data["time_table"] = None
            result_data["result_table"] = None
            print(f"❌ Table feilet for n={n}: {e}")

        # Verifiser at alle gir samme resultat
        all_results = [
            r
            for r in [
                result_data.get("result_naive"),
                result_data.get("result_memo"),
                result_data.get("result_table"),
            ]
            if r is not None
        ]

        if len(set(all_results)) > 1:
            print(f"⚠️  ADVARSEL: Ulike resultater for n={n}!")
            if result_data.get("result_naive") is not None:
                print(f"   Naive: {result_data['result_naive']}")
            if result_data.get("result_memo") is not None:
                print(f"   Memo:  {result_data['result_memo']}")
            if result_data.get("result_table") is not None:
                print(f"   Table: {result_data['result_table']}")

        results.append(result_data)

    # Print resultater i en pen tabell
    print("\n" + "=" * 110)
    print("📊 RESULTATER".center(110))
    print("=" * 110)

    # Tabell header
    print(
        "\n┌────────┬─────────────────┬─────────────────┬─────────────────┬──────────────┬──────────────┬──────────────┐"
    )
    print(
        "│   n    │   Naive (s)     │   Memo (s)      │   Table (s)     │  Naive/Memo  │ Naive/Table  │  Memo/Table  │"
    )
    print(
        "├────────┼─────────────────┼─────────────────┼─────────────────┼──────────────┼──────────────┼──────────────┤"
    )

    # Datarows
    for r in results:
        n = r["n"]

        # Formater naive tid
        if r["time_naive"] is not None:
            naive_str = f"{r['time_naive']:>13.6f}s"
        else:
            naive_str = "       -       "

        # Formater memo tid
        if r["time_memo"] is not None:
            memo_str = f"{r['time_memo']:>13.6f}s"
        else:
            memo_str = "       -       "

        # Formater table tid
        if r["time_table"] is not None:
            table_str = f"{r['time_table']:>13.6f}s"
        else:
            table_str = "       -       "

        # Beregn speedups
        if r["time_naive"] and r["time_memo"]:
            speedup_memo = r["time_naive"] / r["time_memo"]
            speedup_memo_str = f"{speedup_memo:>11.1f}x"
        else:
            speedup_memo_str = "      -      "

        if r["time_naive"] and r["time_table"]:
            speedup_table = r["time_naive"] / r["time_table"]
            speedup_table_str = f"{speedup_table:>11.1f}x"
        else:
            speedup_table_str = "      -      "

        if r["time_memo"] and r["time_table"]:
            ratio = r["time_memo"] / r["time_table"]
            ratio_str = f"{ratio:>11.2f}x"
        else:
            ratio_str = "      -      "

        print(
            f"│ {n:>6} │ {naive_str} │ {memo_str} │ {table_str} │ {speedup_memo_str} │ {speedup_table_str} │ {ratio_str} │"
        )

    print(
        "└────────┴─────────────────┴─────────────────┴─────────────────┴──────────────┴──────────────┴──────────────┘"
    )

    # Forklaring
    print("\n📝 Forklaring:")
    print("   • Naive/Memo: Hvor mye raskere er memoization enn naive rekursjon")
    print("   • Naive/Table: Hvor mye raskere er tabulation enn naive rekursjon")
    print(
        "   • Memo/Table: Ratio mellom memo og table (>1 = table er raskere, <1 = memo er raskere)"
    )

    # Statistikk og oppsummering
    print("\n" + "=" * 110)
    print("📈 OPPSUMMERING OG STATISTIKK".center(110))
    print("=" * 110 + "\n")

    # Beregn statistikk
    memo_speedups = [
        r["time_naive"] / r["time_memo"]
        for r in results
        if r.get("time_naive") and r.get("time_memo")
    ]
    table_speedups = [
        r["time_naive"] / r["time_table"]
        for r in results
        if r.get("time_naive") and r.get("time_table")
    ]
    memo_vs_table = [
        r["time_memo"] / r["time_table"]
        for r in results
        if r.get("time_memo") and r.get("time_table")
    ]

    if memo_speedups:
        print("🔹 MEMOIZATION vs NAIVE:")
        print(
            f"   • Gjennomsnittlig speedup: {sum(memo_speedups)/len(memo_speedups):.1f}x"
        )
        print(f"   • Minimum speedup: {min(memo_speedups):.1f}x")
        print(f"   • Maksimum speedup: {max(memo_speedups):.1f}x")
        print()

    if table_speedups:
        print("🔹 TABULATION vs NAIVE:")
        print(
            f"   • Gjennomsnittlig speedup: {sum(table_speedups)/len(table_speedups):.1f}x"
        )
        print(f"   • Minimum speedup: {min(table_speedups):.1f}x")
        print(f"   • Maksimum speedup: {max(table_speedups):.1f}x")
        print()

    if memo_vs_table:
        avg_ratio = sum(memo_vs_table) / len(memo_vs_table)
        print("🔹 MEMOIZATION vs TABULATION:")
        print(f"   • Gjennomsnittlig ratio: {avg_ratio:.2f}x")

        if avg_ratio > 1.1:
            print(
                f"   • 🏆 Tabulation er i gjennomsnitt {avg_ratio:.1f}x raskere enn memoization"
            )
        elif avg_ratio < 0.9:
            print(
                f"   • 🏆 Memoization er i gjennomsnitt {1/avg_ratio:.1f}x raskere enn tabulation"
            )
        else:
            print("   • ⚖️  Omtrent lik hastighet")
        print()

    # Konklusjon
    print("💡 KONKLUSJON:")
    if table_speedups:
        best_speedup = max(table_speedups) if table_speedups else 0
        print(
            f"   Dynamic programming (memo/table) gir opptil {best_speedup:.0f}x speedup vs naive rekursjon!"
        )

    if avg_ratio and len(memo_vs_table) > 5:
        if avg_ratio > 1.1:
            print(f"   For dette problemet er tabulation den raskeste tilnærmingen.")
        elif avg_ratio < 0.9:
            print(f"   For dette problemet er memoization den raskeste tilnærmingen.")
        else:
            print(f"   Memo og table har sammenlignbar ytelse for dette problemet.")

    print("\n" + "=" * 110 + "\n")


# endregion


# Kjør benchmark hvis du vil
# Uncomment linjen under for å kjøre benchmarken:
# benchmark_comparison()

# print(rodcut_table(20, [1, 2, 3, 7, 5, 6, 7]))


def rodcut_table_cost(n, p, k):
    table = [0 for _ in range(n + 1)]
    for i in range(0, n + 1):
        for j in range(1, min(len(p), i) + 1):
            table[i] = max(table[i], p[j - 1] + table[i - j] - k)
    return table[n]


def rodcut_memo_cost(n, p, k, memo):
    if n == 0:
        return 0
    elif n in memo.keys():
        return memo[n]
    best = float("-inf")
    for i in range(1, min(len(p), n) + 1):
        value = max(rodcut_memo_cost(n - i, p, k, memo) - k, 0) + p[i - 1]
        if value > best:
            best = value
    memo[n] = best
    return memo[n]
