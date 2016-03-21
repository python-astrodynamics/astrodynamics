# coding: utf-8
from __future__ import absolute_import, division, print_function

import numpy as np
import pytest
from astrodynamics.compat.math import isclose
from astrodynamics.lowlevel.rotation import Rotation


@pytest.mark.parametrize('matrix', [
    np.array([
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0]
    ]),
    np.array([
        [0.445888, 0.797184, -0.407040],
        [0.821760, -0.184320, 0.539200],
        [-0.354816, 0.574912, 0.737280]
    ])
])
def test_matrix_error(matrix):
    with pytest.raises(ValueError):
        Rotation.from_matrix(matrix)


@pytest.mark.parametrize('matrix, q0, q1, q2, q3', [
    (
        np.array([
            [0.445888, 0.797184, -0.407040],
            [-0.354816, 0.574912, 0.737280],
            [0.821760, -0.184320, 0.539200]
        ]),
        0.8, 0.288, 0.384, 0.36
    ),
    (
        np.array([
            [0.539200, 0.737280, 0.407040],
            [0.184320, -0.574912, 0.797184],
            [0.821760, -0.354816, -0.445888]
        ]),
        0.36, 0.8, 0.288, 0.384
    ),
    (
        np.array([
            [-0.445888, 0.797184, -0.407040],
            [0.354816, 0.574912, 0.737280],
            [0.821760, 0.184320, -0.539200]
        ]),
        0.384, 0.36, 0.8, 0.288
    ),
    (
        np.array([
            [-0.539200, 0.737280, 0.407040],
            [-0.184320, -0.574912, 0.797184],
            [0.821760, 0.354816, 0.445888]
        ]),
        0.288, 0.384, 0.36, 0.8
    )
])
def test_matrix(matrix, q0, q1, q2, q3):
    r = Rotation.from_matrix(matrix)
    assert isclose(r.q0, q0)
    assert isclose(r.q1, q1)
    assert isclose(r.q2, q2)
    assert isclose(r.q3, q3)


def test_apply_to():
    r1 = Rotation.from_axis_angle(np.array([2, -3, 5]), 1.7)
    r2 = Rotation.from_axis_angle(np.array([-1, 3, 2]), 0.3)
    r3 = r2.apply_to(r1)

    for x in np.arange(-0.9, 0.9, 0.2):
        for y in np.arange(-0.9, 0.9, 0.2):
            for z in np.arange(-0.9, 0.9, 0.2):
                u = np.array([x, y, z])

                v1 = r2.apply_to(r1.apply_to(u))
                v2 = r3.apply_to(u)

                assert isclose(v1[0], v2[0])
                assert isclose(v1[1], v2[1])
                assert isclose(v1[2], v2[2])
