# coding: utf-8
from __future__ import absolute_import, division, print_function

import astropy.units as u
import numpy as np
from astropy.time import Time
from astropy._erfa import bp00

from astrodynamics.frames import GCRF, EME2000
from astrodynamics.rotation import Rotation

from tests.check import check_rotation, check_vector


def test_aas_reference_leo():
    """This reference test has been extracted from the following paper:
    Implementation Issues Surrounding the New IAU Reference Systems for
    Astrodynamics, by David A. Vallado, John H. Seago, P. Kenneth Seidelmann

    http://www.centerforspace.com/downloads/files/pubs/AAS-06-134.pdf
    """
    t0 = Time('2004-04-06 07:51:28.386009', scale='utc')
    t = GCRF.get_transform_to(EME2000, t0)

    p_gcrf_iau_2000_a = np.array([5102508.9579, 6123011.4038, 6378136.9252]) * u.m
    v_gcrf_iau_2000_a = np.array([-4743.220156, 790.536497, 5533.755728]) * u.m / u.s
    p_eme2000_eq_a = np.array([5102509.0383, 6123011.9758, 6378136.3118]) * u.m
    v_eme2000_eq_a = np.array([-4743.219766, 790.536344, 5533.756084]) * u.m / u.s

    p, v, _ = t.transform(p_gcrf_iau_2000_a, v_gcrf_iau_2000_a)

    check_vector(p_eme2000_eq_a, p, rtol=0, atol=1.1e-4 * u.m)
    check_vector(v_eme2000_eq_a, v, rtol=0, atol=2.6e-7 * u.m / u.s)

    p_gcrf_iau_2000_b = np.array([5102508.9579, 6123011.4012, 6378136.9277]) * u.m
    v_gcrf_iau_2000_b = np.array([-4743.220156, 790.536495, 5533.755729]) * u.m / u.s

    p_eme2000_eq_b = np.array([5102509.0383, 6123011.9733, 6378136.3142]) * u.m
    v_eme2000_eq_b = np.array([-4743.219766, 790.536342, 5533.756085]) * u.m / u.s

    p, v, _ = t.transform(p_gcrf_iau_2000_b, v_gcrf_iau_2000_b)

    check_vector(p_eme2000_eq_b, p, rtol=0, atol=7.4e-5 * u.m)
    check_vector(v_eme2000_eq_b, v, rtol=0, atol=2.6e-7 * u.m / u.s)


def test_aas_reference_geo():
    """This reference test has been extracted from the following paper:
    Implementation Issues Surrounding the New IAU Reference Systems for
    Astrodynamics, by David A. Vallado, John H. Seago, P. Kenneth Seidelmann

    http://www.centerforspace.com/downloads/files/pubs/AAS-06-134.pdf
    """
    t0 = Time('2004-06-01', scale='utc')
    t = GCRF.get_transform_to(EME2000, t0)

    p_gcrf_iau_2000_a = np.array([-40588150.3617, -11462167.0397, 27143.1974]) * u.m
    v_gcrf_iau_2000_a = np.array([834.787458, -2958.305691, -1.172993]) * u.m / u.s
    p_eme2000_eq_a = np.array([-40588149.5482, -11462169.9118, 27146.8462]) * u.m
    v_eme2000_eq_a = np.array([834.787667, -2958.305632, -1.172963]) * u.m / u.s

    p, v, _ = t.transform(p_gcrf_iau_2000_a, v_gcrf_iau_2000_a)

    check_vector(p_eme2000_eq_a, p, rtol=0, atol=5.8e-5 * u.m)
    check_vector(v_eme2000_eq_a, v, rtol=0, atol=6.4e-7 * u.m / u.s)

    p_gcrf_iau_2000_b = np.array([-40588150.3617, -11462167.0397, 27143.2125]) * u.m
    v_gcrf_iau_2000_b = np.array([834.787458, -2958.305691, -1.172999]) * u.m / u.s

    p_eme2000_eq_b = np.array([-40588149.5481, -11462169.9118, 27146.8613]) * u.m
    v_eme2000_eq_b = np.array([834.787667, -2958.305632, -1.172968]) * u.m / u.s

    p, v, _ = t.transform(p_gcrf_iau_2000_b, v_gcrf_iau_2000_b)

    check_vector(p_eme2000_eq_b, p, rtol=0, atol=1.1e-4 * u.m)
    check_vector(v_eme2000_eq_b, v, rtol=0, atol=5.5e-7 * u.m / u.s)


def test_erfa_bp00():
    t = Time('2004-02-14', scale='utc')
    rb, rp, rbp = bp00(t.jd1, t.jd2)
    r1 = Rotation.from_matrix(rb)
    r2 = GCRF.get_transform_to(EME2000, t).rotation
    check_rotation(r1, r2, atol=2.5e-16 * u.rad)
