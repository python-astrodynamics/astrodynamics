# coding: utf-8
# These tests are taken from astropy, as with the astrodynamics.constant.Constant
# class. It retains the original license (see licenses/ASTROPY_LICENSE.txt)
from __future__ import absolute_import, division, print_function

import copy

import astropy.units as u
from astropy.units import Quantity

import astrodynamics.constants as const
from astrodynamics.constants import J2, Constant


def test_units():
    """Confirm that none of the constants defined in astrodynamics have invalid
    units.
    """
    for key, val in vars(const).items():
        if isinstance(val, Constant):
            # Getting the unit forces the unit parser to run.
            assert not isinstance(val.unit, u.UnrecognizedUnit)


def test_copy():
    copied = copy.deepcopy(J2)
    assert copied == J2

    copied = copy.copy(J2)
    assert copied == J2


def test_view():
    """Check that Constant and Quantity views can be taken."""
    x = J2
    x2 = x.view(Constant)
    assert x2 == x
    assert x2.value == x.value
    # make sure it has the necessary attributes and they're not blank
    assert x2.uncertainty
    assert x2.name == x.name
    assert x2.reference == x.reference
    assert x2.unit == x.unit

    q1 = x.view(Quantity)
    assert q1 == x
    assert q1.value == x.value
    assert type(q1) is Quantity
    assert not hasattr(q1, 'reference')

    q2 = Quantity(x)
    assert q2 == x
    assert q2.value == x.value
    assert type(q2) is Quantity
    assert not hasattr(q2, 'reference')

    x3 = Quantity(x, subok=True)
    assert x3 == x
    assert x3.value == x.value
    # make sure it has the necessary attributes and they're not blank
    assert x3.uncertainty
    assert x3.name == x.name
    assert x3.reference == x.reference
    assert x3.unit == x.unit

    x4 = Quantity(x, subok=True, copy=False)
    assert x4 is x


def test_repr():
    a = Constant('the name', value=1, unit='m2', uncertainty=0.1, reference='me')
    s = ("Constant(name='the name', value=1, unit='m2', uncertainty=0.1, "
         "reference='me')")
    assert repr(a) == s
