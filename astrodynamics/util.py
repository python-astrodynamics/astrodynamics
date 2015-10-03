# coding: utf-8
from __future__ import absolute_import, division, print_function

from astropy import units as u
from astropy.units import Unit, UnitBase

from .compat.math import isclose

__all__ = (
    'qisclose',
    'read_only_property',
    'verify_unit',
)


def read_only_property(name, docstring=None):
    """Return property for accessing attribute with name `name`

    Parameters:
        name: Attribute name
        docstring: Optional docstring for getter.

    Example:
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
        quantity: :py:class:`~astropy.units.Quantity` to be verified. Bare
                  numbers are valid if the unit is dimensionless.
        unit: Equivalent unit, or string parsable by
              :py:class:`astropy.units.Unit`

    Raises:
        ValueError: Units are not equivalent.

    Returns:
        ``quantity`` unchanged. Bare numbers will be converted to a dimensionless
        :py:class:`~astropy.units.Quantity`.

    Example:
        .. code-block:: python

            def __init__(self, a):
                self.a = verify_unit(a, astropy.units.m)

    """
    if not isinstance(unit, UnitBase):
        unit = Unit(unit)

    q = quantity * u.one
    if unit.is_equivalent(q.unit):
        return q
    else:
        raise ValueError(
            "Unit '{}' not equivalent to quantity '{}'.".format(unit, quantity))


def qisclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    """Helper function for using :py:func:`math.isclose` with
    :py:class:`~astropy.units.Quantity` objects.
    """
    return isclose(a.si.value, b.si.value, rel_tol=rel_tol, abs_tol=abs_tol)
