"""Tests for regex NFA engine."""

import pytest
from regex_nfa import match


class TestRegexNFA:
    def test_literal(self):
        assert match("abc", "abc")
        assert not match("abc", "abd")

    def test_dot(self):
        assert match("a.c", "abc")
        assert match("a.c", "axc")

    def test_star(self):
        assert match("a*", "")
        assert match("a*", "aaa")
        assert match("ab*c", "ac")
        assert match("ab*c", "abbc")

    def test_plus(self):
        assert not match("a+", "")
        assert match("a+", "aaa")

    def test_optional(self):
        assert match("ab?c", "ac")
        assert match("ab?c", "abc")

    def test_alternation(self):
        assert match("cat|dog", "cat")
        assert match("cat|dog", "dog")
        assert not match("cat|dog", "bird")

    def test_grouping(self):
        assert match("(ab)+", "ababab")
        assert not match("(ab)+", "aba")

    def test_char_class(self):
        assert match("[abc]", "a")
        assert match("[abc]", "c")
        assert not match("[abc]", "d")

    def test_complex(self):
        assert match("a(bc)*d", "ad")
        assert match("a(bc)*d", "abcbcd")
        assert not match("a(bc)*d", "abc")
