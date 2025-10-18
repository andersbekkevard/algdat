def partition(A, p, r):
    x = A[r]
    i = p - 1
    for j in range(p, r):
        if A[j] <= x:
            i += 1
            A[i], A[j] = A[j], A[i]
    i += 1
    A[i], A[r] = A[r], A[i]
    return i


def quicksort(A, p, r):
    if p >= r:
        return
    q = partition(A, p, r)
    quicksort(A, p, q-1)
    quicksort(A, q+1, r)


def randomized_quicksort


def quicksort_wrapper(A):
    """Wrapper function for easier testing"""
    if not A:
        return A
    quicksort(A, 0, len(A) - 1)
    return A


def test_quicksort():
    """Test suite for quicksort implementation"""
    test_cases = [
        # Empty list
        [],
        # Single element
        [1],
        # Two elements
        [2, 1],
        [1, 2],
        # Three elements
        [3, 2, 1],
        [1, 2, 3],
        [2, 1, 3],
        # Multiple elements
        [5, 2, 8, 1, 9],
        [9, 8, 7, 6, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [3, 1, 4, 1, 5, 9, 2, 6],
        # Duplicates
        [2, 2, 2, 2],
        [1, 2, 2, 3, 3, 3],
        # Negative numbers
        [-3, -1, -2, -5],
        [5, -2, 0, -1, 3],
        # Mixed types (integers)
        [10, 5, 15, 2, 8, 12],
    ]
    
    failed_count = 0
    
    for i, test_case in enumerate(test_cases):
        # Create a copy to avoid modifying the original
        test_array = test_case.copy()
        expected = sorted(test_case)
        result = quicksort_wrapper(test_array)
        
        if result != expected:
            print(f"failed instance: {test_case}")
            failed_count += 1
    
    if failed_count == 0:
        print("all succeeded")


if __name__ == "__main__":
    test_quicksort()

