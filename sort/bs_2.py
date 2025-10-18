def insertion_sort(A, n):
    for i in range(1, n):
        x = A[i]
        j = i
        while j > 0 and A[j - 1] > x:
            A[j] = A[j - 1]
            j -= 1
        A[j] = x


def bucket_sort(A, n):
    B = [[] for _ in range(n)]
    for i in range(n):
        bucket_index = int(A[i] * n)
        # Handle edge case where A[i] = 1.0
        if bucket_index >= n:
            bucket_index = n - 1
        B[bucket_index].append(A[i])

    C = []
    for i in range(n):
        insertion_sort(B[i], len(B[i]))
        C += B[i]
    return C

def bucket_sort_integers(A, n, max_val):
    """
    Bucket sort for integers in range [0, max_val]
    """
    # Create n empty buckets
    B = [[] for _ in range(n)]
    
    # Distribute elements into buckets
    for i in range(len(A)):
        bucket_index = int((A[i] * n) / (max_val + 1))
        B[bucket_index].append(A[i])
    
    # Sort each bucket using insertion sort
    for i in range(n):
        insertion_sort(B[i], len(B[i]))
    
    # Concatenate all buckets
    result = []
    for bucket in B:
        result.extend(bucket)
    
    return result

if __name__ == "__main__":
    import random
    
    all_tests_passed = True
    
    # Test with floating point numbers in range [0, 1)
    print("=== Bucket Sort for [0, 1) ===")
    A_float = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]
    n_float = len(A_float)
    print("Original array:", A_float)
    result_float = bucket_sort(A_float, n_float)
    print("Bucket sorted:", result_float)
    expected_float = sorted(A_float)
    if result_float != expected_float:
        print("❌ Test failed!")
        all_tests_passed = False
    else:
        print("✅ Test passed!")
    
    # Test with random floating point numbers
    print("\n=== Random Float Test ===")
    random.seed(42)
    A_random = [random.random() for _ in range(10)]
    print("Original array:", [round(x, 3) for x in A_random])
    result_random = bucket_sort(A_random, len(A_random))
    print("Bucket sorted:", [round(x, 3) for x in result_random])
    expected_random = sorted(A_random)
    if result_random != expected_random:
        print("❌ Test failed!")
        all_tests_passed = False
    else:
        print("✅ Test passed!")
    
    # Test with integers
    print("\n=== Bucket Sort for Integers ===")
    A_int = [170, 45, 75, 90, 802, 24, 2, 66]
    n_int = len(A_int)
    max_val = max(A_int)
    print("Original array:", A_int)
    result_int = bucket_sort_integers(A_int, n_int, max_val)
    print("Bucket sorted:", result_int)
    expected_int = sorted(A_int)
    if result_int != expected_int:
        print("❌ Test failed!")
        all_tests_passed = False
    else:
        print("✅ Test passed!")
    
    # Test with more integers
    print("\n=== More Integer Tests ===")
    test_arrays = [
        [1000, 100, 10, 1],
        [999, 998, 997, 996],
        [123, 456, 789, 321, 654, 987]
    ]
    
    for i, A in enumerate(test_arrays):
        print(f"\nTest {i+1}:")
        print("Original array:", A)
        result = bucket_sort_integers(A, len(A), max(A))
        print("Bucket sorted:", result)
        expected = sorted(A)
        if result != expected:
            print("❌ Test failed!")
            all_tests_passed = False
        else:
            print("✅ Test passed!")
    
    # Final result
    print("\n" + "="*50)
    if all_tests_passed:
        print("🎉 ALL TESTS SUCCESSFUL! 🎉")
    else:
        print("❌ Some tests failed!")
