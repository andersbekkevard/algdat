def parent(i: int):
    return (i - 1) // 2


def left(i: int):
    return 2 * i + 1


def right(i: int):
    return 2 * i + 2


class Heap:
    def __init__(self):
        self.items: list[int] = []

    def insert(self, value: int):
        self.items.append(value)

    def get(self, i: int) -> int:
        return self.items[i]

    def set(self, i: int, val: int):
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
    if l < A.size() and A.get(l) > A.get(m):
        m = l
    if r < A.size() and A.get(r) > A.get(m):
        m = r
    if m != i:
        A.swap(i, m)
        max_heapify(A, m)


h = Heap()
h.insert(0)
h.insert(1)
h.insert(2)
h.insert(3)
h.insert(4)
h.insert(5)
print(h)

for i in range(len(h.items) - 1, -1, -1):
    max_heapify(h, i)

print(h)
