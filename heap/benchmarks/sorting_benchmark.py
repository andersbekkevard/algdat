"""
Benchmark: Heapsort vs Mergesort vs Quicksort
Goal: Visualize the constant factor in O(n log n) by computing time / (n * log2(n))
"""

import random
import time
import math
from typing import Callable


# =======================
# HEAPSORT (in-place)
# =======================
def heapsort(A: list[int], n: int):
    if n <= 1:
        return

    def max_heapify(i: int, size: int):
        greatest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < size and A[l] > A[greatest]:
            greatest = l
        if r < size and A[r] > A[greatest]:
            greatest = r
        if greatest != i:
            A[i], A[greatest] = A[greatest], A[i]
            max_heapify(greatest, size)

    # Build max-heap (bottom-up)
    for i in range((n - 2) // 2, -1, -1):
        max_heapify(i, n)

    # Extract elements one by one
    for heap_size in range(n - 1, 0, -1):
        A[0], A[heap_size] = A[heap_size], A[0]
        max_heapify(0, heap_size)


# =======================
# MERGESORT (uses auxiliary space, but same style)
# =======================
def mergesort(A: list[int], n: int):
    if n <= 1:
        return

    aux = [0] * n  # Pre-allocate auxiliary array once

    def merge(lo: int, mid: int, hi: int):
        # Copy to aux
        for k in range(lo, hi + 1):
            aux[k] = A[k]

        i, j = lo, mid + 1
        for k in range(lo, hi + 1):
            if i > mid:
                A[k] = aux[j]
                j += 1
            elif j > hi:
                A[k] = aux[i]
                i += 1
            elif aux[i] <= aux[j]:
                A[k] = aux[i]
                i += 1
            else:
                A[k] = aux[j]
                j += 1

    def sort(lo: int, hi: int):
        if lo >= hi:
            return
        mid = lo + (hi - lo) // 2
        sort(lo, mid)
        sort(mid + 1, hi)
        merge(lo, mid, hi)

    sort(0, n - 1)


# =======================
# QUICKSORT (in-place, median-of-three pivot)
# =======================
def quicksort(A: list[int], n: int):
    if n <= 1:
        return

    def median_of_three(lo: int, hi: int) -> int:
        mid = lo + (hi - lo) // 2
        # Sort lo, mid, hi and return mid as pivot index
        if A[lo] > A[mid]:
            A[lo], A[mid] = A[mid], A[lo]
        if A[lo] > A[hi]:
            A[lo], A[hi] = A[hi], A[lo]
        if A[mid] > A[hi]:
            A[mid], A[hi] = A[hi], A[mid]
        return mid

    def partition(lo: int, hi: int) -> int:
        # Use median-of-three for pivot selection
        pivot_idx = median_of_three(lo, hi)
        A[pivot_idx], A[hi] = A[hi], A[pivot_idx]  # Move pivot to end
        pivot = A[hi]

        i = lo - 1
        for j in range(lo, hi):
            if A[j] <= pivot:
                i += 1
                A[i], A[j] = A[j], A[i]
        A[i + 1], A[hi] = A[hi], A[i + 1]
        return i + 1

    def sort(lo: int, hi: int):
        if lo >= hi:
            return
        p = partition(lo, hi)
        sort(lo, p - 1)
        sort(p + 1, hi)

    sort(0, n - 1)


# =======================
# BENCHMARKING
# =======================
def benchmark_sort(
    sort_func: Callable[[list[int], int], None],
    sizes: list[int],
    trials: int = 5,
    seed: int = 42,
) -> dict[int, float]:
    """
    Benchmark a sorting function across different sizes.
    Returns dict mapping size -> average time in seconds.
    """
    results = {}

    for n in sizes:
        times = []
        for trial in range(trials):
            # Generate fresh random data each trial
            random.seed(seed + trial)
            data = [random.randint(0, n * 10) for _ in range(n)]

            # Time only the sort
            start = time.perf_counter()
            sort_func(data, n)
            end = time.perf_counter()

            times.append(end - start)

        results[n] = sum(times) / len(times)

    return results


def compute_constant(size: int, time_sec: float) -> float:
    """Compute the constant factor: time / (n * log2(n))"""
    if size <= 1:
        return 0.0
    return time_sec / (size * math.log2(size))


def print_results(results: dict[str, dict[int, float]], sizes: list[int]):
    """Pretty print the benchmark results with constant factors."""

    # Header
    print("\n" + "=" * 90)
    print(f"{'SIZE':>12} | {'HEAPSORT':>18} | {'MERGESORT':>18} | {'QUICKSORT':>18}")
    print(
        f"{'':>12} | {'time (ms)':>8} {'const':>8} | {'time (ms)':>8} {'const':>8} | {'time (ms)':>8} {'const':>8}"
    )
    print("=" * 90)

    for n in sizes:
        heap_t = results["heapsort"][n]
        merge_t = results["mergesort"][n]
        quick_t = results["quicksort"][n]

        heap_c = compute_constant(n, heap_t)
        merge_c = compute_constant(n, merge_t)
        quick_c = compute_constant(n, quick_t)

        # Time in milliseconds, constant in nanoseconds (more readable)
        print(
            f"{n:>12,} | {heap_t*1000:>8.3f} {heap_c*1e9:>8.2f} | "
            f"{merge_t*1000:>8.3f} {merge_c*1e9:>8.2f} | "
            f"{quick_t*1000:>8.3f} {quick_c*1e9:>8.2f}"
        )

    print("=" * 90)
    print("Note: 'const' = time / (n * log2(n)) in nanoseconds")
    print("      A stable constant across sizes confirms O(n log n) behavior")
    print()

    # Compute average constants (excluding smallest sizes)
    large_sizes = [n for n in sizes if n >= 1000]
    if large_sizes:
        avg_heap = (
            sum(compute_constant(n, results["heapsort"][n]) for n in large_sizes)
            / len(large_sizes)
            * 1e9
        )
        avg_merge = (
            sum(compute_constant(n, results["mergesort"][n]) for n in large_sizes)
            / len(large_sizes)
            * 1e9
        )
        avg_quick = (
            sum(compute_constant(n, results["quicksort"][n]) for n in large_sizes)
            / len(large_sizes)
            * 1e9
        )

        print("Average constants (for n >= 1000):")
        print(f"  Heapsort:  {avg_heap:.2f} ns")
        print(f"  Mergesort: {avg_merge:.2f} ns")
        print(f"  Quicksort: {avg_quick:.2f} ns")

        fastest = min(avg_heap, avg_merge, avg_quick)
        print(f"\nRelative to fastest:")
        print(f"  Heapsort:  {avg_heap/fastest:.2f}x")
        print(f"  Mergesort: {avg_merge/fastest:.2f}x")
        print(f"  Quicksort: {avg_quick/fastest:.2f}x")


def main():
    # Test sizes: from small to large
    sizes = [100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000]

    # Increase recursion limit for large arrays
    import sys

    sys.setrecursionlimit(100_000)

    print("Benchmarking sorting algorithms...")
    print(f"Sizes: {sizes}")
    print(f"Trials per size: 5")
    print()

    # Run benchmarks
    print("Running heapsort...", end=" ", flush=True)
    heap_results = benchmark_sort(heapsort, sizes)
    print("done")

    print("Running mergesort...", end=" ", flush=True)
    merge_results = benchmark_sort(mergesort, sizes)
    print("done")

    print("Running quicksort...", end=" ", flush=True)
    quick_results = benchmark_sort(quicksort, sizes)
    print("done")

    results = {
        "heapsort": heap_results,
        "mergesort": merge_results,
        "quicksort": quick_results,
    }

    print_results(results, sizes)


if __name__ == "__main__":
    main()
