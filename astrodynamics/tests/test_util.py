# coding: utf-8
from __future__ import absolute_import, division, print_function

import pytest
from astropy import units as u

from astrodynamics.util import verify_unit


def test_verify_unit():
    # Implicit dimensionless values are allowed, test that Quantity is returned.
    assert verify_unit(0, u.one) == 0 * u.one
    assert verify_unit(0, '') == 0 * u.one

    # Test failure mode
    with pytest.raises(ValueError):
        verify_unit(0, u.meter)
    with pytest.raises(ValueError):
        verify_unit(0, 'm')

    # Quantity should be passed back if unit matches
    assert verify_unit(1 * u.meter, u.meter) == 1 * u.meter
    assert verify_unit(1 * u.meter, 'm') == 1 * u.meter
