# coding: utf-8
from __future__ import absolute_import, division, print_function

from astropy import units as u

from astrodynamics.bodies import wgs84, CelestialBody, Ellipsoid
from astrodynamics.constants import EARTH_MASS, GEOCENTRIC_GRAVITATIONAL_CONSTANT
from astrodynamics.util import isclose


def test_wgs84_ellipsoid():
    x = wgs84.b
    y = 6356752.314245 * u.m
    assert isclose(x.si.value, y.si.value)


def test_celestial_body():
    a = CelestialBody(name='earth', ellipsoid=wgs84, mu=wgs84.mu)
    b = CelestialBody.from_reference_ellipsoid(name='earth', ellipsoid=wgs84)
    assert a.mu == b.mu == wgs84.mu

    ellipsoid = Ellipsoid(a=1 * u.m, b=1 * u.m)
    c = CelestialBody(name='earth', ellipsoid=ellipsoid,
                      mu=GEOCENTRIC_GRAVITATIONAL_CONSTANT)
    assert isclose(c.mass, EARTH_MASS)
