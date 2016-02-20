# coding: utf-8
from __future__ import absolute_import, division, print_function

import numpy as np
import pytest

import astrodynamics.lowlevel.ephemerides as ephemerides


class MockSegment(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute_and_differentiate(self, tdb, tdb2):
        r = np.empty(3)
        v = np.empty(3)
        if self.a == 3 and self.b == 399:
            r.fill(1.0)
            v.fill(1.0)
        elif self.a == 3 and self.b == 301:
            r.fill(2.0)
            v.fill(2.0)
        elif self.a == 0 and self.b == 3:
            r.fill(3.0)
            v.fill(3.0)
        elif self.a == 0 and self.b == 4:
            r.fill(4.0)
            v.fill(4.0)
        return r, v


class MockKernel(object):
    def __init__(self):
        self.pairs = [
            (0, 3),
            (0, 4),
            (3, 301),
            (3, 399),
        ]

    def __getitem__(self, ind):
        return MockSegment(ind[0], ind[1])


@pytest.fixture
def ephemeris():
    eph = ephemerides.JPLEphemeris()
    eph._kernel = MockKernel()
    eph.generate_paths()
    return eph


def test_pair_failure(ephemeris):
    with pytest.raises(ValueError):
        ephemeris.rv(0, 5, 0)


def test_ephemeris(ephemeris):
    r, v = ephemeris.rv(0, 3, 0)
    assert np.all(r == 3.0)
    assert np.all(v == 3.0)
    r, v = ephemeris.rv(3, 0, 0)
    assert np.all(r == -3.0)
    assert np.all(v == -3.0)
    r, v = ephemeris.rv(0, 4, 0)
    assert np.all(r == 4.0)
    assert np.all(v == 4.0)
    r, v = ephemeris.rv(4, 0, 0)
    assert np.all(r == -4.0)
    assert np.all(v == -4.0)
    r, v = ephemeris.rv(3, 301, 0)
    assert np.all(r == 2.0)
    assert np.all(v == 2.0)
    r, v = ephemeris.rv(301, 3, 0)
    assert np.all(r == -2.0)
    assert np.all(v == -2.0)
    r, v = ephemeris.rv(3, 399, 0)
    assert np.all(r == 1.0)
    assert np.all(v == 1.0)
    r, v = ephemeris.rv(399, 3, 0)
    assert np.all(r == -1.0)
    assert np.all(v == -1.0)
    r, v = ephemeris.rv(0, 301, 0)
    assert np.all(r == 5.0)
    assert np.all(v == 5.0)
    r, v = ephemeris.rv(301, 0, 0)
    assert np.all(r == -5.0)
    assert np.all(v == -5.0)
    r, v = ephemeris.rv(0, 399, 0)
    assert np.all(r == 4.0)
    assert np.all(v == 4.0)
    r, v = ephemeris.rv(399, 0, 0)
    assert np.all(r == -4.0)
    assert np.all(v == -4.0)
    r, v = ephemeris.rv(3, 4, 0)
    assert np.all(r == 1.0)
    assert np.all(v == 1.0)
    r, v = ephemeris.rv(4, 3, 0)
    assert np.all(r == -1.0)
    assert np.all(v == -1.0)
    r, v = ephemeris.rv(301, 4, 0)
    assert np.all(r == -1.0)
    assert np.all(v == -1.0)
    r, v = ephemeris.rv(4, 301, 0)
    assert np.all(r == 1.0)
    assert np.all(v == 1.0)
    r, v = ephemeris.rv(4, 301, 0, 0)
    assert np.all(r == 1.0)
    assert np.all(v == 1.0)
