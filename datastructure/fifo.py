class Queue:
    def __init__(self, capacity):
        self.size = 0
        self.capacity = capacity
        self.q = [None] * capacity
        self.front = 0
        self.rear = 0

    def enqueue(self, val):
        if self.size == self.capacity:
            raise Exception("Queue is full")
        self.q[self.rear] = val
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1

    def dequeue(self):
        if self.size == 0:
            raise Exception("Queue is empty")
        val = self.q[self.front]
        self.q[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return val

    def __str__(self):
        return str(self.q)


q = Queue(3)
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
print(q)
print(q.dequeue())
q.enqueue(4)
print(q.dequeue())
q.enqueue(5)
print(q.dequeue())
print(q.dequeue())
print(q.dequeue())
print(q)
