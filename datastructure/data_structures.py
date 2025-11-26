class Stack:
    def __init__(self, size: int):
        self.items = [-1 for _ in range(size)]
        self.size = size
        self.top = 0

    def empty(self):
        return self.top == 0

    def push(self, x):
        if self.top >= self.size - 1:
            raise Exception()
        self.top += 1
        self.items[self.top] = x

    def pop(self):
        if self.empty():
            raise Exception()
        self.top -= 1
        return self.items[self.top + 1]

    def __repr__(self):
        return f"Stack(size={self.size}, top={self.top})"

    def __str__(self):
        if self.empty():
            return "Stack([])"
        elements = [self.items[i] for i in range(1, self.top + 1)]
        return f"Stack({elements})"


class Queue:
    def __init__(self, size: int):
        self.items = [0 for _ in range(size)]
        self.size = size
        self.capacity = 0
        self.head, self.tail = 0, 0

    def enqueue(self, x):
        if self.capacity == self.size:
            raise Exception()
        self.items[self.tail] = x
        self.capacity += 1
        self.tail = (self.tail + 1) % self.size

    def dequeue(self):
        if self.capacity == 0:
            raise Exception()
        x = self.items[self.head]
        self.head = (self.head + 1) % self.size
        self.capacity -= 1
        return x

    def __repr__(self):
        return "Q = " + str(self.items)

    def __str__(self):
        return "Q = " + str(self.items)


n = 10
Q = Queue(n)
for i in range(1, n + 1):
    Q.enqueue(i)
for i in range(1, n + 1):
    print(Q.dequeue())
