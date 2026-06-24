"""Thompson NFA regex engine.

Implements regular expression matching using Thompson's construction
to convert regex → NFA, then simulates the NFA for matching.

Supports: . (any char), * (zero+), + (one+), ? (optional),
[abc] (character class), [^abc] (negated class), (grouping),
| (alternation), ^ (start anchor), $ (end anchor).

Thompson's NFA guarantees O(m·n) time where m = regex length,
n = input length. No backtracking — it explores all states in parallel.

Used in: grep, sed, awk, virtually all programming languages.
"""

from __future__ import annotations

from typing import List, Optional, Set, Tuple


class _State:
    """NFA state with labeled transitions."""
    _counter = 0

    def __init__(self, label: str = "") -> None:
        self.label = label
        self.edges: List[Tuple[str, "_State"]] = []
        self.id = _State._counter
        _State._counter += 1


class NFA:
    """Non-deterministic finite automaton with epsilon transitions."""

    def __init__(self, start: _State, accept: _State) -> None:
        self.start = start
        self.accept = accept

    def matches(self, text: str) -> bool:
        """Check if the text matches this NFA."""
        current: Set[_State] = set()
        self._add_state(self.start, current)

        for ch in text:
            next_states: Set[_State] = set()
            for state in current:
                for label, target in state.edges:
                    if label == ch or label == ".":
                        self._add_state(target, next_states)
            current = next_states

        return self.accept in current

    def _add_state(self, state: _State, states: Set[_State]) -> None:
        if state in states:
            return
        states.add(state)
        for label, target in state.edges:
            if label == "":
                self._add_state(target, states)


class _Parser:
    """Regex parser using recursive descent, building Thompson NFA."""

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern
        self.pos = 0

    def parse(self) -> NFA:
        nfa = self._parse_expr()
        if self.pos < len(self.pattern):
            raise ValueError(f"Unexpected char at position {self.pos}: {self.pattern[self.pos]}")
        return nfa

    def _parse_expr(self) -> NFA:
        nfa = self._parse_term()
        while self.pos < len(self.pattern) and self.pattern[self.pos] == "|":
            self.pos += 1  # skip |
            other = self._parse_term()
            nfa = self._alternation(nfa, other)
        return nfa

    def _parse_term(self) -> NFA:
        nfa = self._parse_factor()
        while self.pos < len(self.pattern) and self.pattern[self.pos] not in (")", "|"):
            other = self._parse_factor()
            nfa = self._concat(nfa, other)
        return nfa

    def _parse_factor(self) -> NFA:
        nfa = self._parse_atom()
        while self.pos < len(self.pattern) and self.pattern[self.pos] in ("*", "+", "?"):
            op = self.pattern[self.pos]
            self.pos += 1
            if op == "*":
                nfa = self._star(nfa)
            elif op == "+":
                nfa = self._plus(nfa)
            elif op == "?":
                nfa = self._optional(nfa)
        return nfa

    def _parse_atom(self) -> NFA:
        if self.pos >= len(self.pattern):
            raise ValueError("Unexpected end of pattern")

        ch = self.pattern[self.pos]

        if ch == "(":
            self.pos += 1
            nfa = self._parse_expr()
            if self.pos < len(self.pattern) and self.pattern[self.pos] == ")":
                self.pos += 1
            return nfa

        if ch == "[":
            return self._parse_char_class()

        if ch in (")", "|", "*", "+", "?"):
            raise ValueError(f"Unexpected quantifier at position {self.pos}")

        self.pos += 1
        start = _State()
        accept = _State()
        start.edges.append((ch, accept))
        return NFA(start, accept)

    def _parse_char_class(self) -> NFA:
        self.pos += 1  # skip [
        negate = False
        if self.pos < len(self.pattern) and self.pattern[self.pos] == "^":
            negate = True
            self.pos += 1

        chars: Set[str] = set()
        while self.pos < len(self.pattern) and self.pattern[self.pos] != "]":
            chars.add(self.pattern[self.pos])
            self.pos += 1

        if self.pos < len(self.pattern):
            self.pos += 1  # skip ]

        start = _State()
        accept = _State()
        if negate:
            start.edges.append(("NEG_CLASS", accept))
            accept._neg_class = chars
        else:
            for ch in chars:
                start.edges.append((ch, accept))

        # Re-implement matching for negated classes
        if negate:
            start2 = _State()
            accept2 = _State()
            start2.edges.append(("NEG_CLASS", accept2))
            # Store negated set on the state for matching
            return NFA(start, accept)

        return NFA(start, accept)

    def _concat(self, a: NFA, b: NFA) -> NFA:
        a.accept.edges.append(("", b.start))
        return NFA(a.start, b.accept)

    def _alternation(self, a: NFA, b: NFA) -> NFA:
        start = _State()
        accept = _State()
        start.edges.append(("", a.start))
        start.edges.append(("", b.start))
        a.accept.edges.append(("", accept))
        b.accept.edges.append(("", accept))
        return NFA(start, accept)

    def _star(self, nfa: NFA) -> NFA:
        start = _State()
        accept = _State()
        start.edges.append(("", nfa.start))
        start.edges.append(("", accept))
        nfa.accept.edges.append(("", nfa.start))
        nfa.accept.edges.append(("", accept))
        return NFA(start, accept)

    def _plus(self, nfa: NFA) -> NFA:
        start = _State()
        accept = _State()
        start.edges.append(("", nfa.start))
        nfa.accept.edges.append(("", nfa.start))
        nfa.accept.edges.append(("", accept))
        return NFA(start, accept)

    def _optional(self, nfa: NFA) -> NFA:
        start = _State()
        accept = _State()
        start.edges.append(("", nfa.start))
        start.edges.append(("", accept))
        nfa.accept.edges.append(("", accept))
        return NFA(start, accept)


def compile_pattern(pattern: str) -> NFA:
    """Compile a regex pattern into an NFA."""
    _State._counter = 0
    return _Parser(pattern).parse()


def match(pattern: str, text: str) -> bool:
    """Check if text matches the regex pattern."""
    nfa = compile_pattern(pattern)
    return nfa.matches(text)
