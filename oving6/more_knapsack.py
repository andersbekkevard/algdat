#!/usr/bin/python3
# coding=utf-8

large_tests = False


def unlimited_knapsack(weights, values, capacity):
    return solve_unlimited(dict(), weights, values, len(weights), capacity)


def solve_unlimited(mem, wgt, vals, n, W):
    if (n, W) in mem:
        return mem[(n, W)]
    if n == 0 or W == 0:
        result = 0
    elif wgt[n - 1] > W:
        result = solve_unlimited(mem, wgt, vals, n - 1, W)
    else:
        exclude = solve_unlimited(mem, wgt, vals, n - 1, W)
        include = solve_unlimited(mem, wgt, vals, n, W - wgt[n - 1]) + vals[n - 1]

        result = max(exclude, include)
    mem[(n, W)] = result
    return result


tests = [
    ([2, 3, 4, 5], [3, 4, 5, 6], 5, 7),
    ([1, 2, 3], [6, 10, 12], 5, 30),
    ([10, 20, 30], [60, 100, 120], 50, 300),
    ([5, 4, 6, 3], [10, 40, 30, 50], 10, 150),
    ([2, 2, 2, 2], [5, 5, 5, 5], 4, 10),
    ([1], [10], 1, 10),
    ([1, 2], [1, 2], 1, 1),
    ([3, 4, 5], [30, 50, 60], 8, 100),
    ([1, 3, 4, 5], [1, 4, 5, 7], 7, 9),
    ([2, 3, 4, 5], [3, 4, 5, 6], 0, 0),
    ([1, 3], [10, 20], 3, 30),
    ([2, 5], [15, 30], 10, 75),
]

if large_tests:
    tests += [
        ([7, 3, 4, 5, 6, 8, 2, 9, 1], [10, 5, 6, 8, 12, 15, 3, 18, 2], 20, 200),
        ([10, 15, 20, 25, 30], [100, 90, 120, 80, 70], 40, 400),
        ([5, 10, 15, 20, 25], [50, 60, 70, 80, 90], 50, 500),
        (
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 5, 8, 9, 10, 17, 17, 20, 24, 30],
            25,
            250,
        ),
        ([2, 3, 5, 7, 11, 13], [5, 8, 14, 20, 30, 35], 20, 50),
        ([4, 5, 6, 7, 8, 9, 10], [8, 10, 12, 14, 16, 18, 20], 30, 60),
        ([3, 4, 5, 6, 7, 8], [6, 8, 10, 12, 14, 16], 18, 36),
        ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2], 5, 10),
        ([5, 5, 5, 5, 5], [10, 10, 10, 10, 10], 12, 20),
        ([8, 9, 10, 11, 12], [16, 18, 20, 22, 24], 25, 48),
    ]

failed = False
for weights, values, capacity, answer in tests:
    student = unlimited_knapsack(weights, values, capacity)
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
