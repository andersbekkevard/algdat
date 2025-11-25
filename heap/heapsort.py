import random
from random import randint as rnd

# Want to improve by using the max-heapify building method instead


def heapsort(A: list[int], n: int):
    if n <= 1:
        return

    def max_heapify(A: list[int], size: int, i: int):
        greatest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < size and A[l] > A[greatest]:
            greatest = l
        if r < size and A[r] > A[greatest]:
            greatest = r

        if greatest != i:
            A[i], A[greatest] = A[greatest], A[i]
            max_heapify(A, size, greatest)

    # build heap with max-heapify
    # Bottom layers are already heaps
    # Calling max heapify from first internal node and up
    for i in range((n - 2) // 2, -1, -1):
        max_heapify(A, n, i)

    for heap_size in range(n - 1, 0, -1):
        A[0], A[heap_size] = A[heap_size], A[0]
        max_heapify(A, heap_size, 0)

    # -- is sorted in place --


random.seed(42)
LOWER = 1
UPPER = 20
N = 10
A = [rnd(LOWER, UPPER) for _ in range(N)]
print(A)
heapsort(A, N)
print(A)
