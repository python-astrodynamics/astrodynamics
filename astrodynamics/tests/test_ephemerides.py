# coding: utf-8
from __future__ import absolute_import, division, print_function

import astrodynamics.ephemerides as ephemerides

EARTH = '399'
MOON = '301'
EARTH_BARYCENTER = '3'
MARS_BARYCENTER = '4'
SOLAR_SYSTEM_BARYCENTER = '0'

def test_ssb_to_earth_bc():
    opath, tpath = ephemerides.paths(
        SOLAR_SYSTEM_BARYCENTER,
        EARTH_BARYCENTER,
    )
    assert opath == [0, 3]
    assert not tpath

def test_earth_bc_to_moon():
    opath, tpath = ephemerides.paths(
        EARTH_BARYCENTER,
        MOON,
    )
    assert opath == [3, 301]
    assert not tpath

def test_earth_to_moon():
    opath, tpath = ephemerides.paths(
        EARTH,
        MOON,
    )
    assert opath == [3, 399]
    assert tpath == [3, 301]

def test_earth_bc_to_mars_bc():
    opath, tpath = ephemerides.paths(
        EARTH_BARYCENTER,
        MARS_BARYCENTER,
    )
    assert opath == [0, 3]
    assert tpath == [0, 4]

def test_earth_to_mars_bc():
    opath, tpath = ephemerides.paths(
        EARTH,
        MARS_BARYCENTER,
    )
    assert opath == [0, 3, 399]
    assert tpath == [0, 4]

def test_ssb_to_moon():
    opath, tpath = ephemerides.paths(
        SOLAR_SYSTEM_BARYCENTER,
        MOON,
    )
    assert opath == [0, 3, 301]
    assert not tpath
