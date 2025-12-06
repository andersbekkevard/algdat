"""
Fibonacci min-heap rewritten as an object with integer keys,
mirroring the CLRS pseudocode closely.
"""

import math
from typing import Generator, Optional


class FibNode:
    def __init__(self, key: int) -> None:
        self.key = key
        self.parent: Optional["FibNode"] = None
        self.child: Optional["FibNode"] = None
        self.left: "FibNode" = self
        self.right: "FibNode" = self
        self.degree = 0
        self.mark = False


class FibonacciHeap:
    def __init__(self) -> None:
        self.min: Optional[FibNode] = None
        self.n = 0

    # ------------------------------------------------------------------ #
    # Helpers                                                            #
    # ------------------------------------------------------------------ #
    def _iterate(self, start: Optional[FibNode]) -> Generator[FibNode, None, None]:
        if start is None:
            return
        x = start
        first = True
        while first or x != start:
            first = False
            yield x
            x = x.right

    def _insert_root(self, x: FibNode) -> None:
        if self.min is None:
            x.left = x.right = x
            self.min = x
        else:
            m = self.min
            r = m.right
            m.right = x
            x.left = m
            x.right = r
            r.left = x
            if x.key < m.key:
                self.min = x

    def _remove_root(self, x: FibNode) -> None:
        if x.right == x:
            self.min = None
        else:
            l = x.left
            r = x.right
            l.right = r
            r.left = l
            if self.min is x:
                self.min = r
        x.left = x.right = x

    def _heap_link(self, y: FibNode, x: FibNode) -> None:
        # remove y from root list
        y.left.right = y.right
        y.right.left = y.left
        y.parent = x
        if x.child is None:
            x.child = y
            y.left = y.right = y
        else:
            c = x.child
            r = c.right
            c.right = y
            y.left = c
            y.right = r
            r.left = y
        x.degree += 1
        y.mark = False

    def _consolidate(self) -> None:
        if self.min is None:
            return
        D = int(math.log2(self.n)) + 2 if self.n > 0 else 1
        A: list[Optional[FibNode]] = [None] * (D + 1)
        roots = list(self._iterate(self.min))
        for w in roots:
            x = w
            d = x.degree
            while A[d] is not None:
                y = A[d]
                if y and x.key > y.key:
                    x, y = y, x
                self._heap_link(y, x)  # type: ignore[arg-type]
                A[d] = None
                d += 1
            A[d] = x
        self.min = None
        for a in A:
            if a is not None:
                a.left = a.right = a
                if self.min is None:
                    self.min = a
                else:
                    self._insert_root(a)
                    if a.key < self.min.key:
                        self.min = a

    def _cut(self, x: FibNode, y: FibNode) -> None:
        if y.child is x:
            if x.right != x:
                y.child = x.right
            else:
                y.child = None
        x.left.right = x.right
        x.right.left = x.left
        y.degree -= 1
        x.left = x.right = x
        x.parent = None
        x.mark = False
        self._insert_root(x)

    def _cascading_cut(self, y: FibNode) -> None:
        z = y.parent
        if z is None:
            return
        if not y.mark:
            y.mark = True
        else:
            self._cut(y, z)
            self._cascading_cut(z)

    # ------------------------------------------------------------------ #
    # Public operations                                                  #
    # ------------------------------------------------------------------ #
    def insert(self, key: int) -> FibNode:
        x = FibNode(key)
        self._insert_root(x)
        self.n += 1
        return x

    def minimum(self) -> FibNode:
        if self.min is None:
            raise IndexError("minimum from empty heap")
        return self.min

    def union(self, other: "FibonacciHeap") -> "FibonacciHeap":
        H = FibonacciHeap()
        H.min = self.min
        if H.min is None or (other.min is not None and other.min.key < H.min.key):
            H.min = other.min
        if self.min and other.min:
            self_right = self.min.right
            other_left = other.min.left
            self.min.right = other.min
            other.min.left = self.min
            self_right.left = other_left
            other_left.right = self_right
        H.n = self.n + other.n
        return H

    def extract_min(self) -> FibNode:
        z = self.min
        if z is None:
            raise IndexError("extract_min from empty heap")
        if z.child is not None:
            for x in list(self._iterate(z.child)):
                x.parent = None
                x.left = x.right = x
                self._insert_root(x)
        self._remove_root(z)
        self.n -= 1
        if self.min is not None:
            self._consolidate()
        return z

    def decrease_key(self, x: FibNode, k: int) -> None:
        if k > x.key:
            raise ValueError("new key is greater than current key")
        x.key = k
        y = x.parent
        if y is not None and x.key < y.key:
            self._cut(x, y)
            self._cascading_cut(y)
        if self.min is None or x.key < self.min.key:
            self.min = x

    def delete(self, x: FibNode) -> None:
        self.decrease_key(x, -math.inf)  # type: ignore[arg-type]
        self.extract_min()


__all__ = ["FibonacciHeap", "FibNode"]
