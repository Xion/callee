"""
Tests for operators' matchers.
"""
from itertools import chain, combinations

import callee.operators as __unit__
from tests import MatcherTestCase


class OperatorTestCase(MatcherTestCase):
    """Base class for operator matchers' tests."""

    def subsets(self, s, strict=False):
        """Return a set of all subsets of set ``s``."""
        max_subset_size = len(s)
        if not strict:
            max_subset_size += 1
        return set(map(frozenset,
                       chain.from_iterable(combinations(s, n)
                                           for n in range(max_subset_size))))


# Simple comparisons

class Less(OperatorTestCase):

    def test_numbers(self):
        ref = 42

        self.assert_match(0, ref)
        self.assert_match(-ref, ref)
        self.assert_match(3.14, ref)

        self.assert_no_match(ref, ref)
        self.assert_no_match(2 * ref, ref)

    def test_strings(self):
        ref = "Alice has a cat"

        for i in range(len(ref) - 1):
            self.assert_match(ref[:i], ref)

        self.assert_no_match(ref, ref)
        self.assert_no_match(2 * ref, ref)
        self.assert_no_match("Bob has a cat", ref)

    def test_sets(self):
        ref = set([1, 2, 3, 5])

        for s in self.subsets(ref, strict=True):
            self.assert_match(s, ref)

        self.assert_no_match(ref, ref)
        self.assert_no_match(ref | set([7]), ref)
        self.assert_no_match(set([0]), ref)

    # Assertion functions

    def assert_match(self, value, ref):
        return super(Less, self).assert_match(__unit__.Less(ref), value)

    def assert_no_match(self, value, ref):
        return super(Less, self).assert_no_match(__unit__.Less(ref), value)


class LessOrEqual(OperatorTestCase):

    def test_numbers(self):
        ref = 42

        self.assert_match(0, ref)
        self.assert_match(-ref, ref)
        self.assert_match(3.14, ref)
        self.assert_match(ref, ref)

        self.assert_no_match(2 * ref, ref)

    def test_strings(self):
        ref = "Alice has a cat"

        for i in range(len(ref) - 1):
            self.assert_match(ref[:i], ref)
        self.assert_match(ref, ref)

        self.assert_no_match(2 * ref, ref)
        self.assert_no_match("Bob has a cat", ref)

    def test_sets(self):
        ref = set([1, 2, 3, 5])

        for s in self.subsets(ref):
            self.assert_match(s, ref)

        self.assert_no_match(ref | set([7]), ref)
        self.assert_no_match(set([0]), ref)

    # Assertion functions

    def assert_match(self, value, ref):
        return super(LessOrEqual, self) \
            .assert_match(__unit__.LessOrEqual(ref), value)

    def assert_no_match(self, value, ref):
        return super(LessOrEqual, self) \
            .assert_no_match(__unit__.LessOrEqual(ref), value)


class Greater(OperatorTestCase):

    def test_numbers(self):
        ref = 42

        self.assert_match(2 * ref, ref)

        self.assert_no_match(0, ref)
        self.assert_no_match(-ref, ref)
        self.assert_no_match(3.14, ref)
        self.assert_no_match(ref, ref)

    def test_strings(self):
        ref = "Alice has a cat"

        self.assert_match(2 * ref, ref)
        self.assert_match("Bob has a cat", ref)

        for i in range(len(ref) - 1):
            self.assert_no_match(ref[:i], ref)
        self.assert_no_match(ref, ref)

    def test_sets(self):
        ref = set([1, 2, 3, 5])

        self.assert_match(ref | set([7]), ref)

        for s in self.subsets(ref):
            self.assert_no_match(s, ref)
        self.assert_no_match(set([0]), ref)

    # Assertion functions

    def assert_match(self, value, ref):
        return super(Greater, self).assert_match(__unit__.Greater(ref), value)

    def assert_no_match(self, value, ref):
        return super(Greater, self) \
            .assert_no_match(__unit__.Greater(ref), value)


class GreaterOrEqual(OperatorTestCase):

    def test_numbers(self):
        ref = 42

        self.assert_match(ref, ref)
        self.assert_match(2 * ref, ref)

        self.assert_no_match(0, ref)
        self.assert_no_match(-ref, ref)
        self.assert_no_match(3.14, ref)

    def test_strings(self):
        ref = "Alice has a cat"

        self.assert_match(ref, ref)
        self.assert_match(2 * ref, ref)
        self.assert_match("Bob has a cat", ref)

        for i in range(len(ref) - 1):
            self.assert_no_match(ref[:i], ref)

    def test_sets(self):
        ref = set([1, 2, 3, 5])

        self.assert_match(ref, ref)
        self.assert_match(ref | set([7]), ref)

        for s in self.subsets(ref, strict=True):
            self.assert_no_match(s, ref)
        self.assert_no_match(set([0]), ref)

    # Assertion functions

    def assert_match(self, value, ref):
        return super(GreaterOrEqual, self) \
            .assert_match(__unit__.GreaterOrEqual(ref), value)

    def assert_no_match(self, value, ref):
        return super(GreaterOrEqual, self) \
            .assert_no_match(__unit__.GreaterOrEqual(ref), value)


# Length comparisons

class Shorter(OperatorTestCase):

    def test_length_value(self):
        ref = 12

        self.assert_match([], ref)
        self.assert_match([1], ref)
        self.assert_match("Alice", ref)

        self.assert_no_match(range(ref), ref)
        self.assert_no_match('x' * ref, ref)
        self.assert_no_match("Alice has a cat", ref)

    def test_sequence(self):
        ref = [1, 2, 3]

        for s in self.subsets(ref, strict=True):
            self.assert_match(list(s), ref)
        self.assert_match([42] * (len(ref) - 1), ref)

        self.assert_no_match(ref, ref)
        self.assert_no_match(2 * ref, ref)

    # Assertion functions

    def assert_match(self, value, ref):
        return super(Shorter, self).assert_match(__unit__.Shorter(ref), value)

    def assert_no_match(self, value, ref):
        return super(Shorter, self) \
            .assert_no_match(__unit__.Shorter(ref), value)


class ShorterOrEqual(OperatorTestCase):

    def test_length_value(self):
        ref = 12

        self.assert_match([], ref)
        self.assert_match([1], ref)
        self.assert_match("Alice", ref)
        self.assert_match(range(ref), ref)
        self.assert_match('x' * ref, ref)

        self.assert_no_match('x' * (ref + 1), ref)
        self.assert_no_match("Alice has a cat", ref)

    def test_sequence(self):
        ref = [1, 2, 3]

        for s in self.subsets(ref):
            self.assert_match(list(s), ref)
        self.assert_match([42] * (len(ref) - 1), ref)

        self.assert_no_match(2 * ref, ref)

    # Assertion functions

    def assert_match(self, value, ref):
        return super(ShorterOrEqual, self) \
            .assert_match(__unit__.ShorterOrEqual(ref), value)

    def assert_no_match(self, value, ref):
        return super(ShorterOrEqual, self) \
            .assert_no_match(__unit__.ShorterOrEqual(ref), value)


class Longer(OperatorTestCase):

    def test_length_value(self):
        ref = 12

        self.assert_match('x' * (ref + 1), ref)
        self.assert_match("Alice has a cat", ref)

        self.assert_no_match([], ref)
        self.assert_no_match([1], ref)
        self.assert_no_match("Alice", ref)
        self.assert_no_match(range(ref), ref)
        self.assert_no_match('x' * ref, ref)

    def test_sequence(self):
        ref = [1, 2, 3]

        self.assert_match(2 * ref, ref)
        self.assert_match([42] * (len(ref) + 1), ref)

        for s in self.subsets(ref):
            self.assert_no_match(list(s), ref)
        self.assert_no_match([42] * len(ref), ref)

    # Assertion functions

    def assert_match(self, value, ref):
        return super(Longer, self).assert_match(__unit__.Longer(ref), value)

    def assert_no_match(self, value, ref):
        return super(Longer, self) \
            .assert_no_match(__unit__.Longer(ref), value)


class LongerOrEqual(OperatorTestCase):

    def test_length_value(self):
        ref = 12

        self.assert_match('x' * (ref + 1), ref)
        self.assert_match("Alice has a cat", ref)
        self.assert_match(range(ref), ref)
        self.assert_match('x' * ref, ref)

        self.assert_no_match([], ref)
        self.assert_no_match([1], ref)
        self.assert_no_match("Alice", ref)

    def test_sequence(self):
        ref = [1, 2, 3]

        self.assert_match(ref, ref)
        self.assert_match(2 * ref, ref)
        self.assert_match([42] * len(ref), ref)
        self.assert_match([42] * (len(ref) + 1), ref)

        for s in self.subsets(ref, strict=True):
            self.assert_no_match(list(s), ref)

    # Assertion functions

    def assert_match(self, value, ref):
        return super(LongerOrEqual, self) \
            .assert_match(__unit__.LongerOrEqual(ref), value)

    def assert_no_match(self, value, ref):
        return super(LongerOrEqual, self) \
            .assert_no_match(__unit__.LongerOrEqual(ref), value)
