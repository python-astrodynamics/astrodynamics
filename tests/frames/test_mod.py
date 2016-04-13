# coding: utf-8
from __future__ import absolute_import, division, print_function

import astropy.units as u
import numpy as np
from astropy.time import Time

from astrodynamics.frames import GCRF, MOD_CONVENTIONS_2010_SIMPLE_EOP
from astrodynamics.rotation import Rotation

from tests.check import check_rotation, check_vector


def test_erfa_bp06():
    t = Time('2004-02-14', scale='utc')
    from astropy._erfa import bp06
    rb, rp, rbp = bp06(t.jd1, t.jd2)
    m1 = rbp
    m2 = GCRF.get_transform_to(MOD_CONVENTIONS_2010_SIMPLE_EOP, t).rotation.matrix
    assert np.allclose(m1, m2, rtol=0, atol=1.1e-12)
