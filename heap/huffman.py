"""
Pseudocode:

def huffman(text):
    # Count the frequency of each character in the text
    # Sort the characters by frequency
    # Build the Huffman tree (prefix free)
    # Traverse the tree and encode the text
"""


def count_chars(text: str) -> dict[str, int]:
    counts = {}
    for character in text:
        counts[character] = counts.get(character, 0) + 1
    return counts


def partition(arr: list[tuple[str, int]], low: int, high: int, reversed=False) -> int:
    pivot = arr[high][1]
    i = low - 1
    for j in range(low, high):
        if reversed:
            if arr[j][1] >= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        else:
            if arr[j][1] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort(arr: list[tuple[str, int]], low: int, high: int, reversed=False) -> None:
    if low < high:
        pi = partition(arr, low, high, reversed)
        quicksort(arr, low, pi - 1, reversed)
        quicksort(arr, pi + 1, high, reversed)


class Node:
    def __init__(self, character: str | None, frequency: int):
        self.character = character
        self.frequency = frequency
        self.left: Node | None = None
        self.right: Node | None = None

    def __str__(self):
        if self.character is not None:
            representation = f"● character: {self.character}\n"
        else:
            representation = f""
        if self.left is not None:
            representation += f"┣━━━┓ (venstre)"
            representation += "\n┃   " + str(self.left).replace("\n", "\n┃   ")
            representation += f"\n┗━━━┓ (høyre)"
            representation += "\n    " + str(self.right).replace("\n", "\n    ")
        return representation


class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, item: Node) -> None:
        """Add an item to the heap and maintain heap property."""
        self.heap.append(item)
        self._bubble_up(len(self.heap) - 1)

    def extract_min(self) -> Node:
        """Remove and return the minimum item from the heap."""
        if len(self.heap) == 0:
            raise ValueError("Heap is empty")
        if len(self.heap) == 1:
            return self.heap.pop()

        min_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bubble_down(0)
        return min_item

    def _bubble_up(self, index: int) -> None:
        """Move item up the heap to maintain min heap property."""
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index].frequency < self.heap[parent_index].frequency:
                self.heap[index], self.heap[parent_index] = (
                    self.heap[parent_index],
                    self.heap[index],
                )
                index = parent_index
            else:
                break

    def _bubble_down(self, index: int) -> None:
        """Move item down the heap to maintain min heap property."""
        while True:
            smallest = index
            left_child = 2 * index + 1
            right_child = 2 * index + 2

            if (
                left_child < len(self.heap)
                and self.heap[left_child].frequency < self.heap[smallest].frequency
            ):
                smallest = left_child
            if (
                right_child < len(self.heap)
                and self.heap[right_child].frequency < self.heap[smallest].frequency
            ):
                smallest = right_child

            if smallest != index:
                self.heap[index], self.heap[smallest] = (
                    self.heap[smallest],
                    self.heap[index],
                )
                index = smallest
            else:
                break

    def is_empty(self) -> bool:
        """Check if the heap is empty."""
        return len(self.heap) == 0

    def size(self) -> int:
        """Return the number of items in the heap."""
        return len(self.heap)


def build_huffman_tree(text: str) -> Node:
    count_list = list(count_chars(text).items())
    heap = MinHeap()
    for character, frequency in count_list:
        heap.insert(Node(character, frequency))

    while heap.size() > 1:
        n1, n2 = heap.extract_min(), heap.extract_min()
        n3 = Node(None, n1.frequency + n2.frequency)
        n3.left, n3.right = n1, n2
        heap.insert(n3)

    return heap.extract_min()


def encode(data, encoding):
    return "".join([encoding[c] for c in data])


def encoding(node, code="", lookup=None):
    if lookup is None:
        lookup = {}

    if node.character:
        lookup[node.character] = code
    else:
        encoding(node.left, code + "0", lookup)
        encoding(node.right, code + "1", lookup)
    return lookup


def decode(data: str, root: Node | None) -> str:
    """Decode a bit string using the Huffman tree."""
    if not data or not root:
        return ""

    result = []
    current: Node | None = root

    for bit in data:
        if current is None:
            break
        if bit == "0":
            current = current.left
        else:
            current = current.right

        if current and current.character:
            result.append(current.character)
            current = root

    return "".join(result)


if __name__ == "__main__":
    # Demo usage with multiple examples
    examples = [
        "hello world",
        "aaaaaabbbbbccd",
        "the quick brown fox jumps over the lazy dog",
        "mississippi",
        "abcdefghijklmnopqrstuvwxyz",
        """
Id sunt cupidatat do dolore sunt incididunt fugiat officia ex dolore nulla eu esse adipisicing occaecat. Eu magna aliquip nostrud officia. Sit aliqua officia est voluptate fugiat. Deserunt ullamco laborum adipisicing mollit nulla cillum. Enim officia elit est aliquip nulla minim tempor.

Non deserunt consectetur quis laboris ipsum ullamco occaecat ipsum. Ad ut eu aliqua ad ipsum occaecat ut sunt dolore magna excepteur consectetur sint laborum. Do nulla reprehenderit amet commodo incididunt sit. Irure adipisicing ea quis.

Deserunt culpa non velit proident minim minim. Dolore nisi dolore eu aliquip dolore aute et aliqua est. Id proident laboris nulla reprehenderit consequat excepteur exercitation veniam duis velit. Est tempor ex fugiat anim labore ut ex et magna. Ea velit duis incididunt non veniam ad ex laborum esse occaecat officia. Ullamco pariatur proident aliqua aliqua est. Occaecat pariatur ipsum in Lorem minim deserunt. Aute deserunt do quis nisi tempor non.

Ad officia non ullamco velit laboris aliqua esse cupidatat. Sint irure esse aute nulla consectetur cupidatat quis. Incididunt in laboris deserunt. Veniam veniam mollit nostrud. Ullamco velit in dolore consequat nisi veniam occaecat qui irure culpa irure et eu. Ullamco laborum laboris enim esse duis ad culpa occaecat est sint fugiat.

Exercitation ut incididunt veniam pariatur dolore in culpa magna nisi occaecat aliquip eiusmod. Velit do aute fugiat id pariatur dolor culpa dolore consectetur voluptate qui est fugiat irure. Ad ullamco amet consequat voluptate magna proident occaecat cupidatat in. Aliquip labore Lorem est adipisicing ut ullamco. Ea cillum ipsum mollit pariatur Lorem dolor commodo in incididunt nulla elit. Incididunt officia nostrud ut reprehenderit labore.

Irure cillum proident laborum nisi nulla. Voluptate amet cillum ullamco. Veniam enim commodo amet velit aliqua consectetur dolor occaecat labore ex. Adipisicing anim sit elit Lorem culpa duis aute do. Elit sit cillum in ut sit voluptate. Elit laborum nostrud reprehenderit occaecat enim laboris amet laboris Lorem quis duis mollit ex.

Labore in occaecat dolore nisi eiusmod exercitation irure aute tempor aliquip aliquip culpa proident sunt. Voluptate ut veniam ipsum exercitation proident. Ut occaecat sunt est ipsum. Est esse deserunt reprehenderit ex mollit eu ea amet nulla nulla minim culpa mollit sint proident. Dolore cillum ullamco nisi proident laboris do do voluptate consectetur et exercitation. Cillum ea sunt reprehenderit ea do pariatur dolor duis nisi ipsum fugiat qui irure cupidatat.

Non tempor laborum laborum occaecat quis. Magna dolore laborum commodo ex laborum enim fugiat pariatur sunt sunt ex labore culpa proident dolore. Irure in non sint. Labore velit adipisicing fugiat officia amet nostrud quis consectetur in eiusmod anim do labore occaecat. Minim sit dolore ipsum duis non excepteur reprehenderit tempor laborum sit deserunt.

Nulla est irure occaecat ex quis do est cillum exercitation qui irure incididunt ipsum voluptate velit. Irure dolor enim aute commodo laboris laboris sit in eu ex voluptate proident ex irure irure. Id tempor nostrud ipsum fugiat deserunt esse tempor veniam anim nulla Lorem nulla non aliqua. Deserunt id amet reprehenderit est amet dolor occaecat pariatur eu est. Elit ut do deserunt nostrud laboris. Occaecat officia duis fugiat eiusmod veniam veniam consequat ea. Aliquip officia fugiat labore aute proident. Occaecat anim ad proident sunt aute consequat proident nulla esse adipisicing.

Cillum ipsum eu incididunt reprehenderit dolore. Occaecat aliqua sit laborum dolore dolore dolore veniam sit id. Proident culpa non velit sit dolor culpa adipisicing. Enim excepteur consectetur cupidatat ex sit fugiat sunt commodo sit do. Laboris eu ipsum cillum pariatur in elit eiusmod. Pariatur proident et esse fugiat esse. Consectetur labore cillum do ut id. Aliqua eu non magna ut anim aliqua nulla do cupidatat excepteur dolore tempor eu labore nostrud.
        """,
    ]

    print("=" * 70)
    print("HUFFMAN ENCODING vs ASCII ENCODING")
    print("=" * 70)

    for text in examples:
        print(f"\n{'─' * 70}")
        print(f"Text: '{text}'")
        print(f"Length: {len(text)} characters")

        # ASCII encoding size (8 bits per character)
        ascii_bits = len(text) * 8

        # Build Huffman tree and get codes
        tree = build_huffman_tree(text)
        codes = encoding(tree)

        # Huffman encoded size
        encoded = encode(text, codes)
        huffman_bits = len(encoded)

        # Calculate savings
        bytes_saved = (ascii_bits - huffman_bits) / 8
        percent_saved = ((ascii_bits - huffman_bits) / ascii_bits) * 100

        print(f"\nASCII encoding:     {ascii_bits} bits ({ascii_bits // 8} bytes)")
        print(f"Huffman encoding:   {huffman_bits} bits ({huffman_bits / 8:.2f} bytes)")
        print(f"\nSPACE SAVED:        {bytes_saved:.1f} bytes ({percent_saved:.1f}%)")

        print(f"\nCharacter codes:")
        for char, code in sorted(codes.items()):
            display_char = repr(char)[1:-1]  # Pretty print special chars
            print(f"  '{display_char}': {code} ({len(code)} bits)")

    print(f"\n{'═' * 70}")
