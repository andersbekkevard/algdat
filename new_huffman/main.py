#!/usr/bin/env python3
"""
Huffman Coding Demonstration

This script demonstrates Huffman coding on various text types,
showing how compression effectiveness varies with text characteristics.
"""

import json
from pathlib import Path
from huffman import compress, decompress


def print_header(title):
    """Print a section header."""
    width = 70
    print()
    print("=" * width)
    print(f" {title}".center(width))
    print("=" * width)


def print_subheader(title):
    """Print a subsection header."""
    print()
    print(f"--- {title} ---")


def print_bar(value, max_value, width=40, fill_char="█", empty_char="░"):
    """Create a visual bar representation."""
    filled = int((value / max_value) * width) if max_value > 0 else 0
    return fill_char * filled + empty_char * (width - filled)


def print_code_table(codes, max_display=10):
    """Print the Huffman code table."""
    sorted_codes = sorted(codes.items(), key=lambda x: (len(x[1]), x[0]))

    print(f"\n  {'Char':<8} {'Code':<20} {'Length'}")
    print(f"  {'-'*8} {'-'*20} {'-'*6}")

    for i, (char, code) in enumerate(sorted_codes):
        if i >= max_display and len(sorted_codes) > max_display + 2:
            print(f"  ... and {len(sorted_codes) - max_display} more characters ...")
            break
        # Display special characters nicely
        if char == " ":
            display = "SPACE"
        elif char == "\n":
            display = "NEWLINE"
        elif char == "\t":
            display = "TAB"
        else:
            display = repr(char)[1:-1]
        print(f"  {display:<8} {code:<20} {len(code)}")


def analyze_text(name, description, text):
    """Analyze and display compression results for a text."""
    print_subheader(name)
    print(f"  {description}")

    # Show preview of text
    preview = text[:60].replace("\n", "\\n")
    if len(text) > 60:
        preview += "..."
    print(f'\n  Text preview: "{preview}"')

    # Compress
    encoded, tree, codes, stats = compress(text)

    # Display statistics
    print(f"\n  Statistics:")
    print(f"    Original length:     {stats['original_chars']:>6} characters")
    print(f"    Unique characters:   {stats['unique_chars']:>6}")
    print(f"    Original size:       {stats['original_bits']:>6} bits (8 bits/char)")
    print(f"    Compressed size:     {stats['compressed_bits']:>6} bits")
    print(f"    Avg bits per char:   {stats['avg_bits_per_char']:>6.2f}")

    # Compression ratio visualization
    ratio = stats["compression_ratio"]
    saved = stats["space_saved_percent"]

    print(f"\n  Compression ratio: {ratio:.1%}")
    print(f"    Original:   {print_bar(1.0, 1.0)} 100%")
    print(f"    Compressed: {print_bar(ratio, 1.0)} {ratio*100:.1f}%")
    print(f"\n  Space saved: {saved:.1f}%")

    # Show code table
    print("\n  Huffman Code Table (shortest codes first):")
    print_code_table(codes)

    # Verify correctness
    decoded = decompress(encoded, tree)
    status = "PASSED" if decoded == text else "FAILED"
    print(f"\n  Decode verification: {status}")

    return stats


def main():
    print_header("HUFFMAN CODING DEMONSTRATION")
    print(
        """
  Huffman coding is a greedy algorithm that builds an optimal
  prefix-free binary code. Characters with higher frequencies
  get shorter codes, minimizing the total encoded length.

  Key insight: The algorithm repeatedly combines the two lowest
  frequency nodes, building the tree from leaves to root.
    """
    )

    # Load texts
    texts_path = Path(__file__).parent / "texts.json"
    with open(texts_path) as f:
        texts = json.load(f)

    # Analyze each text
    all_stats = []
    for key, data in texts.items():
        stats = analyze_text(data["name"], data["description"], data["text"])
        stats["name"] = data["name"]
        all_stats.append(stats)

    # Summary comparison
    print_header("COMPRESSION COMPARISON SUMMARY")

    # Sort by compression ratio (best compression first)
    all_stats.sort(key=lambda x: x["compression_ratio"])

    print(f"\n  {'Text Type':<25} {'Ratio':>8} {'Saved':>8} {'Visual'}")
    print(f"  {'-'*25} {'-'*8} {'-'*8} {'-'*40}")

    for stats in all_stats:
        ratio = stats["compression_ratio"]
        saved = stats["space_saved_percent"]
        bar = print_bar(ratio, 1.0, width=30)
        print(f"  {stats['name']:<25} {ratio:>7.1%} {saved:>7.1f}% {bar}")

    # Educational notes
    print_header("KEY OBSERVATIONS")
    print(
        """
  1. REPETITIVE TEXT: Achieves best compression because few unique
     characters mean very short codes for frequent characters.

  2. NATURAL LANGUAGE: Good compression (~40-50% savings) because
     letters like 'e', 't', 'a' appear much more than 'z', 'q'.

  3. DNA SEQUENCES: Only 4 characters, so each gets a 2-bit code.
     Saves 75% compared to 8-bit ASCII (theoretical optimum).

  4. SOURCE CODE: Moderate compression due to keywords, but symbols
     and varied characters reduce effectiveness.

  5. HIGH ENTROPY: Poor compression when characters are uniformly
     distributed - no frequency advantage to exploit.

  Huffman coding achieves OPTIMAL prefix-free encoding, meaning
  no other prefix-free code can do better for the same frequencies.
    """
    )

    # Show entropy relationship
    print_header("THEORETICAL BACKGROUND")
    print(
        """
  Shannon's entropy H gives the theoretical minimum bits per symbol:

      H = -Σ p(x) * log2(p(x))

  Huffman coding achieves: H <= L < H + 1

  where L is the average code length. This means Huffman is always
  within 1 bit of the theoretical optimum!

  The greedy choice property ensures that combining the two minimum
  frequency nodes first always leads to an optimal solution.
    """
    )


if __name__ == "__main__":
    main()
