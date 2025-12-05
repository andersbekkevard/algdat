from random import randint as rnd
import random


def randomized_partition(A, p, r):
    q = rnd(p, r)
    A[q], A[r] = A[r], A[q]
    return partition(A, p, r)


def partition(A, p, r):
    x = A[r]
    j = p
    for i in range(p, r):
        if A[i] < x:
            A[j], A[i] = A[i], A[j]
            j += 1
    A[j], A[r] = A[r], A[j]
    return j


def quicksort(A, p, r):
    if p >= r:
        return
    q = randomized_partition(A, p, r)
    quicksort(A, p, q - 1)
    quicksort(A, q + 1, r)


def randomized_select(A, p, r, i):
    """
    Finds the i-th order variable (1-indexed) and returns it
    """
    if p >= r:
        return A[p]
    q = randomized_partition(A, p, r)
    k = q - p + 1
    if k == i:
        return A[q]
    elif i < k:
        return randomized_select(A, p, q - 1, i)
    else:
        return randomized_select(A, q + 1, r, i - k)


A = [5, 5, 5, 5, 53, 3, 3, 2]
n = len(A)
print(A)
x = randomized_select(A, 0, n - 1, 1)
print(x)
print(A)
