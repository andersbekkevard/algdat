from math import floor


def standard_counting_sort(A, n, k):
    B = [0] * n
    C = [0] * k
    for i in range(n):
        C[A[i]] = C[A[i]] + 1
    for i in range(1, k):
        C[i] = C[i] + C[i - 1]
    for i in range(n - 1, -1, -1):
        B[C[A[i]] - 1] = A[i]
        C[A[i]] -= 1
    return B


def counting_sort(A, n, k, digit):
    divisor = k**digit

    B = [0] * n
    C = [0] * k
    for i in range(n):
        x = (A[i] // divisor) % k
        C[x] += 1
    for i in range(1, k):
        C[i] += C[i - 1]
    for i in range(n - 1, -1, -1):
        x = (A[i] // divisor) % k
        B[C[x] - 1] = A[i]
        C[x] -= 1
    return B


def radix_sort(A, n, d, k):
    for i in range(d):
        A = counting_sort(A, n, k, i)
    return A


def is_sorted(A):
    for i in range(len(A) - 1):
        if A[i] > A[i + 1]:
            return False
    return True


def bucket_sort(A):
    """
    Assumes all elements are uniformly distributed on the interval [0,1)
    """
    n = len(A)
    B = [[] for _ in range(n)]
    for x in A:
        B[floor(x * n)].append(x)
    out = []
    for bucket in B:
        if bucket:
            insertion_sort(bucket, len(bucket))
            out.extend(bucket)
    return out


def insertion_sort(A, n):
    for i in range(1, n):
        key = A[i]
        j = i - 1
        while j >= 0 and A[j] > key:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = key


import numpy as np


def print_array(A, digits=3):
    print("[", end="")
    for i in range(len(A)):
        if i > 0:
            print(", ", end="")
        print(f"{A[i]:.{digits}f}", end="")
    print("]")


np.random.seed(42)
N = 10
A = list(np.random.rand(N))
print_array(A)
A = bucket_sort(A)
print_array(A)
