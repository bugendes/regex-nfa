# Regex NFA Engine

A regular expression engine built from scratch using Thompson's NFA construction. Converts regex patterns to non-deterministic finite automata, then simulates all possible states in parallel for matching.

## How It Works

**Thompson's Construction (1968):** Each regex primitive maps to a small NFA fragment with epsilon (empty) transitions. Fragments are composed via concatenation, alternation, and repetition:

- **Literal `a`:** Two states with a single `a`-labeled edge.
- **Concatenation `AB`:** Connect A's accept to B's start via epsilon.
- **Alternation `A|B`:** New start fans out to A and B; both accept states merge to a new accept.
- **Star `A*`:** Epsilon from start to A's start and to accept; epsilon from A's accept back to A's start and to accept.

**Simulation:** Instead of backtracking, track the set of all active states simultaneously. For each input character, advance all active states. This guarantees O(m·n) time — no exponential blowup from patterns like `(a+)+b`.

**Parser:** Recursive descent: expression → term → factor → atom, with quantifiers (`*`, `+`, `?`) applied at the factor level.

## Complexity

| Operation | Time | Notes |
|-----------|------|-------|
| compile   | O(m) | m = pattern length |
| match     | O(m·n) | n = text length, no backtracking |

Space: O(m) states in the NFA, O(m) active states during simulation.

## Supported Syntax

| Syntax | Meaning |
|--------|---------|
| `.` | Any single character |
| `*` | Zero or more of previous |
| `+` | One or more of previous |
| `?` | Zero or one of previous |
| `[abc]` | Character class |
| `(...)` | Grouping |
| `\|` | Alternation |

## Applications

**Text Processing:** grep, sed, awk — all use regex engines. Thompson NFA is the theoretical foundation; production engines add back-references, lookahead, and optimizations.

**Lexical Analysis:** Compilers use regex (via DFAs derived from NFAs) to tokenize source code.

**Input Validation:** Email addresses, phone numbers, URLs — regex is the universal pattern validator.

**Bioinformatics:** Motif searching in DNA/protein sequences uses regex variants (PROSITE patterns).
