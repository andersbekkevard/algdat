def parent(i: int):
    return (i - 1) // 2


def left(i: int):
    return 2 * i + 1


def right(i: int):
    return 2 * i + 2


class Node:
    def __init__(self, key: int):
        self.key = key

    def __repr__(self):
        return f"{self.key}"

    def __str__(self):
        return f"{self.key}"


class Heap:
    def __init__(self):
        self.items: list[Node] = []

    def get(self, i: int) -> Node:
        return self.items[i]

    def set(self, i: int, val: Node):
        self.items[i] = val

    def swap(self, i: int, j: int):
        self.items[i], self.items[j] = self.items[j], self.items[i]

    def size(self) -> int:
        return len(self.items)

    def __repr__(self):
        return f"Heap({self.__str__()})"

    def __str__(self):
        return str(self.items)


def max_heapify(A: Heap, i: int):
    l = left(i)
    r = right(i)
    m = i
    if l < A.size() and A.get(l).key > A.get(m).key:
        m = l
    if r < A.size() and A.get(r).key > A.get(m).key:
        m = r
    if m != i:
        A.swap(i, m)
        max_heapify(A, m)


def max_heap_maximum(A: Heap) -> Node:
    if A.size() == 0:
        raise IndexError("Heap is empty")
    return A.get(0)


def max_heap_extract_max(A: Heap) -> Node:
    r = max_heap_maximum(A)
    A.set(0, A.get(A.size() - 1))
    A.items.pop()
    if A.size() > 0:
        max_heapify(A, 0)
    return r


def build_max_heap(nodes: list[Node]) -> Heap:
    A = Heap()
    A.items = nodes.copy()
    n = len(A.items)
    for i in range(n // 2 - 1, -1, -1):
        max_heapify(A, i)
    return A


def max_heap_increase_key(A: Heap, x: Node, key: int):
    if key < x.key:
        raise ValueError("New key is smaller than current key")
    x.key = key
    i = A.items.index(x)
    while i > 0 and A.get(parent(i)).key < A.get(i).key:
        A.swap(i, parent(i))
        i = parent(i)


def is_valid_heap(A: Heap) -> bool:
    for i in range(1, A.size()):
        if A.get(i).key > A.get(parent(i)).key:
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


# endregion

if __name__ == "__main__":
    import numpy as np

    np.random.seed(42)

    # test_extract_max()
    test_increase_key()
