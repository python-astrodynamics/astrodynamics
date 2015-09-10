# coding: utf-8
from __future__ import absolute_import, division, print_function

from astropy import units as u

from astrodynamics.bodies.ellipsoid import wgs84
from astrodynamics.util import isclose


def test_wgs84_ellipsoid():
    x = wgs84.b
    y = 6356752.314245 * u.m
    assert isclose(x.si.value, y.si.value)
