"""
Huffman Coding Implementation
Following "Introduction to Algorithms" (CLRS) style.

The algorithm builds an optimal prefix-free code for a given set of characters
and their frequencies. It uses a greedy approach with a min-priority queue.
"""

import heapq
from collections import Counter


def build_frequency_table(text):
    """Count frequency of each character in text."""
    return Counter(text)


def huffman(freq):
    """
    HUFFMAN(C) - Build Huffman tree from frequency table.

    Input: freq - dictionary mapping characters to frequencies
    Returns: root of the Huffman tree

    Tree nodes are tuples: (frequency, node_id, left, right, char)
    - Leaf nodes: (freq, id, None, None, char)
    - Internal nodes: (freq, id, left, right, None)

    node_id is used to break ties in heap comparison.
    """
    # Build initial heap of leaf nodes
    heap = []
    node_id = 0

    for char, f in freq.items():
        # (frequency, unique_id, left, right, character)
        node = (f, node_id, None, None, char)
        heapq.heappush(heap, node)
        node_id += 1

    # Special case: single character
    if len(heap) == 1:
        node = heapq.heappop(heap)
        root = (node[0], node_id, node, None, None)
        return root

    # Build tree by combining two minimum nodes
    while len(heap) > 1:
        # Extract two nodes with minimum frequency
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        # Create internal node with combined frequency
        combined_freq = left[0] + right[0]
        internal = (combined_freq, node_id, left, right, None)
        node_id += 1

        heapq.heappush(heap, internal)

    return heap[0]


def build_codes(root):
    """
    Traverse Huffman tree to build code table.

    Returns: dictionary mapping characters to binary strings
    """
    codes = {}

    def traverse(node, code):
        if node is None:
            return

        freq, node_id, left, right, char = node

        # Leaf node - store the code
        if char is not None:
            codes[char] = code if code else "0"  # Handle single char case
            return

        # Internal node - recurse
        traverse(left, code + "0")
        traverse(right, code + "1")

    traverse(root, "")
    return codes


def encode(text, codes):
    """Encode text using the code table."""
    return "".join(codes[char] for char in text)


def decode(encoded, root):
    """Decode binary string using the Huffman tree."""
    if root is None:
        return ""

    result = []
    node = root

    # Handle single character case
    freq, node_id, left, right, char = root
    if char is not None:
        return char * len(encoded)

    for bit in encoded:
        if bit == "0":
            node = node[2]  # left child
        else:
            node = node[3]  # right child

        # Check if leaf
        if node[4] is not None:
            result.append(node[4])
            node = root

    return "".join(result)


def compress(text):
    """
    Full compression pipeline.

    Returns: (encoded_string, huffman_tree, code_table, stats)
    """
    if not text:
        return "", None, {}, {}

    # Build frequency table
    freq = build_frequency_table(text)

    # Build Huffman tree
    tree = huffman(freq)

    # Build code table
    codes = build_codes(tree)

    # Encode text
    encoded = encode(text, codes)

    # Calculate statistics
    original_bits = len(text) * 8  # ASCII
    compressed_bits = len(encoded)

    stats = {
        "original_chars": len(text),
        "unique_chars": len(freq),
        "original_bits": original_bits,
        "compressed_bits": compressed_bits,
        "compression_ratio": compressed_bits / original_bits if original_bits > 0 else 0,
        "space_saved_percent": (1 - compressed_bits / original_bits) * 100 if original_bits > 0 else 0,
        "avg_bits_per_char": compressed_bits / len(text) if text else 0,
    }

    return encoded, tree, codes, stats


def decompress(encoded, tree):
    """Decompress encoded string using Huffman tree."""
    return decode(encoded, tree)
