"""
Additional heap implementations inspired by CLRS (Cormen, Leiserson, Rivest,
and Stein). This package intentionally does not reuse the simpler heap
implementations elsewhere in the repository so each variant is self contained.
"""

from .binary_heap import (
    build_max_heap,
    heap_extract_max,
    heap_increase_key,
    heap_maximum,
    max_heap_insert,
    max_heapify,
)
from .d_ary_heap import (
    build_3ary_max_heap,
    build_4ary_max_heap,
    build_5ary_max_heap,
    heap_extract_max_3ary,
    heap_extract_max_4ary,
    heap_extract_max_5ary,
    heap_increase_key_3ary,
    heap_increase_key_4ary,
    heap_increase_key_5ary,
    max_heap_insert_3ary,
    max_heap_insert_4ary,
    max_heap_insert_5ary,
    quaternary_max_heapify,
    quinary_max_heapify,
    ternary_max_heapify,
)
from .fibonacci_heap import FibNode, FibonacciHeap

__all__ = [
    # Binary heap
    "max_heapify",
    "build_max_heap",
    "heap_maximum",
    "heap_extract_max",
    "heap_increase_key",
    "max_heap_insert",
    # 3-ary heap
    "ternary_max_heapify",
    "build_3ary_max_heap",
    "heap_extract_max_3ary",
    "heap_increase_key_3ary",
    "max_heap_insert_3ary",
    # 4-ary heap
    "quaternary_max_heapify",
    "build_4ary_max_heap",
    "heap_extract_max_4ary",
    "heap_increase_key_4ary",
    "max_heap_insert_4ary",
    # 5-ary heap
    "quinary_max_heapify",
    "build_5ary_max_heap",
    "heap_extract_max_5ary",
    "heap_increase_key_5ary",
    "max_heap_insert_5ary",
    # Fibonacci heap
    "FibonacciHeap",
    "FibNode",
]
