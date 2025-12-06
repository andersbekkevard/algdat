from heap.more_variants import (
    FibonacciHeap,
    build_3ary_max_heap,
    build_4ary_max_heap,
    build_5ary_max_heap,
    build_max_heap,
    heap_extract_max,
    heap_extract_max_3ary,
    heap_extract_max_4ary,
    heap_extract_max_5ary,
    max_heap_insert,
    max_heap_insert_3ary,
    max_heap_insert_4ary,
    max_heap_insert_5ary,
)


def test_binary_heap_extracts_descending():
    data = [5, 3, 8, 1, 9, 4, 7]
    A = list(data)
    heap_size = build_max_heap(A)
    extracted = []
    for _ in range(heap_size):
        x, heap_size = heap_extract_max(A, heap_size)
        extracted.append(x)
    assert extracted == sorted(data, reverse=True)


def test_dary_heaps_extract_descending():
    data = [7, 2, 6, 4, 9, 1, 8, 5]
    # 3-ary
    A3 = list(data)
    hs3 = build_3ary_max_heap(A3)
    extracted3 = []
    for _ in range(hs3):
        x, hs3 = heap_extract_max_3ary(A3, hs3)
        extracted3.append(x)
    assert extracted3 == sorted(data, reverse=True)

    # 4-ary
    A4 = list(data)
    hs4 = build_4ary_max_heap(A4)
    extracted4 = []
    for _ in range(hs4):
        x, hs4 = heap_extract_max_4ary(A4, hs4)
        extracted4.append(x)
    assert extracted4 == sorted(data, reverse=True)

    # 5-ary
    A5 = list(data)
    hs5 = build_5ary_max_heap(A5)
    extracted5 = []
    for _ in range(hs5):
        x, hs5 = heap_extract_max_5ary(A5, hs5)
        extracted5.append(x)
    assert extracted5 == sorted(data, reverse=True)


def test_fibonacci_heap_extract_and_decrease_key():
    values = [7, 3, 18, 38, 24, 17, 23, 52]
    H = FibonacciHeap()
    nodes = [H.insert(v) for v in values]
    H.decrease_key(nodes[2], 2)  # 18 -> 2
    extracted = [H.extract_min().key for _ in range(H.n)]
    assert extracted == sorted([2, 3, 7, 17, 23, 24, 38, 52])
