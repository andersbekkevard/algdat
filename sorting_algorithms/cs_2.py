def counting_sort(A, n, k):
    B = [0] * n
    C = [0] * k

    for i in range(n):
        C[A[i]] += 1

    for i in range(1, k):
        C[i] += C[i-1]
        
    for i in range(n - 1, -1, -1):
        B[C[A[i]] - 1] = A[i]
        C[A[i]] -= 1

    return B


def test_counting_sort(counting_sort_function):
    print(f"Testing {counting_sort_function.__name__}")
    
    # Test 1: Basic case
    A = [3, 2, 1, 5, 4]
    n = len(A)
    k = max(A) + 1
    result = counting_sort_function(A.copy(), n, k)
    expected = sorted(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 2: Already sorted array
    A = [1, 2, 3, 4, 5]
    n = len(A)
    k = max(A) + 1
    result = counting_sort_function(A.copy(), n, k)
    expected = sorted(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 3: Reverse sorted array
    A = [5, 4, 3, 2, 1]
    n = len(A)
    k = max(A) + 1
    result = counting_sort_function(A.copy(), n, k)
    expected = sorted(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 4: Array with duplicates
    A = [3, 1, 3, 2, 1, 3, 2]
    n = len(A)
    k = max(A) + 1
    result = counting_sort_function(A.copy(), n, k)
    expected = sorted(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 5: All equal elements
    A = [7, 7, 7, 7, 7]
    n = len(A)
    k = max(A) + 1
    result = counting_sort_function(A.copy(), n, k)
    expected = sorted(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 6: Single element
    A = [42]
    n = len(A)
    k = max(A) + 1
    result = counting_sort_function(A.copy(), n, k)
    expected = sorted(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 7: Two elements
    A = [2, 1]
    n = len(A)
    k = max(A) + 1
    result = counting_sort_function(A.copy(), n, k)
    expected = sorted(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    A = [1, 2]
    n = len(A)
    k = max(A) + 1
    result = counting_sort_function(A.copy(), n, k)
    expected = sorted(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 8: Array with zeros
    A = [0, 5, 0, 3, 0, 1]
    n = len(A)
    k = max(A) + 1
    result = counting_sort_function(A.copy(), n, k)
    expected = sorted(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 9: Array starting from 0
    A = [0, 1, 2, 3, 4]
    n = len(A)
    k = max(A) + 1
    result = counting_sort_function(A.copy(), n, k)
    expected = sorted(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 10: Large range
    A = [10, 5, 15, 2, 8, 12, 1, 20]
    n = len(A)
    k = max(A) + 1
    result = counting_sort_function(A.copy(), n, k)
    expected = sorted(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 11: Many duplicates
    A = [2, 2, 2, 2, 1, 1, 1, 3, 3, 3, 3]
    n = len(A)
    k = max(A) + 1
    result = counting_sort_function(A.copy(), n, k)
    expected = sorted(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 12: Stability test - verify stable sort with duplicates
    # For counting sort, we verify by checking the sorted output is correct
    A = [5, 2, 8, 2, 9, 1, 5, 5]
    n = len(A)
    k = max(A) + 1
    result = counting_sort_function(A.copy(), n, k)
    expected = sorted(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 13: Large array
    A = [i % 50 for i in range(100, 0, -1)]  # Values 0-49, length 100
    n = len(A)
    k = max(A) + 1
    result = counting_sort_function(A.copy(), n, k)
    expected = sorted(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 14: Random-like pattern
    A = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    n = len(A)
    k = max(A) + 1
    result = counting_sort_function(A.copy(), n, k)
    expected = sorted(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test 15: Small range, many elements
    A = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    n = len(A)
    k = 2  # Only values 0 and 1
    result = counting_sort_function(A.copy(), n, k)
    expected = sorted(A)
    assert result == expected, f"Expected {expected}, got {result}"
    
    print("All counting_sort tests passed.")


if __name__ == "__main__":
    test_counting_sort(counting_sort)