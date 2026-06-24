#!/usr/bin/env python3
"""Regex NFA engine demo."""

from regex_nfa import match


def main():
    print("=== Regex NFA Engine Demo ===
")

    tests = [
        ("a(bc)*d", ["ad", "abcd", "abcbcd", "abc"]),
        ("cat|dog", ["cat", "dog", "bird"]),
        ("[abc]+", ["aabcc", "d", ""]),
        ("(0|1)+", ["0110", "2", ""]),
    ]

    for pattern, texts in tests:
        for text in texts:
            result = "MATCH" if match(pattern, text) else "NO MATCH"
            print(f"  /{pattern}/ vs '{text}': {result}")
        print()


if __name__ == "__main__":
    main()
