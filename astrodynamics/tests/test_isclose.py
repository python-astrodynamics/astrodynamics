# coding: utf-8
from __future__ import absolute_import, division, print_function

from decimal import Decimal
from fractions import Fraction

import pytest

from astrodynamics.compat.math import _isclose

eps = 1E-05
NAN = float('nan')
INF = float('inf')
NINF = float('-inf')

# These tests are taken from Python 3.5 stdlib tests for isclose.
# If we're on Python 3.5+, import math.isclose too.

try:
    from math import isclose
except ImportError:
    isclose_functions = [_isclose]
else:
    isclose_functions = [_isclose, isclose]


@pytest.fixture(scope='module', params=isclose_functions)
def isclose_function(request):
    return request.param

# identical values must test as close
identical_examples = [(2.0, 2.0),
                      (0.1e200, 0.1e200),
                      (1.123e-300, 1.123e-300),
                      (12345, 12345.0),
                      (0.0, -0.0),
                      (345678, 345678)]

# examples that are close to 1e-8, but not 1e-9
eight_decimal_places_examples = [(1e8, 1e8 + 1),
                                 (-1e-8, -1.000000009e-8),
                                 (1.12345678, 1.12345679)]

near_zero_examples = [(1e-9, 0.0),
                      (-1e-9, 0.0),
                      (-1e-150, 0.0)]

# these should never be close (following IEEE 754 rules for equality)
not_close_examples = [(NAN, NAN),
                      (NAN, 1e-100),
                      (1e-100, NAN),
                      (INF, NAN),
                      (NAN, INF),
                      (INF, NINF),
                      (INF, 1.0),
                      (1.0, INF),
                      (INF, 1e308),
                      (1e308, INF)]

zero_tolerance_close_examples = [(1.0, 1.0),
                                 (-3.4, -3.4),
                                 (-1e-300, -1e-300)]

zero_tolerance_not_close_examples = [(1.0, 1.000000000000001),
                                     (0.99999999999999, 1.0),
                                     (1.0e200, .999999999999999e200)]

integer_examples = [(100000001, 100000000),
                    (123456789, 123456788)]

decimal_examples = [(Decimal('1.00000001'), Decimal('1.0')),
                    (Decimal('1.00000001e-20'), Decimal('1.0e-20')),
                    (Decimal('1.00000001e-100'), Decimal('1.0e-100'))]

# could use some more examples here!
fraction_examples = [(Fraction(1, 100000000) + 1, Fraction(1))]


def test_negative_tolerances(isclose_function):
    # ValueError should be raised if either tolerance is less than zero
    with pytest.raises(ValueError):
        assert isclose_function(1, 1, rel_tol=-1e-100)
    with pytest.raises(ValueError):
        assert isclose_function(1, 1, rel_tol=1e-100, abs_tol=-1e10)


@pytest.mark.parametrize('a, b', identical_examples)
def test_identical(a, b, isclose_function):
    assert isclose_function(a, b, rel_tol=0.0, abs_tol=0.0)


@pytest.mark.parametrize('a, b', eight_decimal_places_examples)
def test_eight_decimal_places(a, b, isclose_function):
    assert isclose_function(a, b, rel_tol=1e-8)
    assert not isclose_function(a, b, rel_tol=1e-9)


@pytest.mark.parametrize('a, b', near_zero_examples)
def test_near_zero(a, b, isclose_function):
    # these should not be close to any rel_tol
    assert not isclose_function(a, b, rel_tol=0.9)
    # these should be close to abs_tol=1e-8
    assert isclose_function(a, b, abs_tol=1e-8)


def test_identical_infinite(isclose_function):
    # these are close regardless of tolerance -- i.e. they are equal
    assert isclose_function(INF, INF)
    assert isclose_function(INF, INF, abs_tol=0.0)
    assert isclose_function(NINF, NINF)
    assert isclose_function(NINF, NINF, abs_tol=0.0)


@pytest.mark.parametrize('a, b', not_close_examples)
def test_inf_ninf_nan(a, b, isclose_function):
    # use largest reasonable tolerance
    assert not isclose_function(a, b, abs_tol=0.999999999999999)


@pytest.mark.parametrize('a, b', zero_tolerance_close_examples)
def test_zero_tolerance(a, b, isclose_function):
    assert isclose_function(a, b, rel_tol=0.0)


@pytest.mark.parametrize('a, b', zero_tolerance_not_close_examples)
def test_zero_tolerance_not_close(a, b, isclose_function):
    assert not isclose_function(a, b, rel_tol=0.0)


@pytest.mark.parametrize('a, b', [(9, 10), (10, 9)])
def test_assymetry(a, b, isclose_function):
    # test the assymetry example from PEP 485
    assert isclose_function(a, b, rel_tol=0.1)


@pytest.mark.parametrize('a, b', integer_examples)
def test_integers(a, b, isclose_function):
    assert isclose_function(a, b, rel_tol=1e-8)
    assert not isclose_function(a, b, rel_tol=1e-9)


@pytest.mark.parametrize('a, b', decimal_examples)
def test_decimals(a, b, isclose_function):
    if isclose_function is _isclose:
        pytest.xfail("Python implementation of isclose doesn't work with Decimal")
    assert isclose_function(a, b, rel_tol=1e-8)
    assert not isclose_function(a, b, rel_tol=1e-9)


@pytest.mark.parametrize('a, b', fraction_examples)
def test_fractions(a, b, isclose_function):
    assert isclose_function(a, b, rel_tol=1e-8)
    assert not isclose_function(a, b, rel_tol=1e-9)
