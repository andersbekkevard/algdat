"""
Concrete 3-ary, 4-ary, and 5-ary max-heaps with duplicated logic.
Heaps use only a list A and an integer heap_size (CLRS style).
"""

INF = 10**18


# ------------------------------ 3-ary heap --------------------------------- #
def parent3(i: int) -> int:
    return (i - 1) // 3


def child3(i: int, k: int) -> int:
    return 3 * i + k


def ternary_max_heapify(A: list[int], heap_size: int, i: int) -> None:
    largest = i
    for k in (1, 2, 3):
        c = child3(i, k)
        if c < heap_size and A[c] > A[largest]:
            largest = c
    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        ternary_max_heapify(A, heap_size, largest)


def build_3ary_max_heap(A: list[int]) -> int:
    heap_size = len(A)
    for i in range((heap_size // 3), -1, -1):
        ternary_max_heapify(A, heap_size, i)
    return heap_size


def heap_extract_max_3ary(A: list[int], heap_size: int) -> tuple[int, int]:
    if heap_size < 1:
        raise IndexError("heap underflow")
    max_val = A[0]
    A[0] = A[heap_size - 1]
    A.pop()
    heap_size -= 1
    if heap_size > 0:
        ternary_max_heapify(A, heap_size, 0)
    return max_val, heap_size


def heap_increase_key_3ary(A: list[int], i: int, key: int) -> None:
    if key < A[i]:
        raise ValueError("new key is smaller than current key")
    A[i] = key
    while i > 0 and A[parent3(i)] < A[i]:
        p = parent3(i)
        A[i], A[p] = A[p], A[i]
        i = p


def max_heap_insert_3ary(A: list[int], heap_size: int, key: int) -> int:
    heap_size += 1
    A.append(-INF)
    heap_increase_key_3ary(A, heap_size - 1, key)
    return heap_size


# ------------------------------ 4-ary heap --------------------------------- #
def parent4(i: int) -> int:
    return (i - 1) // 4


def child4(i: int, k: int) -> int:
    return 4 * i + k


def quaternary_max_heapify(A: list[int], heap_size: int, i: int) -> None:
    largest = i
    for k in (1, 2, 3, 4):
        c = child4(i, k)
        if c < heap_size and A[c] > A[largest]:
            largest = c
    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        quaternary_max_heapify(A, heap_size, largest)


def build_4ary_max_heap(A: list[int]) -> int:
    heap_size = len(A)
    for i in range((heap_size // 4), -1, -1):
        quaternary_max_heapify(A, heap_size, i)
    return heap_size


def heap_extract_max_4ary(A: list[int], heap_size: int) -> tuple[int, int]:
    if heap_size < 1:
        raise IndexError("heap underflow")
    max_val = A[0]
    A[0] = A[heap_size - 1]
    A.pop()
    heap_size -= 1
    if heap_size > 0:
        quaternary_max_heapify(A, heap_size, 0)
    return max_val, heap_size


def heap_increase_key_4ary(A: list[int], i: int, key: int) -> None:
    if key < A[i]:
        raise ValueError("new key is smaller than current key")
    A[i] = key
    while i > 0 and A[parent4(i)] < A[i]:
        p = parent4(i)
        A[i], A[p] = A[p], A[i]
        i = p


def max_heap_insert_4ary(A: list[int], heap_size: int, key: int) -> int:
    heap_size += 1
    A.append(-INF)
    heap_increase_key_4ary(A, heap_size - 1, key)
    return heap_size


# ------------------------------ 5-ary heap --------------------------------- #
def parent5(i: int) -> int:
    return (i - 1) // 5


def child5(i: int, k: int) -> int:
    return 5 * i + k


def quinary_max_heapify(A: list[int], heap_size: int, i: int) -> None:
    largest = i
    for k in (1, 2, 3, 4, 5):
        c = child5(i, k)
        if c < heap_size and A[c] > A[largest]:
            largest = c
    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        quinary_max_heapify(A, heap_size, largest)


def build_5ary_max_heap(A: list[int]) -> int:
    heap_size = len(A)
    for i in range((heap_size // 5), -1, -1):
        quinary_max_heapify(A, heap_size, i)
    return heap_size


def heap_extract_max_5ary(A: list[int], heap_size: int) -> tuple[int, int]:
    if heap_size < 1:
        raise IndexError("heap underflow")
    max_val = A[0]
    A[0] = A[heap_size - 1]
    A.pop()
    heap_size -= 1
    if heap_size > 0:
        quinary_max_heapify(A, heap_size, 0)
    return max_val, heap_size


def heap_increase_key_5ary(A: list[int], i: int, key: int) -> None:
    if key < A[i]:
        raise ValueError("new key is smaller than current key")
    A[i] = key
    while i > 0 and A[parent5(i)] < A[i]:
        p = parent5(i)
        A[i], A[p] = A[p], A[i]
        i = p


def max_heap_insert_5ary(A: list[int], heap_size: int, key: int) -> int:
    heap_size += 1
    A.append(-INF)
    heap_increase_key_5ary(A, heap_size - 1, key)
    return heap_size


__all__ = [
    # 3-ary
    "parent3",
    "child3",
    "ternary_max_heapify",
    "build_3ary_max_heap",
    "heap_extract_max_3ary",
    "heap_increase_key_3ary",
    "max_heap_insert_3ary",
    # 4-ary
    "parent4",
    "child4",
    "quaternary_max_heapify",
    "build_4ary_max_heap",
    "heap_extract_max_4ary",
    "heap_increase_key_4ary",
    "max_heap_insert_4ary",
    # 5-ary
    "parent5",
    "child5",
    "quinary_max_heapify",
    "build_5ary_max_heap",
    "heap_extract_max_5ary",
    "heap_increase_key_5ary",
    "max_heap_insert_5ary",
]
