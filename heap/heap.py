INF: int = 10**9


# ============================================================================
# Heap Operations - Complexity (Kjøretid)
# ============================================================================
# Operation                      Time Complexity
# ─────────────────────────────────────────────
# Max-Heapify                     O(lg n)
# Heap-Max                        Θ(1)
# Heap-Extract-Max                O(lg n)
# Heap-Increase-Key               O(lg n)
# Max-Heap-Insert                 O(lg n)
# Build-Max-Heap                  Θ(n)
# ============================================================================


def parent(i: int) -> int:
    return (i - 1) // 2


def left(i: int) -> int:
    return 2 * i + 1


def right(i: int) -> int:
    return 2 * i + 2


class Node:
    def __init__(self, key: int) -> None:
        self.key = key

    def __repr__(self) -> str:
        return f"{self.key}"

    def __str__(self) -> str:
        return f"{self.key}"


class Heap:
    def __init__(self) -> None:
        self.items: list[Node] = []

    def size(self) -> int:
        return len(self.items)

    def get(self, i: int) -> Node:
        return self.items[i]

    def set(self, i: int, val: Node) -> None:
        self.items[i] = val

    def swap(self, i: int, j: int) -> None:
        self.items[i], self.items[j] = self.items[j], self.items[i]

    def __repr__(self) -> str:
        return f"Heap({self.__str__()})"

    def __str__(self) -> str:
        return str(self.items)


def max_heapify(A: Heap, i: int, n: int | None = None) -> None:
    """Restore max-heap property at index i. n is heap size (defaults to A.size())."""
    if n is None:
        n = A.size()
    l = left(i)
    r = right(i)
    m = i
    if l < n and A.get(l).key > A.get(m).key:
        m = l
    if r < n and A.get(r).key > A.get(m).key:
        m = r
    if m != i:
        A.swap(i, m)
        max_heapify(A, m, n)


def max_heap_maximum(A: Heap) -> Node:
    return A.get(0)


def max_heap_extract_max(A: Heap) -> Node:
    """Extract and return the maximum element from the heap."""
    n = A.size()
    A.swap(0, n - 1)
    result = A.items.pop()
    max_heapify(A, 0)
    return result


def build_max_heap(nodes: list[Node]) -> Heap:
    """Build a max-heap from a list of nodes."""
    A = Heap()
    A.items = nodes
    n = A.size()
    for i in range((n - 2) // 2, -1, -1):
        max_heapify(A, i, n)
    return A


def bubble_up(A: Heap, i: int) -> None:
    """Bubble up element at index i to restore max-heap property."""
    while i > 0 and A.get(i).key > A.get(parent(i)).key:
        A.swap(i, parent(i))
        i = parent(i)


def max_heap_increase_key(A: Heap, x: Node, key: int) -> None:
    """Increase the key of node x to the new key value."""
    if key >= x.key:
        i = A.items.index(x)
        x.key = key
        bubble_up(A, i)


def max_heap_insert(A: Heap, x: Node) -> None:
    """Insert a node into the heap."""
    key = x.key
    x.key = -INF
    A.items.append(x)
    max_heap_increase_key(A, x, key)


def heapsort(array: list[int]) -> list[int]:
    """Sort an array using heapsort and return the sorted array."""
    A = build_max_heap([Node(v) for v in array])
    for i in range(len(array) - 1, -1, -1):
        array[i] = max_heap_extract_max(A).key
    return array


def is_valid_heap(A: Heap) -> bool:
    """Check if A satisfies the max-heap property."""
    n = A.size()
    for i in range(n):
        l = left(i)
        r = right(i)
        if l < n and A.get(l).key > A.get(i).key:
            return False
        if r < n and A.get(r).key > A.get(i).key:
            return False
    return True


# region tests


def test_extract_max():
    """Test extract-max operation on a max heap."""
    print("=" * 80)
    print("TEST: Extract-Max")
    print("=" * 80)

    # Generate a heap with random nodes
    num_elements = 10
    random_keys = np.random.randint(1, 101, size=num_elements)
    nodes = [Node(key) for key in random_keys]
    print(f"Original nodes: {nodes}\n")

    heap = build_max_heap(nodes)
    print(f"Built max heap: {heap}\n")

    # Extract items one by one
    extraction_count = num_elements
    for extraction_num in range(1, extraction_count + 1):
        if heap.size() == 0:
            print("Heap is empty!")
            break

        extracted = max_heap_extract_max(heap)
        is_valid = is_valid_heap(heap)
        status = "✅" if is_valid else "❌"
        print(
            f"Extraction {extraction_num:2}: Extracted {str(extracted):>4} | {status} Heap: {heap}"
        )

    print()


def test_increase_key():
    """Test increase-key operation on a max heap."""
    print("=" * 80)
    print("TEST: Increase-Key")
    print("=" * 80)

    # Generate a heap with random nodes
    num_elements = 8
    random_keys = np.random.randint(10, 51, size=num_elements)
    nodes = [Node(key) for key in random_keys]
    print(f"Original nodes: {nodes}\n")

    heap = build_max_heap(nodes)
    print(f"Built max heap: {heap}\n")

    # Test increase-key on different nodes
    test_cases = [
        (2, 95),  # Increase node at index 2 to 95
        (5, 70),  # Increase node at index 5 to 70
        (7, 88),  # Increase node at index 7 to 88
    ]

    for idx, (node_idx, new_key) in enumerate(test_cases, 1):
        if node_idx >= heap.size():
            print(f"Operation {idx}: Node index {node_idx} out of bounds! Skipping.\n")
            continue

        target_node = heap.get(node_idx)
        old_key = target_node.key
        print(
            f"Operation {idx}: Increasing node at index {node_idx} from {old_key} to {new_key}"
        )

        max_heap_increase_key(heap, target_node, new_key)
        is_valid = is_valid_heap(heap)
        status = "✅" if is_valid else "❌"
        print(f"           {status} Heap after increase: {heap}\n")

    print()


def test_insert():
    """Test insert operation on a max heap."""
    print("=" * 80)
    print("TEST: Insert")
    print("=" * 80)

    # Start with an empty heap
    heap = Heap()
    print(f"Starting with empty heap: {heap}\n")

    # Insert values one by one
    insert_values = [15, 10, 20, 8, 2, 16, 25, 5, 30, 12]
    print(f"Inserting values in order: {insert_values}\n")

    for insert_num, value in enumerate(insert_values, 1):
        node = Node(value)
        max_heap_insert(heap, node)
        is_valid = is_valid_heap(heap)
        status = "✅" if is_valid else "❌"
        print(f"Insert {insert_num:2}: Inserted {value:>2} | {status} Heap: {heap}")

    print()


def test_heapsort():
    """Test heapsort algorithm."""
    print("=" * 80)
    print("TEST: heapsort")
    print("=" * 80)

    # Test cases with different sizes
    test_cases = [
        [15, 10, 20, 8, 2, 16, 25, 5, 30, 12],
        [42, 17, 93, 5, 88, 31, 64, 11],
        [100],
        [3, 2, 1],
    ]

    for case_num, unsorted_array in enumerate(test_cases, 1):
        original = unsorted_array.copy()
        print(f"Test case {case_num}:")
        print(f"  Original:  {original}")

        sorted_array = heapsort(unsorted_array)
        is_sorted = sorted_array == sorted(original)
        status = "✅" if is_sorted else "❌"

        print(f"  Sorted:    {sorted_array}")
        print(f"  {status} Correctly sorted in ascending order\n")

    print()


# endregion

if __name__ == "__main__":
    import numpy as np

    np.random.seed(42)

    test_extract_max()
    test_increase_key()
    test_insert()
    test_heapsort()
