from __future__ import absolute_import, division, print_function

import math

from astropy import units as u

__all__ = (
    'isclose',
    'read_only_property',
    'verify_unit',
)


def read_only_property(name, docstring=None):
    """Return property for accessing attribute with name `name`

    Parameters:
        name: Attribute name
        docstring: Optional docstring for getter.

    Example
    -------

    .. code-block:: python

        class Circle:
            def __init__(self, radius):
                self._radius = radius

            radius = read_only_property('_radius')
    """
    def fget(self):
        return getattr(self, name)

    fget.__doc__ = docstring
    return property(fget)


def verify_unit(quantity, unit):
    """Verify unit of passed quantity and return it.

    Parameters:
        quantity: Quantity to be verified.
        unit: Equivalent unit

    Raises:
        ValueError: Units are not equivalent.

    Returns:
        quantity parameter, unchanged.

    Example:

    .. code-block:: python

        def __init__(self, a):
            self.a = verify_unit(a, astropy.units.m)

    :type quantity: :py:class:`astropy.units.Quantity`
    :type unit: :py:class:`astropy.units.UnitBase`
    """
    if unit.is_equivalent((quantity * u.one).unit):
        return quantity
    else:
        raise ValueError(
            "Unit '{}' not equivalent to quantity '{}'.".format(unit, quantity))


def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
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
    substratcion and multiplication, including Decimal, Fraction, and
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

    if a == b:  # short-circuit exact equality
        return True

    if rel_tol < 0.0 or abs_tol < 0.0:
        raise ValueError('error tolerances must be non-negative')

    # use cmath so it will work with complex ot float
    if math.isinf(abs(a)) or math.isinf(abs(b)):
        # This includes the case of two infinities of opposite sign, or
        # one infinity and one finite number. Two infinities of opposite sign
        # would otherwise have an infinite relative tolerance.
        return False
    diff = abs(b - a)

    return (((diff <= abs(rel_tol * b)) or
             (diff <= abs(rel_tol * a))) or
            (diff <= abs_tol))
