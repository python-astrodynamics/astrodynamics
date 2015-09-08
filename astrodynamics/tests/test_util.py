import pytest
from astropy import units as u

from astrodynamics.util import verify_unit


def test_verify_unit():
    # Implicit dimensionless values are allowed
    verify_unit(0, u.one)

    # Test failure mode
    with pytest.raises(ValueError):
        verify_unit(0, u.meter)

    # Quantity should be passed back if unit matches
    assert verify_unit(1 * u.meter, u.meter) == 1 * u.meter
