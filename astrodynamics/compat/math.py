# coding: utf-8
from __future__ import absolute_import, division, print_function

import math


def _isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    """
    Returns True if `a` is close in value to `b`. False otherwise

    :param a: one of the values to be tested

    :param b: the other value to be tested

    :param rel_tol=1e-9: The relative tolerance -- the amount of error
                         allowed, relative to the absolute value of the
                         larger input values.

    :param abs_tol=0.0: The minimum absolute tolerance level -- useful
                        for comparisons to zero.

    NOTES:

    -inf, inf and NaN behave similarly to the IEEE 754 Standard. That
    is, NaN is not close to anything, even itself. inf and -inf are
    only close to themselves.

    The function can be used with any type that supports comparison,
    subtraction and multiplication, including Decimal, Fraction, and
    Complex

    Complex values are compared based on their absolute value.

    See PEP-0485 for a detailed description.

    This is the result of much discussion on the python-ideas list
    in January, 2015:

       https://mail.python.org/pipermail/python-ideas/2015-January/030947.html

       https://mail.python.org/pipermail/python-ideas/2015-January/031124.html

       https://mail.python.org/pipermail/python-ideas/2015-January/031313.html

    Copyright: Christopher H. Barker
    License: Apache License 2.0 http://opensource.org/licenses/apache2.0.php
    """

    if rel_tol < 0.0 or abs_tol < 0.0:
        raise ValueError('tolerances must be non-negative')

    if a == b:
        # short circuit exact equality -- needed to catch two infinities of
        # the same sign. And perhaps speeds things up a bit sometimes.
        return True

    # This catches the case of two infinities of opposite sign, or
    # one infinity and one finite number. Two infinities of opposite
    # sign would otherwise have an infinite relative tolerance.
    # Two infinities of the same sign are caught by the equality check
    # above.
    if math.isinf(a) or math.isinf(b):
        return False

    diff = abs(b - a)

    return (((diff <= abs(rel_tol * b)) or
             (diff <= abs(rel_tol * a))) or
            (diff <= abs_tol))

try:
    from math import isclose
except ImportError:
    isclose = _isclose
