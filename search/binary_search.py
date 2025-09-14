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
        return p
    elif v < pivot:
        return bisect_recursive(A, p, q - 1, v)
    else:
        return bisect_recursive(A, q + 1, r, v)


x = bisect_recursive([1, 2, 3, 3, 4, 5], 0, 4, 3)
print(x)
# Edge case tests for bisect_recursive

# Empty array
assert bisect_recursive([], 0, -1, 1) is None, "Empty array should return None"

# Single element, value present
assert bisect_recursive([5], 0, 0, 5) == 0, "Single element present should return 0"

# Single element, value absent
assert (
    bisect_recursive([5], 0, 0, 3) is None
), "Single element absent should return None"

# Value at the start
assert bisect_recursive([2, 3, 4, 5], 0, 3, 2) == 0, "Value at start should return 0"

# Value at the end
assert bisect_recursive([2, 3, 4, 5], 0, 3, 5) == 3, "Value at end should return 3"

# Value not present, in range
assert (
    bisect_recursive([1, 3, 5, 7], 0, 3, 4) is None
), "Value not present should return None"

# All elements the same, value present
assert bisect_recursive([2, 2, 2, 2], 0, 3, 2) in [
    0,
    1,
    2,
    3,
], "All same, value present should return valid index"

# All elements the same, value absent
assert (
    bisect_recursive([2, 2, 2, 2], 0, 3, 3) is None
), "All same, value absent should return None"

# Negative numbers
assert (
    bisect_recursive([-5, -3, -1, 0, 2], 0, 4, -3) == 1
), "Negative number present should return correct index"

# Large indices
large_arr = list(range(10000))
assert bisect_recursive(large_arr, 0, 9999, 9999) == 9999, "Large array, value at end"

print("All edge case tests passed.")
