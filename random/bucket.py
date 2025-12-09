def insertion_sort(A, n):
    for i in range(1, n):
        for j in range(i - 1, -1, -1):
            if A[j] <= A[j + 1]:
                break
            A[j], A[j + 1] = A[j + 1], A[j]


def insertion_sort_optimized(A):
    for i in range(1, len(A)):
        key = A[i]
        j = i - 1
        while j >= 0 and key < A[j]:
            A[j + 1] = A[j]
            j -= 1

        A[j + 1] = key


A = [1, 4, 3, 5, 6]
insertion_sort(A, len(A))
print(A)


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


def sorted_insert(head, value):
    """Inserts a value into a sorted linked list."""
    if head is None or value < head.value:
        new_node = Node(value)
        new_node.next = head
        return new_node

    current = head
    while current.next is not None and current.next.value < value:
        current = current.next

    new_node = Node(value)
    new_node.next = current.next
    current.next = new_node
    return head


def bucket_sort(A, n):
    """
    Bucket sort using Linked Lists for buckets.

    Efficiency Note:
    In C/C++, using Linked Lists can save memory and avoid resizing overhead compared to dynamic arrays.
    However, in Python, the overhead of creating Node objects and interpreter indirection usually makes
    this SLOWER than using Python's built-in lists (dynamic arrays) which are highly optimized in C.
    The time complexity remains O(n + k) on average.
    """
    buckets = [None] * n

    # 1. Distribute elements into buckets (inserting in sorted order)
    for x in A:
        idx = int(x * n)
        # Boundary check for x=1.0 case if inputs allowed 1.0, though usually [0, 1)
        if idx == n:
            idx -= 1
        buckets[idx] = sorted_insert(buckets[idx], x)

    # 2. Concatenate buckets
    out = []
    for head in buckets:
        current = head
        while current:
            out.append(current.value)
            current = current.next

    return out


if __name__ == "__main__":
    # Test cases for bucket sort (inputs should be in range [0, 1))
    test_cases = [
        ([0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68], 10),
        ([0.5, 0.3, 0.7, 0.1, 0.9], 5),
        ([0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51], 7),
        ([0.1, 0.2, 0.3, 0.4, 0.5], 5),
        ([0.9, 0.8, 0.7, 0.6, 0.5], 5),
        ([0.5], 1),
        ([], 0),
    ]

    print("Testing Bucket Sort:")
    print("=" * 60)

    all_passed = True
    for i, (A, n) in enumerate(test_cases, 1):
        if not A:  # Handle empty array
            result = bucket_sort(A, n)
            expected = []
            passed = result == expected
            status = "✅" if passed else "❌"
            print(f"Test {i}: {status}")
            print(f"  Input: {A}")
            print(f"  Result: {result}")
            print(f"  Expected: {expected}")
            if not passed:
                all_passed = False
            print()
            continue

        original = A.copy()
        result = bucket_sort(A, n)
        expected = sorted(original)
        passed = result == expected
        status = "✅" if passed else "❌"

        print(f"Test {i}: {status}")
        print(f"  Input: {original}")
        print(f"  Result: {result}")
        print(f"  Expected: {expected}")
        if not passed:
            all_passed = False
            print(f"  ❌ MISMATCH!")
        print()

    print("=" * 60)
    if all_passed:
        print(f"✅ All {len(test_cases)} tests passed!")
    else:
        print(f"❌ Some tests failed!")
