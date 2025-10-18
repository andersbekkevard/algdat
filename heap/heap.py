class Heap:
    def __init__(self):
        self.items: list[int] = []
        
    def insert(self, value:int):
        self.items.append(value)

    def get_parent(self, i: int):
        if i == 0:
            return None
        return self.items[(i-1) // 2]
    
    def get_left(self, i: int):
        left_index = 2*i + 1
        if left_index >= len(self.items):
            return None
        return self.items[left_index]

    def get_right(self, i: int):
        right_index = 2*i + 2
        if right_index >= len(self.items):
            return None
        return self.items[right_index]
    
    def __repr__(self):
        return f"Heap({self.__str__()})"
    
    def __str__(self):
        return str(self.items)

h = Heap()
h.insert(0)
h.insert(1)
h.insert(2)
h.insert(3)
h.insert(4)
h.insert(5)
print(h)
print(h.get_right(1))