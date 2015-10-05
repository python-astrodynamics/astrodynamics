# coding: utf-8
from __future__ import absolute_import, division, print_function

import pytest
from astropy import units as u

from astrodynamics.util import format_size, verify_unit


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


size_tests = (
    300, 3000, 3000000, 3000000000, 3000000000000, (300, True), (3000, True),
    (3000000, True), (300, False, True), (3000, False, True),
    (3000000, False, True), (1024, False, True), (10 ** 26 * 30, False, True),
    (10 ** 26 * 30, True), 10 ** 26 * 30, (3141592, False, False, '%.2f'),
    (3000, False, True, '%.3f'), (3000000000, False, True, '%.0f'),
    (10 ** 26 * 30, True, False, '%.3f'),
)

size_results = (
    '300 Bytes', '3.0 kB', '3.0 MB', '3.0 GB', '3.0 TB', '300 Bytes', '2.9 KiB',
    '2.9 MiB', '300B', '2.9K', '2.9M', '1.0K', '2481.5Y', '2481.5 YiB',
    '3000.0 YB', '3.14 MB', '2.930K', '3G', '2481.542 YiB'
)


@pytest.mark.parametrize('args, string', zip(size_tests, size_results))
def test_format_size(args, string):
    if not isinstance(args, tuple):
        args = args,
    assert format_size(*args) == string
