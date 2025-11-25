def max_heapify(A, n, i):
    l = 2 * i + 1
    r = 2 * i + 2
    m = i
    if l < n and A[l] > A[m]:
        m = l
    if r < n and A[r] > A[m]:
        m = r
    if m != i:
        A[i], A[m] = A[m], A[i]
        max_heapify(A, n, m)


def heapsort(A, n):
    if n <= 1:
        return

    # build heap
    # we know that n//2 nodes are internal, the rest are already heaps
    for i in range((n - 2) // 2, -1, -1):
        max_heapify(A, n, i)

    # extract max
    for i in range(n - 1, -1, -1):
        A[0], A[i] = A[i], A[0]
        max_heapify(A, i, 0)


def extract_max(A, n):
    A[0], A[n - 1] = A[n - 1], A[0]
    max_heapify(A, n - 1, 0)
    return A.pop()
