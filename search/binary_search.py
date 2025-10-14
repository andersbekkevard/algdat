import time
import random

"""
Binary search

A is a sorted array
p is the start index
r is the end index
v is the value to search for

Returns the index of the value in the array
"""


def bisect_recursive(A, p, r, v):
    if p > r:
        return None

    q = p + (r - p) // 2
    pivot = A[q]
    if pivot == v:
        return q
    elif v < pivot:
        return bisect_recursive(A, p, q - 1, v)
    else:
        return bisect_recursive(A, q + 1, r, v)
    
def bisect_iterative(A, p, r, v):
    while p <= r:
        q = p + (r - p) // 2
        pivot = A[q]
        if pivot == v:
            return q
        elif v < pivot:
            r = q - 1
        else:
            p = q + 1
    return None


def verify_bisect(binary_search_function):
    print(f"Verifying {binary_search_function.__name__}")
    x = binary_search_function([1, 2, 3, 3, 4, 5], 0, 4, 3)
    print(x)
    # Edge case tests for bisect_recursive

    # Empty array
    assert binary_search_function([], 0, -1, 1) is None, "Empty array should return None"

    # Single element, value present
    assert binary_search_function([5], 0, 0, 5) == 0, "Single element present should return 0"

    # Single element, value absent
    assert (
        binary_search_function([5], 0, 0, 3) is None
    ), "Single element absent should return None"

    # Value at the start
    assert binary_search_function([2, 3, 4, 5], 0, 3, 2) == 0, "Value at start should return 0"

    # Value at the end
    assert binary_search_function([2, 3, 4, 5], 0, 3, 5) == 3, "Value at end should return 3"

    # Value not present, in range
    assert (
        binary_search_function([1, 3, 5, 7], 0, 3, 4) is None
    ), "Value not present should return None"

    # All elements the same, value present
    assert binary_search_function([2, 2, 2, 2], 0, 3, 2) in [
        0,
        1,
        2,
        3,
    ], "All same, value present should return valid index"

    # All elements the same, value absent
    assert (
        binary_search_function([2, 2, 2, 2], 0, 3, 3) is None
    ), "All same, value absent should return None"

    # Negative numbers
    assert (
        binary_search_function([-5, -3, -1, 0, 2], 0, 4, -3) == 1
    ), "Negative number present should return correct index"

    # Large indices
    large_arr = list(range(10000))
    assert binary_search_function(large_arr, 0, 9999, 9999) == 9999, "Large array, value at end"

    print("All edge case tests passed.")





def benchmark_binary_search():
    """Benchmark recursive vs iterative binary search implementations."""
    
    # Test configurations: (array_size, num_searches)
    test_configs = [
        (100, 1000),
        (1000, 1000),
        (10000, 1000),
        (100000, 1000),
        (1000000, 1000)
    ]
    
    print("=" * 80)
    print("BINARY SEARCH PERFORMANCE BENCHMARK")
    print("=" * 80)
    print(f"{'Array Size':<12} {'Searches':<10} {'Recursive (s)':<15} {'Iterative (s)':<15} {'Speedup':<10}")
    print("-" * 80)
    
    for array_size, num_searches in test_configs:
        # Create sorted array
        arr = sorted([random.randint(1, array_size * 2) for _ in range(array_size)])
        
        # Generate search values (mix of present and absent)
        search_values = []
        for _ in range(num_searches):
            if random.random() < 0.7:  # 70% chance value exists
                search_values.append(random.choice(arr))
            else:  # 30% chance value doesn't exist
                search_values.append(random.randint(1, array_size * 2))
        
        # Benchmark recursive version
        start_time = time.time()
        for val in search_values:
            bisect_recursive(arr, 0, len(arr) - 1, val)
        recursive_time = time.time() - start_time
        
        # Benchmark iterative version
        start_time = time.time()
        for val in search_values:
            bisect_iterative(arr, 0, len(arr) - 1, val)
        iterative_time = time.time() - start_time
        
        # Calculate speedup
        speedup = recursive_time / iterative_time if iterative_time > 0 else float('inf')
        
        # Print results
        print(f"{array_size:<12} {num_searches:<10} {recursive_time:<15.6f} {iterative_time:<15.6f} {speedup:<10.2f}x")
    
    print("-" * 80)
    print("Note: Higher speedup means iterative is faster")
    print("=" * 80)


if __name__ == "__main__":
    # benchmark_binary_search()
    verify_bisect(bisect_recursive)
    verify_bisect(bisect_iterative)
