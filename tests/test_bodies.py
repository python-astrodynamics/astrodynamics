# coding: utf-8
from __future__ import absolute_import, division, print_function

import pytest
from astropy import units as u

from astrodynamics.bodies import (
    CelestialBody, Ellipsoid, ReferenceEllipsoid, wgs84)
from astrodynamics.constants import (
    EARTH_MASS, GEOCENTRIC_GRAVITATIONAL_CONSTANT, WGS84_EQUATORIAL_RADIUS,
    WGS84_FLATTENING)
from astrodynamics.utils import qisclose


def test_ellipsoid():
    """Test Ellipsoid initialiser and verify computed attributes."""
    wgs84_polar_radius = 6356752.314245 * u.m

    wgs84_ellipsoid1 = Ellipsoid(a=WGS84_EQUATORIAL_RADIUS, f=WGS84_FLATTENING)
    wgs84_ellipsoid2 = Ellipsoid(a=WGS84_EQUATORIAL_RADIUS, b=wgs84_polar_radius)

    assert qisclose(wgs84_ellipsoid1.b, wgs84_ellipsoid2.b)
    assert qisclose(wgs84_ellipsoid1.f, wgs84_ellipsoid2.f)

    with pytest.raises(TypeError):
        Ellipsoid(a=WGS84_EQUATORIAL_RADIUS)

    with pytest.raises(TypeError):
        Ellipsoid(a=WGS84_EQUATORIAL_RADIUS, b=wgs84_polar_radius,
                  f=WGS84_FLATTENING)


def test_ellipsoid_repr():
    a = Ellipsoid(a=2 * u.m, b=1 * u.m)
    assert repr(a) == 'Ellipsoid(a=<Quantity 2.0 m>, f=<Quantity 0.5>)'


def test_reference_ellipsoid_repr():
    a = ReferenceEllipsoid(
        a=1 * u.m, f=0, mu=1 * u.m ** 3 / u.s ** 2, spin=1 * u.rad / u.s)
    s = ('ReferenceEllipsoid(a=<Quantity 1.0 m>, f=<Quantity 0.0>, '
         'mu=<Quantity 1.0 m3 / s2>, spin=<Quantity 1.0 rad / s>)')
    assert repr(a) == s


def test_celestial_body():
    "Test CelestialBody initialiser and verify computed attributes"
    a = CelestialBody(name='earth', ellipsoid=wgs84, mu=wgs84.mu, naif_id=399)
    b = CelestialBody.from_reference_ellipsoid(name='earth', ellipsoid=wgs84,
                                               naif_id=399)
    assert a.mu == b.mu == wgs84.mu

    ellipsoid = Ellipsoid(a=1 * u.m, b=1 * u.m)
    c = CelestialBody(name='earth', ellipsoid=ellipsoid,
                      mu=GEOCENTRIC_GRAVITATIONAL_CONSTANT, naif_id=399)
    assert qisclose(c.mass, EARTH_MASS)


def test_celestial_body_repr():
    ellipsoid = Ellipsoid(a=1 * u.m, b=1 * u.m)
    d = CelestialBody(name='d', ellipsoid=ellipsoid, mu=1 * u.m ** 3 / u.s ** 2,
                      naif_id=1)

    s = ("CelestialBody(name='d', ellipsoid=Ellipsoid(a=<Quantity 1.0 m>, "
         "f=<Quantity 0.0>), mu=<Quantity 1.0 m3 / s2>, naif_id=1)")
    assert repr(d) == s
