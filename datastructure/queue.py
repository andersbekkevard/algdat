class Queue:

    def __init__(self, max_size):
        # Initialiser de underliggende datastrukturene her
        self.list = [None] * max_size
        self.max_size = max_size
        self.first_element_pointer = -1
        self.last_element_pointer = -1

    def enqueue(self, value):
        # Skriv kode for Enqueue operasjonen

        # Initialiserer ved første element
        if self.first_element_pointer == -1 and self.last_element_pointer == -1:
            self.first_element_pointer, self.last_element_pointer = (
                self.max_size - 1,
                self.max_size - 1,
            )
            self.list[self.first_element_pointer] = value
            return

        if self.last_element_pointer - self.first_element_pointer + 1 >= self.max_size:
            return

        self.list[self.first_element_pointer - 1] = value
        self.first_element_pointer -= 1

    def dequeue(self):
        element = self.list[self.last_element_pointer]
        self.list[self.last_element_pointer] = None
        self.last_element_pointer -= 1
        return element

    def __str__(self):
        # Returner en strengrepresentasjon av køen fra front til bak
        return str(self.list)


# Sett 'highscore' til True hvis du vil vises på poengtavlen.
# For mer info se 'https://algdat.idi.ntnu.no/ovinger.html#poengtavle'
# Merk: Kjøring for poengtavlen tar betraktelig lengre tid.
highscore = True


if __name__ == "__main__":
    q = Queue(5)
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    q.enqueue(4)
    q.enqueue(5)
    print(q)
    print(q.dequeue())
    print(q)
    print(q.dequeue())
    print(q)
