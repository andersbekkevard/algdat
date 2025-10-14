from random import randint as rnd

def partition(A, p, r):
    x = A[r]
    i = p - 1
    for j in range(p, r):
        if A[j] <= x:
            i += 1
            A[j], A[i] = A[i], A[j]
    i += 1
    A[i], A[r] = A[r], A[i]
    return i


def randomized_partition(A, p, r):
    q = rnd(p, r)
    A[q], A[r] = A[r], A[q]
    return partition(A, p, r)



def randomized_select(A, p, r, i):
    # returns the ith largest element (1-indexed)
    if p == r:
        return A[p]
    
    q = randomized_partition(A, p, r)
    k = q - p + 1  # number of elements in left partition + pivot
    
    if i == k:
        return A[q]
    elif i < k:
        return randomized_select(A, p, q - 1, i)
    else:
        return randomized_select(A, q + 1, r, i - k)
    

def partition_around_pivot(A, p, r, pivot_idx):
    """Partition array around a specific pivot element"""
    # Move pivot to end
    A[pivot_idx], A[r] = A[r], A[pivot_idx]
    return partition(A, p, r)


def insertion_sort(A, p, r):
    """Sort subarray A[p:r+1] using insertion sort"""
    for i in range(p + 1, r + 1):
        key = A[i]
        j = i - 1
        while j >= p and A[j] > key:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = key


def median_of_medians(A, p, r):
    """Find a good pivot using median-of-medians algorithm"""
    n = r - p + 1
    
    # Base case: if small enough, just sort and return median
    if n <= 5:
        insertion_sort(A, p, r)
        return p + n // 2
    
    # Divide into groups of 5 and find median of each group
    num_groups = (n + 4) // 5  # Ceiling division
    medians_start = p
    
    for i in range(num_groups):
        group_start = p + i * 5
        group_end = min(group_start + 4, r)
        
        # Sort the group
        insertion_sort(A, group_start, group_end)
        
        # Find median of this group
        median_idx = group_start + (group_end - group_start) // 2
        
        # Move median to beginning of array (to collect all medians)
        A[medians_start + i], A[median_idx] = A[median_idx], A[medians_start + i]
    
    # Recursively find median of medians
    median_of_medians_idx = medians_start + num_groups // 2
    select(A, medians_start, medians_start + num_groups - 1, num_groups // 2 + 1)
    
    return medians_start + num_groups // 2


def select(A, p, r, i):
    """
    Deterministic linear-time selection using median-of-medians.
    Returns the ith smallest element (1-indexed) in A[p:r+1].
    """
    if p == r:
        return A[p]
    
    # Find a good pivot using median-of-medians
    pivot_idx = median_of_medians(A, p, r)
    
    # Partition around this pivot
    q = partition_around_pivot(A, p, r, pivot_idx)
    k = q - p + 1  # number of elements in left partition + pivot
    
    if i == k:
        return A[q]
    elif i < k:
        return select(A, p, q - 1, i)
    else:
        return select(A, q + 1, r, i - k)


def test_partition(partition_function):
    print(f"Testing {partition_function.__name__}")
    # Test 1: Basic case
    A = [3, 2, 1, 5, 4]
    q = partition_function(A, 0, len(A) - 1)
    pivot = A[q]
    assert all(x <= pivot for x in A[:q])
    assert all(x > pivot for x in A[q + 1:])

    # Test 2: Already sorted
    A = [1, 2, 3, 4, 5]
    q = partition_function(A, 0, len(A) - 1)
    pivot = A[q]
    assert all(x <= pivot for x in A[:q])
    assert all(x > pivot for x in A[q + 1:])

    # Test 3: Reverse sorted
    A = [5, 4, 3, 2, 1]
    q = partition_function(A, 0, len(A) - 1)
    pivot = A[q]
    assert all(x <= pivot for x in A[:q])
    assert all(x > pivot for x in A[q + 1:])

    # Test 4: All equal elements
    A = [7, 7, 7, 7, 7]
    q = partition_function(A, 0, len(A) - 1)
    pivot = A[q]
    assert all(x == pivot for x in A)
    assert 0 <= q < len(A)

    # Test 5: Single element
    A = [10]
    q = partition_function(A, 0, 0)
    assert q == 0
    assert A == [10]

    # Test 6: Pivot in middle
    A = [4, 9, 3, 8, 6]
    q = partition_function(A, 0, len(A) - 1)
    pivot = A[q]
    assert all(x <= pivot for x in A[:q])
    assert all(x > pivot for x in A[q + 1:])

    print("All partition tests passed.")


def test_select(select_function):
    print(f"Testing {select_function.__name__}")
    
    # Test 1: Basic selection - find smallest element (i=1)
    A = [3, 1, 4, 1, 5, 9, 2, 6]
    result = select_function(A.copy(), 0, len(A) - 1, 1)
    expected = min(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 2: Find largest element (i=n)
    A = [3, 1, 4, 1, 5, 9, 2, 6]
    result = select_function(A.copy(), 0, len(A) - 1, len(A))
    expected = max(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 3: Find median (i=n//2 + 1)
    A = [3, 1, 4, 1, 5, 9, 2, 6]
    sorted_A = sorted(A)
    median_index = len(A) // 2  # 0-indexed median
    result = select_function(A.copy(), 0, len(A) - 1, len(A) // 2 + 1)
    expected = sorted_A[median_index]
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 4: Already sorted array
    A = [1, 2, 3, 4, 5]
    for i in range(1, len(A) + 1):
        result = select_function(A.copy(), 0, len(A) - 1, i)
        expected = A[i - 1]  # 1-indexed to 0-indexed
        assert result == expected, f"Expected {expected}, got {result} for i={i}"
    
    # Test 5: Reverse sorted array
    A = [5, 4, 3, 2, 1]
    sorted_A = sorted(A)  # [1, 2, 3, 4, 5]
    for i in range(1, len(A) + 1):
        result = select_function(A.copy(), 0, len(A) - 1, i)
        expected = sorted_A[i - 1]  # 1-indexed to 0-indexed
        assert result == expected, f"Expected {expected}, got {result} for i={i}"
    
    # Test 6: Array with duplicates
    A = [3, 3, 3, 3, 3]
    result = select_function(A.copy(), 0, len(A) - 1, 1)
    assert result == 3, f"Expected 3, got {result}"
    result = select_function(A.copy(), 0, len(A) - 1, len(A))
    assert result == 3, f"Expected 3, got {result}"
    
    # Test 7: Single element
    A = [42]
    result = select_function(A.copy(), 0, 0, 1)
    assert result == 42, f"Expected 42, got {result}"
    
    # Test 8: Two elements
    A = [2, 1]
    result = select_function(A.copy(), 0, 1, 1)
    assert result == 1, f"Expected 1, got {result}"
    result = select_function(A.copy(), 0, 1, 2)
    assert result == 2, f"Expected 2, got {result}"
    
    # Test 9: Negative numbers
    A = [-3, -1, -2, -5]
    sorted_A = sorted(A)
    for i in range(1, len(A) + 1):
        result = select_function(A.copy(), 0, len(A) - 1, i)
        expected = sorted_A[i - 1]
        assert result == expected, f"Expected {expected}, got {result} for i={i}"
    
    # Test 10: Mixed positive and negative
    A = [5, -2, 0, -1, 3]
    sorted_A = sorted(A)
    for i in range(1, len(A) + 1):
        result = select_function(A.copy(), 0, len(A) - 1, i)
        expected = sorted_A[i - 1]
        assert result == expected, f"Expected {expected}, got {result} for i={i}"
    
    # Test 11: Large array
    A = list(range(1, 101))  # [1, 2, 3, ..., 100]
    import random
    random.shuffle(A)
    
    # Test various positions
    test_positions = [1, 10, 50, 90, 100]
    for i in test_positions:
        result = select_function(A.copy(), 0, len(A) - 1, i)
        expected = i
        assert result == expected, f"Expected {expected}, got {result} for i={i}"
    
    # Test 12: Subarray selection
    A = [9, 3, 7, 1, 5, 2, 8]
    # Select from subarray [7, 1, 5, 2] (indices 2-5)
    subarray = A[2:6]  # [7, 1, 5, 2]
    sorted_subarray = sorted(subarray)
    
    for i in range(1, len(subarray) + 1):
        result = select_function(A.copy(), 2, 5, i)
        expected = sorted_subarray[i - 1]
        assert result == expected, f"Expected {expected}, got {result} for i={i} in subarray"
    
    print("All select tests passed.")


if __name__ == "__main__":
    test_partition(partition)
    test_partition(randomized_partition)
    test_select(randomized_select)
    test_select(select)