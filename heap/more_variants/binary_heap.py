"""
Binary max-heap using only a list A and an integer heap_size,
mirroring the CLRS pseudocode style.
"""

INF = 10**18


def parent(i: int) -> int:
    return (i - 1) // 2


def left(i: int) -> int:
    return 2 * i + 1


def right(i: int) -> int:
    return 2 * i + 2


def max_heapify(A: list[int], heap_size: int, i: int) -> None:
    l = left(i)
    r = right(i)
    largest = i
    if l < heap_size and A[l] > A[largest]:
        largest = l
    if r < heap_size and A[r] > A[largest]:
        largest = r
    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        max_heapify(A, heap_size, largest)


def build_max_heap(A: list[int]) -> int:
    heap_size = len(A)
    for i in range((heap_size // 2) - 1, -1, -1):
        max_heapify(A, heap_size, i)
    return heap_size


def heap_maximum(A: list[int], heap_size: int) -> int:
    if heap_size == 0:
        raise IndexError("heap_maximum on empty heap")
    return A[0]


def heap_extract_max(A: list[int], heap_size: int) -> tuple[int, int]:
    if heap_size < 1:
        raise IndexError("heap underflow")
    max_val = A[0]
    A[0] = A[heap_size - 1]
    A.pop()
    heap_size -= 1
    if heap_size > 0:
        max_heapify(A, heap_size, 0)
    return max_val, heap_size


def heap_increase_key(A: list[int], i: int, key: int) -> None:
    if key < A[i]:
        raise ValueError("new key is smaller than current key")
    A[i] = key
    while i > 0 and A[parent(i)] < A[i]:
        p = parent(i)
        A[i], A[p] = A[p], A[i]
        i = p


def max_heap_insert(A: list[int], heap_size: int, key: int) -> int:
    heap_size += 1
    A.append(-INF)
    heap_increase_key(A, heap_size - 1, key)
    return heap_size


__all__ = [
    "parent",
    "left",
    "right",
    "max_heapify",
    "build_max_heap",
    "heap_maximum",
    "heap_extract_max",
    "heap_increase_key",
    "max_heap_insert",
]
