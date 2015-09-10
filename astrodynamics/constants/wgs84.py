# coding: utf-8
from __future__ import absolute_import, division, print_function

from astropy import units as u

__all__ = (
    'WGS84_EQUATORIAL_RADIUS',
    'WGS84_FLATTENING',
    'WGS84_MU',
    'WGS84_ANGULAR_VELOCITY',
)

WGS84_EQUATORIAL_RADIUS = 6378137 * u.m
WGS84_FLATTENING = 1 / 298.257223563 * u.one
WGS84_MU = 3.986004418e14 * u.m ** 3 / u.s ** 2
WGS84_ANGULAR_VELOCITY = 7.292115e-5 * u.rad / u.s
