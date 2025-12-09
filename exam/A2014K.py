#!/usr/bin/python3
# coding=utf-8
import random
from math import comb

# Simple boilerplate to let you implement the counting-subsequence task yourself.
# toggle random tests if you like
generate_random_tests = True
random_tests = 5
seed = 1  # set 0 for new random each run


def solve(A, B):
    """
    Return how many times sequence A appears as a subsequence of sequence B.
    """
    n = len(A)
    m = len(B)
    if m < n:
        return 0

    # Calculate in-row-array for A
    in_row_a = [0] * n
    c = ""
    count = 0
    for i in range(n):
        if A[i] == c:
            count += 1
        else:
            count = 1
            c = A[i]

        in_row_a[i] = count

    # Calculate in-row-array for B
    c = ""
    count = 0
    in_row_b = [0] * m
    for j in range(m):
        if B[j] == c:
            count += 1
        else:
            count = 1
            c = B[j]

        in_row_b[j] = count

    dp = [[0] * (n + 1) for _ in range(m + 1)]
    dp[0] = [1] * (n + 1)
    for i in range(n):
        for j in range(m):
            # Remember that the dp table now is one-indexed, but the strings are 0-indexed

            if A[i] != B[j]:
                # If the new one didnt match, no new information, and its the same as with one less letter to work with
                dp[i + 1][j + 1] = dp[i + 1][j]

            elif dp[i + 1][j - 1] == 0 and A[i] == B[j]:
                # if the previous one was zero, but this new letter matched, it is the same as for one shorter A
                dp[i + 1][j + 1] = dp[i][j]

            else:
                # in this situation, we know that we got a match with one less j. This new one also matches.
                # Using the in_row_arrays, we find the number of in rows for both A and B. We then find how many matches
                # we had before these in rows, and multiply it by the binomal coefficient
                p = in_row_a[i]
                q = in_row_b[j]
                new_char_i = i - p
                new_char_j = j - q
                dp[i + 1][j + 1] = comb(q, p) * dp[new_char_i + 1][new_char_j + 1]

    return dp[n][m]


def solve_memo(A, B):
    """
    Top-down memoization solution for counting subsequences.

    count(i, j) = number of ways to form A[i:] as a subsequence of B[j:]

    Recurrence:
    - Base case: if i == len(A), we've matched all of A → return 1
    - Base case: if j == len(B) but i < len(A), B is exhausted → return 0
    - If A[i] != B[j]: skip B[j], count(i, j) = count(i, j+1)
    - If A[i] == B[j]: either use B[j] to match A[i], or skip B[j]
        count(i, j) = count(i+1, j+1) + count(i, j+1)
    """
    n, m = len(A), len(B)
    memo = {}

    def count(i, j):
        # Base case: matched all of A
        if i == n:
            return 1
        # Base case: B exhausted but A not fully matched
        if j == m:
            return 0

        if (i, j) in memo:
            return memo[(i, j)]

        if A[i] != B[j]:
            # Characters don't match, skip B[j]
            result = count(i, j + 1)
        else:
            # Characters match: use B[j] OR skip B[j]
            result = count(i + 1, j + 1) + count(i, j + 1)

        memo[(i, j)] = result
        return result

    return count(0, 0)


def solve_correct(A, B):
    n = len(A)
    m = len(B)

    # dp[i][j] stores the number of ways to form A[:i] using B[:j]
    # Dimensions are (n+1) x (m+1)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Base case: An empty A is a subsequence of any B exactly 1 time (by deleting all chars in B)
    for j in range(m + 1):
        dp[0][j] = 1

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # If characters don't match, discard B's current char
            if A[i - 1] != B[j - 1]:
                dp[i][j] = dp[i][j - 1]
            else:
                # If they match:
                # (Ways without using B[j]) + (Ways using B[j] to match A[i])
                dp[i][j] = dp[i][j - 1] + dp[i - 1][j - 1]

    return dp[n][m]


def get_feedback(student_answer, expected):
    return (
        None
        if student_answer == expected
        else (f"Feil svar. Ditt: {student_answer}, forventet: {expected}")
    )


# Hand-made tiny cases: (A, B, expected, description)
tests = [
    ([], [], 1, "Tom i tom (1 måte)"),
    ([], [1, 2, 3], 1, "Tom A i ikke-tom B (alltid 1)"),
    ([1], [1], 1, "Enkelt match"),
    ([1], [1, 1, 1], 3, "Enkelt element flere ganger"),
    ([1, 2], [1, 2, 1, 2], 3, "Flere kombinasjoner"),
    ([2, 2], [2, 2, 2], 3, "Duplikater"),
    ([1, 2, 3], [1, 2], 0, "For kort B"),
]


def generate_random_test():
    if seed != 0:
        random.seed(seed)
    n = random.randint(0, 6)
    k = random.randint(0, n)
    B = [random.randint(0, 3) for _ in range(n)]
    A = random.sample(B, k) if k <= len(B) else B[:]

    # Simple reference via DP for expected (ok for small sizes)
    dp = [1] + [0] * len(A)
    for b in B:
        for i in range(len(A) - 1, -1, -1):
            if A[i] == b:
                dp[i + 1] += dp[i]
    expected = dp[len(A)]
    return A, B, expected, f"Tilfeldig (n={n}, k={len(A)})"


if __name__ == "__main__":
    failed = False
    all_tests = list(tests)
    if generate_random_tests:
        for _ in range(random_tests):
            all_tests.append(generate_random_test())

    for i, (A, B, expected, desc) in enumerate(all_tests, 1):
        try:
            student_answer = solve(A, B)
        except NotImplementedError:
            print("Du må implementere solve() før du kjører testene.")
            break
        except Exception as e:
            failed = True
            print(f"Test {i} feilet med unntak ({desc}): {e}")
            continue

        feedback = get_feedback(student_answer, expected)
        if feedback:
            failed = True
            print(f"Test {i} feilet: {desc}\nA={A}, B={B}\n{feedback}\n")

    if not failed:
        print(f"Koden fungerte for alle {len(all_tests)} testene! ✓")
