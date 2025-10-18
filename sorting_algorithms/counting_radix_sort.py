import numpy as np


def counting_sort(A, n, k):
    B, C = [0] * n, [0] * k
    for i in range(n):
        C[A[i]] = C[A[i]] + 1
    for i in range(1, k):
        C[i] = C[i] + C[i - 1]
    for i in range(n - 1, -1, -1):
        val = A[i]
        B[C[val] - 1] = val
        C[val] = C[val] - 1
    return B


def counting_sort_by_digit(A, n, k, d):
    """
    Stable counting sort of A by the d-th digit (0 = least significant).
    A: list of integers
    n: length of A
    k: base (number of possible digit values, e.g. 10 for decimal)
    d: digit index (0 = least significant)
    """
    B = [0] * n
    C = [0] * k

    for i in range(n):
        digit = (A[i] // (k**d)) % k
        C[digit] = C[digit] + 1

    for i in range(1, k):
        C[i] = C[i] + C[i - 1]

    for i in range(n - 1, -1, -1):
        digit = (A[i] // (k**d)) % k
        B[C[digit] - 1] = A[i]
        C[digit] = C[digit] - 1

    return B


n = 10
k = 5

np.random.seed(42)
A = list(np.random.randint(0, k, n))
print(A)
print(counting_sort(A, n, k))


def radix_sort(A, n, d):
    for i in range(0, d):
        A = counting_sort_by_digit(A, n, k, i)
    return A


print(radix_sort(A, n, 2))
