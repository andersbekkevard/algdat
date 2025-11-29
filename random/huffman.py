#!/usr/bin/python3
# coding=utf-8
from __future__ import annotations

# ===================================================================
# HUFFMAN ENCODING EKSAMENSØVELSE
# ===================================================================
# Testsettet på serveren er større og mer omfattende enn dette.
# Hvis programmet ditt fungerer lokalt, men ikke når du laster det opp,
# er det gode sjanser for at det er tilfeller du ikke har tatt høyde for.
#
# Denne filen tester din evne til å:
#   1. Bygge et Huffman-tre fra en tekst
#   2. Lage en encoding-dict fra et tre
#   3. Encode tekst med en encoding-dict
#   4. Decode tekst med et Huffman-tre

# Kontroller hvilke tester som kjøres
test_build_tree = True
test_encoding = True
test_encode = True
test_decode = True


# ===================================================================
# NODE-KLASSEN (ferdig implementert)
# ===================================================================
class Node:
    def __init__(self, character=None, frequency=0):
        self.character = character
        self.frequency = frequency
        self.left: Node | None = None
        self.right: Node | None = None

    def __lt__(self, other):
        return self.frequency < other.frequency

    def __str__(self):
        if self.character is not None:
            representation = f"● '{self.character}' (freq: {self.frequency})\n"
        else:
            representation = f"○ (freq: {self.frequency})\n"
        if self.left is not None:
            representation += f"┣━━━┓ (venstre)"
            representation += "\n┃   " + str(self.left).replace("\n", "\n┃   ")
            representation += f"\n┗━━━┓ (høyre)"
            representation += "\n    " + str(self.right).replace("\n", "\n    ")
        return representation

    @classmethod
    def from_dict(cls, dic):
        """Bygg et tre fra en dict-representasjon."""
        if dic is None:
            return None
        node = Node()
        node.left = cls.from_dict(dic.get("left") or dic.get("l"))
        node.right = cls.from_dict(dic.get("right") or dic.get("r"))
        node.character = dic.get("character") or dic.get("c")
        node.frequency = dic.get("frequency") or dic.get("f", 0)
        return node


# ===================================================================
# IMPLEMENTER DISSE FUNKSJONENE
# ===================================================================


def build_huffman_tree(text: str) -> Node:
    """Bygg et Huffman-tre fra en tekst."""
    assert len(text) > 0, "Cannot build Huffman tree from empty text"

    count_dict: dict[str, int] = {}
    for character in text:
        count_dict[character] = count_dict.get(character, 0) + 1
    nodes: list[Node] = [Node(char, freq) for char, freq in count_dict.items()]
    n = len(nodes)

    def min_heapify(A: list[Node], n: int, i: int) -> None:
        l = 2 * i + 1
        r = 2 * i + 2
        m = i
        if l < n and A[l] < A[m]:
            m = l
        if r < n and A[r] < A[m]:
            m = r
        if m != i:
            A[i], A[m] = A[m], A[i]
            min_heapify(A, n, m)

    def extract_min(A: list[Node]) -> Node:
        n = len(A)
        A[0], A[n - 1] = A[n - 1], A[0]
        min_heapify(A, n - 1, 0)
        return A.pop()

    for i in range((n - 2) // 2, -1, -1):
        min_heapify(nodes, n, i)

    def parent(i: int) -> int:
        return (i - 1) // 2

    while len(nodes) > 1:
        l = extract_min(nodes)
        r = extract_min(nodes)
        combined = Node(None, l.frequency + r.frequency)
        combined.left = l
        combined.right = r
        nodes.append(combined)
        i = len(nodes) - 1
        while i > 0 and nodes[parent(i)] > nodes[i]:
            nodes[i], nodes[parent(i)] = nodes[parent(i)], nodes[i]
            i = parent(i)

    return nodes[0]


def encoding(
    node: Node, code: str = "", lookup: dict[str, str] | None = None
) -> dict[str, str]:
    """Lag en encoding-dict fra et Huffman-tre."""
    if lookup is None:
        lookup = {}

    if node.left is None and node.right is None:  # Leaf node
        assert node.character is not None
        lookup[node.character] = code or "0"  # Single-char tree gets code "0"
    else:
        assert node.left is not None and node.right is not None
        encoding(node.left, code + "0", lookup)
        encoding(node.right, code + "1", lookup)

    return lookup


def encode(data: str, encoding_dict: dict[str, str]) -> str:
    """Encode en tekst med en encoding-dict."""
    return "".join(encoding_dict[c] for c in data)


def decode(data: str, root: Node) -> str:
    """Decode en bitstreng med et Huffman-tre."""
    # Single-character tree: root is a leaf
    if root.left is None and root.right is None:
        assert root.character is not None
        return root.character * len(data)

    chars: list[str] = []
    node = root
    for bit in data:
        assert node.left is not None and node.right is not None
        node = node.left if bit == "0" else node.right
        if node.left is None and node.right is None:  # Leaf node
            assert node.character is not None
            chars.append(node.character)
            node = root

    return "".join(chars)


# ===================================================================
# HJELPEFUNKSJONER FOR TESTING
# ===================================================================


def is_prefix_free(encoding_dict: dict) -> bool:
    """Sjekk at ingen kode er prefiks av en annen."""
    codes = list(encoding_dict.values())
    for i, code1 in enumerate(codes):
        for j, code2 in enumerate(codes):
            if i != j and code2.startswith(code1):
                return False
    return True


def calc_encoding_length(text: str, encoding_dict: dict) -> int:
    """Beregn totallengden av encoded tekst."""
    return sum(len(encoding_dict.get(c, "")) for c in text)


def is_optimal_encoding(text: str, encoding_dict: dict) -> bool:
    """
    Sjekk om encodingen er optimal (eller nesten optimal).
    En optimal Huffman-encoding gir minst mulig antall bits.
    """
    # Tell frekvenser
    freq = {}
    for c in text:
        freq[c] = freq.get(c, 0) + 1

    # Sjekk at hyppigere tegn har kortere eller lik kodelengde
    sorted_chars = sorted(freq.keys(), key=lambda c: -freq[c])
    for i, c1 in enumerate(sorted_chars):
        for c2 in sorted_chars[i + 1 :]:
            if c1 in encoding_dict and c2 in encoding_dict:
                if (
                    len(encoding_dict[c1]) > len(encoding_dict[c2])
                    and freq[c1] > freq[c2]
                ):
                    # Mer frekvent tegn har lengre kode - ikke optimalt
                    return False
    return True


# ===================================================================
# TEST 1: BYGG HUFFMAN-TRE
# ===================================================================

build_tree_tests = [
    # (tekst, forventet antall unike tegn)
    ("a", 1),
    ("ab", 2),
    ("aab", 2),
    ("aaabbc", 3),
    ("mississippi", 4),
    ("hello world", 8),
    ("abcdefgh", 8),
    ("aaaaaabbbbccd", 4),
]


def run_build_tree_tests():
    print("\n" + "=" * 60)
    print("TEST 1: BYGG HUFFMAN-TRE")
    print("=" * 60)

    failed = False
    for text, expected_chars in build_tree_tests:
        tree = build_huffman_tree(text)

        if tree is None:
            if failed:
                print("-" * 50)
            failed = True
            print(f"\nFeilet for tekst: '{text}'")
            print("  Du returnerte None")
            continue

        # Sjekk at treet har riktig struktur
        enc = encoding(tree)
        if enc is None:
            if failed:
                print("-" * 50)
            failed = True
            print(f"\nFeilet for tekst: '{text}'")
            print("  encoding() returnerte None - implementer encoding() først")
            continue

        if len(enc) != expected_chars:
            if failed:
                print("-" * 50)
            failed = True
            print(f"\nFeilet for tekst: '{text}'")
            print(f"  Forventet {expected_chars} unike tegn, fikk {len(enc)}")
            print(f"  Din encoding: {enc}")
            continue

        # Sjekk at det er prefix-free
        if not is_prefix_free(enc):
            if failed:
                print("-" * 50)
            failed = True
            print(f"\nFeilet for tekst: '{text}'")
            print("  Encodingen er ikke prefix-free!")
            print(f"  Din encoding: {enc}")
            continue

        # Sjekk at alle tegn i teksten har en kode
        for c in text:
            if c not in enc:
                if failed:
                    print("-" * 50)
                failed = True
                print(f"\nFeilet for tekst: '{text}'")
                print(f"  Tegnet '{c}' mangler i encoding")
                break

    if not failed:
        print("✓ Alle build_huffman_tree-tester bestått!")
    return not failed


# ===================================================================
# TEST 2: ENCODING (TRE -> DICT)
# ===================================================================

encoding_tests = [
    # (tre-dict, forventet encoding)
    (
        {"left": {"character": "a"}, "right": {"character": "b"}},
        {"a": "0", "b": "1"},
    ),
    (
        {
            "left": {"character": "c"},
            "right": {
                "left": {"character": "a"},
                "right": {"character": "b"},
            },
        },
        {"c": "0", "a": "10", "b": "11"},
    ),
    (
        {
            "left": {"character": "a"},
            "right": {
                "left": {"character": "b"},
                "right": {
                    "left": {"character": "c"},
                    "right": {"character": "d"},
                },
            },
        },
        {"a": "0", "b": "10", "c": "110", "d": "111"},
    ),
    (
        {
            "left": {
                "left": {"character": "a"},
                "right": {"character": "b"},
            },
            "right": {
                "left": {"character": "c"},
                "right": {"character": "d"},
            },
        },
        {"a": "00", "b": "01", "c": "10", "d": "11"},
    ),
    (
        {
            "left": {
                "left": {
                    "left": {"character": "a"},
                    "right": {"character": "b"},
                },
                "right": {"character": "c"},
            },
            "right": {"character": "d"},
        },
        {"a": "000", "b": "001", "c": "01", "d": "1"},
    ),
]


def run_encoding_tests():
    print("\n" + "=" * 60)
    print("TEST 2: ENCODING (TRE -> DICT)")
    print("=" * 60)

    failed = False
    for tree_dict, expected in encoding_tests:
        tree = Node.from_dict(tree_dict)
        result = encoding(tree)  # type: ignore

        if result is None:
            if failed:
                print("-" * 50)
            failed = True
            print(f"\nFeilet for tre:")
            print(tree)
            print("  Du returnerte None")
            continue

        if result != expected:
            if failed:
                print("-" * 50)
            failed = True
            print(f"\nFeilet for tre:")
            print(tree)
            print(f"  Ditt svar:    {result}")
            print(f"  Forventet:    {expected}")

    if not failed:
        print("✓ Alle encoding-tester bestått!")
    return not failed


# ===================================================================
# TEST 3: ENCODE (TEKST + DICT -> BITSTRENG)
# ===================================================================

encode_tests = [
    # (tekst, encoding-dict, forventet bitstreng)
    ("na", {"n": "0", "a": "1"}, "01"),
    ("na", {"n": "1", "a": "0"}, "10"),
    ("nabn", {"n": "1", "a": "01", "b": "10"}, "101101"),
    ("abccba", {"a": "00", "b": "01", "c": "1"}, "0001110100"),
    ("accca", {"c": "0", "a": "1"}, "10001"),
    ("abbca", {"a": "01", "b": "1", "c": "00"}, "01110001"),
    ("ffXf", {"X": "0", "f": "1"}, "1101"),
    ("hello", {"h": "00", "e": "01", "l": "1", "o": "001"}, "000111001"),
    ("aaa", {"a": "0"}, "000"),
    ("abc", {"a": "00", "b": "01", "c": "1"}, "00011"),
]


def run_encode_tests():
    print("\n" + "=" * 60)
    print("TEST 3: ENCODE (TEKST + DICT -> BITSTRENG)")
    print("=" * 60)

    failed = False
    for data, enc_dict, expected in encode_tests:
        result = encode(data, enc_dict)

        if result is None:
            if failed:
                print("-" * 50)
            failed = True
            print(f"\nFeilet for tekst: '{data}' med encoding {enc_dict}")
            print("  Du returnerte None")
            continue

        if result != expected:
            if failed:
                print("-" * 50)
            failed = True
            print(f"\nFeilet for tekst: '{data}'")
            print(f"  Encoding: {enc_dict}")
            print(f"  Ditt svar:    '{result}'")
            print(f"  Forventet:    '{expected}'")

    if not failed:
        print("✓ Alle encode-tester bestått!")
    return not failed


# ===================================================================
# TEST 4: DECODE (BITSTRENG + TRE -> TEKST)
# ===================================================================

decode_tests = [
    # (bitstreng, tre-dict, forventet tekst)
    (
        "01",
        {"left": {"character": "n"}, "right": {"character": "a"}},
        "na",
    ),
    (
        "10",
        {"left": {"character": "a"}, "right": {"character": "n"}},
        "na",
    ),
    (
        "0001110100",
        {
            "left": {
                "left": {"character": "a"},
                "right": {"character": "b"},
            },
            "right": {"character": "c"},
        },
        "abccba",
    ),
    (
        "000",
        {"character": "a"},  # Enkelttegn-tre (spesialtilfelle)
        "aaa",
    ),
    (
        "1101",
        {"left": {"character": "X"}, "right": {"character": "f"}},
        "ffXf",
    ),
    (
        "010110",
        {
            "left": {"character": "n"},
            "right": {
                "left": {"character": "a"},
                "right": {"character": "b"},
            },
        },
        "nabn",
    ),
]


def run_decode_tests():
    print("\n" + "=" * 60)
    print("TEST 4: DECODE (BITSTRENG + TRE -> TEKST)")
    print("=" * 60)

    failed = False
    for data, tree_dict, expected in decode_tests:
        tree = Node.from_dict(tree_dict)
        result = decode(data, tree)  # type: ignore

        if result is None:
            if failed:
                print("-" * 50)
            failed = True
            print(f"\nFeilet for bitstreng: '{data}'")
            print(f"  Tre:")
            print(tree)
            print("  Du returnerte None")
            continue

        if result != expected:
            if failed:
                print("-" * 50)
            failed = True
            print(f"\nFeilet for bitstreng: '{data}'")
            print(f"  Tre:")
            print(tree)
            print(f"  Ditt svar:    '{result}'")
            print(f"  Forventet:    '{expected}'")

    if not failed:
        print("✓ Alle decode-tester bestått!")
    return not failed


# ===================================================================
# TEST 5: INTEGRASJONSTEST (HELE FLYTEN)
# ===================================================================

integration_tests = [
    "hello world",
    "mississippi",
    "aaaaaabbbbccd",
    "the quick brown fox",
    "abcdefghijklmnop",
    "aaaaaa",
    "ab",
]


def run_integration_tests():
    print("\n" + "=" * 60)
    print("TEST 5: INTEGRASJONSTEST (HELE FLYTEN)")
    print("=" * 60)

    failed = False
    for text in integration_tests:
        # Bygg tre
        tree = build_huffman_tree(text)
        if tree is None:
            if failed:
                print("-" * 50)
            failed = True
            print(f"\nFeilet for tekst: '{text}'")
            print("  build_huffman_tree returnerte None")
            continue

        # Lag encoding
        enc = encoding(tree)
        if enc is None:
            if failed:
                print("-" * 50)
            failed = True
            print(f"\nFeilet for tekst: '{text}'")
            print("  encoding returnerte None")
            continue

        # Encode
        encoded = encode(text, enc)
        if encoded is None:
            if failed:
                print("-" * 50)
            failed = True
            print(f"\nFeilet for tekst: '{text}'")
            print("  encode returnerte None")
            continue

        # Decode
        decoded = decode(encoded, tree)
        if decoded is None:
            if failed:
                print("-" * 50)
            failed = True
            print(f"\nFeilet for tekst: '{text}'")
            print("  decode returnerte None")
            continue

        # Sjekk at vi får tilbake originalteksten
        if decoded != text:
            if failed:
                print("-" * 50)
            failed = True
            print(f"\nFeilet for tekst: '{text}'")
            print(f"  Encoded: '{encoded}'")
            print(f"  Decoded: '{decoded}'")
            print(f"  (Forventet: '{text}')")
            continue

        # Sjekk at encodingen er prefix-free
        if not is_prefix_free(enc):
            if failed:
                print("-" * 50)
            failed = True
            print(f"\nFeilet for tekst: '{text}'")
            print("  Encodingen er ikke prefix-free!")
            print(f"  Encoding: {enc}")

    if not failed:
        print("✓ Alle integrasjonstester bestått!")
    return not failed


# ===================================================================
# KJØR TESTENE
# ===================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("HUFFMAN ENCODING - EKSAMENØVELSE")
    print("=" * 60)

    results = []

    if test_encoding:
        results.append(("encoding (tre -> dict)", run_encoding_tests()))

    if test_encode:
        results.append(("encode (tekst + dict -> bits)", run_encode_tests()))

    if test_decode:
        results.append(("decode (bits + tre -> tekst)", run_decode_tests()))

    if test_build_tree:
        results.append(("build_huffman_tree", run_build_tree_tests()))

    # Kun kjør integrasjonstester hvis alt annet fungerer
    if all(r[1] for r in results):
        results.append(("integrasjonstest", run_integration_tests()))

    # Oppsummering
    print("\n" + "=" * 60)
    print("OPPSUMMERING")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        status = "✓ BESTÅTT" if passed else "✗ FEILET"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n🎉 Alle tester bestått! Du er klar for eksamen!")
    else:
        print("\n❌ Noen tester feilet. Fortsett å øve!")
