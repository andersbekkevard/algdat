import numpy as np


def insertion_sort(A, n):
    for i in range(1, n):
        x = A[i]
        j = i
        while j > 0 and A[j - 1] > x:
            A[j] = A[j - 1]
            j -= 1
        A[j] = x


def bucket_sort(A, n):
    """
    Ide:
    1. Lage en liste av lister med n bøtter
    2. Appende elementene til bøtte math.floor(A[i]*n)
    3. Sortere bøttene
    4. Konkatenere
    """
    B = [[] for _ in range(n)]
    for val in A:
        B[int(val * n)].append(val)
    for sublist in B:
        insertion_sort(sublist, len(sublist))
    return [x for sublist in B for x in sublist]


def general_bucket_sort(A, n, l, r):
    """
    Antar alle elementer lever i [l, r]
    """
    B = [[] for _ in range(n)]
    for val in A:
        normalized = (val - l) / (r - l)
        B[min(int(normalized * n), n - 1)].append(val)
    for sublist in B:
        insertion_sort(sublist, len(sublist))
    return [x for sublist in B for x in sublist]


np.random.seed(42)
A = np.random.randint(0, 100, 10)
print(list(A))
print(general_bucket_sort(A, 10, 0, 100))
