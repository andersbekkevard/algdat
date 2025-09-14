def partition(A, p, r):
    x = A[r]
    i = r
    for j in range(r - 1, p - 1, -1):
        if A[j] > x:
            i -= 1
            tmp = A[i]
            A[i] = A[j]
            A[j] = tmp
    A[r] = A[i]
    A[i] = x
    return i


def quicksort(A, p, r):
    if r > p:
        q = partition(A, p, r)
        quicksort(A, p, q - 1)
        quicksort(A, q + 1, r)


def quicksort_wrapper(arr):
    """A wrapper for quicksort that sorts the array in-place and returns it."""
    if not arr or len(arr) < 2:
        return arr
    quicksort(arr, 0, len(arr) - 1)
    return arr


def print_quicksort_test(test_case):
    arr = test_case["input"].copy()
    original = arr.copy()
    try:
        result = quicksort_wrapper(arr)
        is_correct = result == sorted(original)
        status = "✅ CORRECT" if is_correct else "❌ INCORRECT"
        print(f"\n📝 Test Case: {test_case['name']}")
        print(f"   Input:  {original}")
        print(f"   Output: {result}")
        print(f"   Status: {status}")
        if not is_correct:
            print(f"   Expected: {sorted(original)}")
    except Exception as e:
        print(f"❌ ERROR in {test_case['name']}: {str(e)}")


if __name__ == "__main__":
    # Define test cases similar to test_sorting.py
    TEST_CASES = [
        # {"name": "Empty", "input": []},
        # {"name": "Single Element", "input": [42]},
        {"name": "Already Sorted", "input": [1, 2, 3, 4, 5]},
        {"name": "Reverse Sorted", "input": [5, 4, 3, 2, 1]},
        {"name": "Random Order", "input": [3, 1, 4, 1, 5, 9, 2, 6]},
        {"name": "Duplicates", "input": [3, 1, 4, 1, 5, 9, 2, 6, 3, 1]},
        {"name": "Negative Numbers", "input": [-5, 3, -1, 7, -2, 0, 4]},
        {"name": "Large Numbers", "input": [1000, 500, 2000, 100, 1500]},
    ]

    print("\nQuicksort function tests:\n")
    passed = 0
    for test_case in TEST_CASES:
        arr = test_case["input"].copy()
        original = arr.copy()
        try:
            result = quicksort_wrapper(arr)
            is_correct = result == sorted(original)
            print_quicksort_test(test_case)
            if is_correct:
                passed += 1
        except Exception as e:
            print(f"❌ ERROR in {test_case['name']}: {str(e)}")

    print("\nTest summary:")
    print(f"✅ Passed: {passed}/{len(TEST_CASES)}")
    if passed == len(TEST_CASES):
        print("🎉 All quicksort tests passed!")
    else:
        print("⚠️  Some quicksort tests failed.")

# Print tests for partition

if __name__ == "false":

    def print_partition_test(arr, p, r):
        arr_copy = arr.copy()
        original_arr = arr.copy()
        idx = partition(arr_copy, p, r)

        # Validate partition correctness
        pivot_value = arr_copy[idx]
        is_valid = True

        # Check left side: all elements <= pivot
        for i in range(p, idx):
            if arr_copy[i] > pivot_value:
                is_valid = False
                break

        # Check right side: all elements >= pivot
        for i in range(idx + 1, r + 1):
            if arr_copy[i] < pivot_value:
                is_valid = False
                break

        print(f"Input: {original_arr} | p={p}, r={r}")
        print(f"Partitioned: {arr_copy}")
        print(f"Pivot index: {idx}")
        print(f"Pivot value: {pivot_value}")
        print(f"Status: {'PASS ✓' if is_valid else 'FAIL ✗'}")
        if not is_valid:
            print("  Error: Elements not properly partitioned around pivot!")
        print("-" * 50)

    print("Partition function tests:\n")

    # Test 1: Already sorted
    print_partition_test([1, 2, 3, 4, 5], 0, 4)

    # Test 2: Reverse sorted
    print_partition_test([5, 4, 3, 2, 1], 0, 4)

    # Test 3: Random order
    print_partition_test([3, 1, 4, 1, 5, 9, 2, 6], 0, 7)

    # Test 4: Duplicates
    print_partition_test([3, 1, 4, 1, 5, 9, 2, 6, 3, 1], 0, 9)

    # Test 5: Negative numbers
    print_partition_test([-5, 3, -1, 7, -2, 0, 4], 0, 6)

    # Test 6: Single element
    print_partition_test([42], 0, 0)

    # Test 7: Two elements
    print_partition_test([2, 1], 0, 1)

    # Test 8: All elements equal
    print_partition_test([7, 7, 7, 7], 0, 3)

    # Test 9: Pivot is minimum
    print_partition_test([5, 4, 3, 2, 1], 0, 4)

    # Test 10: Pivot is maximum
    print_partition_test([1, 2, 3, 4, 5], 0, 4)
