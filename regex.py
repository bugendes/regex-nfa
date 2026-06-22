#!/usr/bin/env python3
"""Simple regex engine — supports . and * via NFA simulation."""

def match(pattern, text):
    """NFA-based regex match supporting . and *."""
    def matches(p_idx, t_idx):
        if p_idx == len(pattern): return t_idx == len(text)
        if p_idx + 1 < len(pattern) and pattern[p_idx + 1] == '*':
            if matches(p_idx + 2, t_idx): return True
            while t_idx < len(text) and (pattern[p_idx] == text[t_idx] or pattern[p_idx] == '.'):
                if matches(p_idx + 2, t_idx + 1): return True
                t_idx += 1
            return False
        if t_idx < len(text) and (pattern[p_idx] == text[t_idx] or pattern[p_idx] == '.'):
            return matches(p_idx + 1, t_idx + 1)
        return False
    return matches(0, 0)

if __name__ == "__main__":
    tests = [("a*", "", True), ("a*", "aaa", True), ("a*b", "b", True),
             ("a*b", "aab", True), (".b", "xb", True), ("a.b", "ab", False)]
    for p, t, exp in tests:
        r = match(p, t)
        print(f"  {"OK" if r==exp else "FAIL"} match('{p}','{t}') = {r}")\n