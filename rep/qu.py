class Queue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.arr = [None for _ in range(capacity)]
        self.head, self.tail, self.size = 0, 0, 0

    def enqueue(self, element):
        if self.size == self.capacity:
            raise Exception("full")
        self.arr[self.tail] = element
        self.tail = (self.tail + 1) % self.capacity
        self.size += 1

    def dequeue(self):
        if self.size == 0:
            raise Exception("empty")
        element = self.arr[self.head]
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return element


Q = Queue(5)
for i in range(4):
    Q.enqueue(i)

for i in range(4):
    print(Q.dequeue())
