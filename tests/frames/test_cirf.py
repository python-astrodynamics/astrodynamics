# coding: utf-8
from __future__ import absolute_import, division, print_function

import astropy.units as u
import numpy as np
import pytest
from astropy.time import Time
from numpy.linalg import norm

from astrodynamics.frames import CIRF_CONVENTIONS_2010_SIMPLE_EOP


@pytest.mark.skip(
    reason='CIRF not fully implemented yet, requires IERS download each time.')
def test_rotation_rate():
    t_min = Time('2009-04-07 02:56:33.816', scale='utc')
    t_max = Time('2043-12-16 10:47:20', scale='utc')

    t1 = CIRF_CONVENTIONS_2010_SIMPLE_EOP.transform_provider.get_transform(t_min)
    t2 = CIRF_CONVENTIONS_2010_SIMPLE_EOP.transform_provider.get_transform(t_max)

    rad_s = u.rad / u.s

    min_rate = norm(t_min.angular_velocity)
    max_rate = norm(t_max.angular_velocity)

    assert np.isclose(min_rate, 1.1e-15 * rad_s, rtol=0, atol=1.0e-16 * rad_s)
    assert np.isclose(max_rate, 8.6e-12 * rad_s, rtol=0, atol=1.0e-13 * rad_s)
