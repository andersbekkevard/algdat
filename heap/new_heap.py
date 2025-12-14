from shutil import ExecError


class Node:
    def __init__(self, key):
        self.key = key

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def __repr__(self):
        return str(self.key)


class Heap(list):
    def __init__(self, iterable=None):
        if iterable is not None:
            super().__init__(iterable)
        else:
            super().__init__()
        self.heap_size = len(self)


def left(i):
    return 2 * i + 1


def right(i):
    return 2 * i + 2


def parent(i):
    return (i - 1) // 2


def max_heapify(A, i):
    l = left(i)
    r = right(i)
    if l < A.heap_size and A[l] > A[i]:
        largest = l
    else:
        largest = i
    if r < A.heap_size and A[r] > A[largest]:
        largest = r

    if largest != i:
        A[largest], A[i] = A[i], A[largest]
        max_heapify(A, largest)


def extract_max(A):
    if A.heap_size < 1:
        raise Exception("heap underflow")
    max_val = A[0]
    A[0] = A[A.heap_size - 1]
    A.heap_size -= 1
    max_heapify(A, 0)
    return max_val


def build_max_heap(A):
    A.heap_size = len(A)
    for i in range(len(A) // 2 - 1, -1, -1):
        max_heapify(A, i)


def increase_key(A, i, k):
    if k < A[i].key:
        raise Exception("New key is smaller than current key")
    A[i].key = k
    while i > 0 and A[parent(i)].key < A[i].key:
        p = parent(i)
        A[i], A[p] = A[p], A[i]
        i = p


def max_heap_insert(A, x):
    A.heap_size += 1
    INF = 1e9
    k = x.key
    x.key = -INF
    if A.heap_size > len(A):
        A.append(x)
    else:
        A[A.heap_size - 1] = x
    increase_key(A, A.heap_size - 1, k)


def heap_sort(A):
    A = Heap(A)
    build_max_heap(A)
    for i in range(A.heap_size - 1, 0, -1):
        A[0], A[i] = A[i], A[0]
        A.heap_size -= 1
        max_heapify(A, 0)
    return list(A)


def verify_max_heap(A):
    """Verify that the array maintains max-heap property"""
    for i in range(A.heap_size):
        l = left(i)
        r = right(i)
        if l < A.heap_size and A[l].key > A[i].key:
            return (
                False,
                f"Heap property violated: A[{l}]={A[l].key} > A[{i}]={A[i].key}",
            )
        if r < A.heap_size and A[r].key > A[i].key:
            return (
                False,
                f"Heap property violated: A[{r}]={A[r].key} > A[{i}]={A[i].key}",
            )
    return True, "Heap property maintained"


# Demonstration of max-heap operations
if __name__ == "__main__":
    A = Heap([Node(x) for x in [3, 5, 1, 10, 2, 7]])
    print("Original array:", A)
    # Build the max heap
    build_max_heap(A)
    print("Max heap:", A)
    # Extract max demonstration
    max_val = extract_max(A)
    print("Extracted max:", max_val)
    # Note: A has not physically shrunk, but heap_size has.
    print(f"Heap content (first {A.heap_size} elements):", A[: A.heap_size])

    # Test increase_key
    print("\n--- Testing increase_key ---")
    A2 = Heap([Node(x) for x in [3, 5, 1, 10, 2, 7]])
    build_max_heap(A2)
    print("Heap before increase_key:", A2)
    is_valid, msg = verify_max_heap(A2)
    print(f"Heap valid before: {is_valid} - {msg} {'✅' if is_valid else ''}")

    # Increase key at index 4 (which has value 2) to 15
    print(f"\nIncreasing key at index 4 from {A2[4].key} to 15")
    increase_key(A2, 4, 15)
    print("Heap after increasing key:", A2)
    print("Root should now be 15:", A2[0])
    is_valid, msg = verify_max_heap(A2)
    print(f"Heap valid after: {is_valid} - {msg} {'✅' if is_valid else ''}")

    # Test another case: increase a key that doesn't need to bubble all the way up
    print("\n--- Testing increase_key (smaller increase) ---")
    A3 = Heap([Node(x) for x in [10, 8, 7, 5, 3, 2]])
    build_max_heap(A3)
    print("Heap before increase_key:", A3)
    print(f"Increasing key at index 5 from {A3[5].key} to 6")
    increase_key(A3, 5, 6)
    print("Heap after increasing key:", A3)
    is_valid, msg = verify_max_heap(A3)
    print(f"Heap valid after: {is_valid} - {msg} {'✅' if is_valid else ''}")

    # Test insert
    print("\n--- Testing max_heap_insert ---")
    A4 = Heap([Node(x) for x in [10, 8, 7, 5, 3, 2]])
    build_max_heap(A4)
    print("Heap before insert:", A4)
    new_node = Node(12)
    print(f"Inserting node with key {new_node.key}")
    max_heap_insert(A4, new_node)
    print("Heap after insert:", A4)
    is_valid, msg = verify_max_heap(A4)
    print(f"Heap valid after insert: {is_valid} - {msg} {'✅' if is_valid else ''}")

    # Test heap_sort
    print("\n--- Testing heap_sort ---")
    test_cases = [
        [3, 5, 1, 10, 2, 7],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [42],
        [5, 3, 5, 1, 3, 2],
        [10, 8, 7, 5, 3, 2, 1],
    ]
    for test_arr in test_cases:
        original = [Node(x) for x in test_arr]
        sorted_result = heap_sort([Node(x) for x in test_arr])
        sorted_keys = [node.key for node in sorted_result]
        expected = sorted(test_arr)
        is_correct = sorted_keys == expected
        print(f"Input: {test_arr}")
        print(f"Output: {sorted_keys}")
        print(f"Expected: {expected}")
        print(f"Correct: {is_correct} {'✅' if is_correct else '❌'}")
        print()
