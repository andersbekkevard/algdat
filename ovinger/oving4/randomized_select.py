import numpy as np


def rand_partition(A, p, r):
    q = np.random.randint(p, r)
    A[q], A[r] = A[r], A[q]
    return partition(A, p, r)


def partition(A, p, r):
    x = A[r]
    i = p
    for j in range(p, r):
        if A[j] < x:
            A[i], A[j] = A[j], A[i]
            i += 1
    A[i], A[r] = A[r], A[i]
    return i


def rand_sel(A, p, r, i):
    if p == r:
        return A[p]

    q = rand_partition(A, p, r)
    if q == i:
        return A[q]
    elif i < q:
        return rand_sel(A, p, q - 1, i)
    else:
        return rand_sel(A, q + 1, r, i - q)


A = [7, 14, 3, 19, 11, 2, 17, 8, 5, 13]
print(rand_sel(A, 0, len(A) - 1, 3))
A.sort()
print(A)
