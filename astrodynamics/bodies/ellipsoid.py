# coding: utf-8
from __future__ import absolute_import, division, print_function

from astropy import units as u
from represent import ReprHelperMixin

from ..constants import (
    WGS84_ANGULAR_VELOCITY, WGS84_EQUATORIAL_RADIUS, WGS84_FLATTENING,
    WGS84_MU)
from ..util import read_only_property, verify_unit

__all__ = (
    'Ellipsoid',
    'ReferenceEllipsoid',
    'wgs84',
)


class Ellipsoid(ReprHelperMixin, object):
    """Ellipsoid

    Parameters:
        a: Semi-major axis (equatorial radius) [m]
        f: Flattening [-]
    """
    def __init__(self, a, f):
        self._a = verify_unit(a, u.m)
        self._b = verify_unit(a * (1 - f), u.m)
        self._f = verify_unit(f, u.one)

    a = read_only_property('_a', 'Semi-major axis')
    b = read_only_property('_b', 'Semi-minor axis')
    f = read_only_property('_f', 'Flattening')

    def _repr_helper_(self, r):
        r.keyword_from_attr('a')
        r.keyword_from_attr('b')
        r.keyword_from_attr('f')


class ReferenceEllipsoid(Ellipsoid):
    """ReferenceEllipsoid

    Parameters:
        a: Semi-major axis (equatorial radius) [m]
        f: Flattening [-]
        mu: Standard gravitational parameter [m\ :sup:`3`\ ·s\ :sup:`-2`]
        spin: Spin rate [rad/s]
    """
    def __init__(self, a, f, mu, spin):
        super(ReferenceEllipsoid, self).__init__(a=a, f=f)
        self._mu = verify_unit(mu, u.m ** 3 / u.s ** 2)
        self._spin = verify_unit(spin, u.rad / u.s)

    mu = read_only_property('_mu', 'Standard gravitational parameter')
    spin = read_only_property('_spin', 'Angular velocity')

    def _repr_helper_(self, r):
        super(ReferenceEllipsoid, self)._repr_helper_(r)
        r.keyword_from_attr('mu')
        r.keyword_from_attr('spin')

wgs84 = ReferenceEllipsoid(
    a=WGS84_EQUATORIAL_RADIUS,
    f=WGS84_FLATTENING,
    mu=WGS84_MU,
    spin=WGS84_ANGULAR_VELOCITY)
