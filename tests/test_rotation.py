# coding: utf-8
from __future__ import absolute_import, division, print_function

from math import pi, sqrt

import astropy.units as u
import itertools
import numpy as np
import pytest
from astrodynamics.compat.math import isclose
from astrodynamics.rotation import Rotation, RotationOrder

from .check import check_angle, check_rotation, check_vector

I = np.array([1, 0, 0])
J = np.array([0, 1, 0])
K = np.array([0, 0, 1])


def test_axis_angle_vector_convention():
    r = Rotation.from_axis_angle(
        np.array([10, 10, 10]), 2 * pi / 3 * u.rad, convention='vector')
    check_vector(r.apply_to(I), J)
    check_vector(r.apply_to(J), K)
    check_vector(r.apply_to(K), I)

    s = 1 / sqrt(3)
    check_vector(r.get_axis(convention='vector'), np.array([s, s, s]))
    check_vector(r.get_axis(convention='frame'), np.array([-s, -s, -s]))

    check_angle(r.angle, 2 * pi / 3 * u.rad)

    with pytest.raises(ValueError):
        Rotation.from_axis_angle(
            np.array([0, 0, 0]), 2 * pi / 3, convention='vector')

    r = Rotation.from_axis_angle(K, 1.5 * pi * u.rad, convention='vector')
    check_vector(r.get_axis(convention='vector'), -K)
    check_vector(r.get_axis(convention='frame'), K)
    check_angle(r.angle, 0.5 * pi * u.rad)

    r = Rotation.from_axis_angle(J, pi * u.rad, convention='vector')
    check_vector(r.get_axis(convention='vector'), J)
    check_vector(r.get_axis(convention='frame'), -J)
    check_angle(r.angle, pi * u.rad)


def test_axis_angle_frame_convention():
    r = Rotation.from_axis_angle(
        np.array([10, 10, 10]), 2 * pi / 3 * u.rad, convention='frame')
    check_vector(r.apply_to(I), K)
    check_vector(r.apply_to(J), I)
    check_vector(r.apply_to(K), J)

    s = 1 / sqrt(3)
    check_vector(r.get_axis(convention='frame'), np.array([s, s, s]))
    check_vector(r.get_axis(convention='vector'), np.array([-s, -s, -s]))
    check_angle(r.angle, 2 * pi / 3 * u.rad)

    with pytest.raises(ValueError):
        Rotation.from_axis_angle(
            np.array([0, 0, 0]), 2 * pi / 3 * u.rad, convention='frame')

    r = Rotation.from_axis_angle(K, 1.5 * pi * u.rad, convention='frame')
    check_vector(r.get_axis(convention='frame'), -K)
    check_vector(r.get_axis(convention='vector'), K)
    check_angle(r.angle, 0.5 * pi * u.rad)

    r = Rotation.from_axis_angle(J, pi * u.rad, convention='frame')
    check_vector(r.get_axis(convention='frame'), J)
    check_vector(r.get_axis(convention='vector'), -J)
    check_angle(r.angle, pi * u.rad)


@pytest.mark.parametrize('convention', ['vector', 'frame'])
def test_invert(convention):
    r = Rotation(0.001, 0.36, 0.48, 0.8)
    inv = ~r
    check_rotation(r.compose(inv, convention=convention), Rotation(1, 0, 0, 0))
    check_rotation(inv.compose(r, convention=convention), Rotation(1, 0, 0, 0))
    check_angle(r.angle, inv.angle)
    x = np.dot(r.get_axis(convention=convention), inv.get_axis(convention=convention))
    assert isclose(-1, x, rel_tol=0, abs_tol=1e-15)


@pytest.mark.parametrize('matrix, exception', [
    (np.array([
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0]
    ]), TypeError),
    (np.array([
        [0.445888, 0.797184, -0.407040],
        [0.821760, -0.184320, 0.539200],
        [-0.354816, 0.574912, 0.737280]
    ]), ValueError)
])
def test_matrix_error(matrix, exception):
    with pytest.raises(exception):
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
    assert isclose(r.q0, q0, rel_tol=0, abs_tol=1e-15)
    assert isclose(r.q1, q1, rel_tol=0, abs_tol=1e-15)
    assert isclose(r.q2, q2, rel_tol=0, abs_tol=1e-15)
    assert isclose(r.q3, q3, rel_tol=0, abs_tol=1e-15)


def test_matrix_other():
    m1 = np.array([
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0],
    ])
    r = Rotation.from_matrix(m1)
    check_vector(r.apply_to(I), K)
    check_vector(r.apply_to(J), I)
    check_vector(r.apply_to(K), J)

    m2 = np.array([
        [0.83203, -0.55012, -0.07139],
        [0.48293, 0.78164, -0.39474],
        [0.27296, 0.29396, 0.91602]
    ])
    r = Rotation.from_matrix(m2)
    m3 = r.matrix
    assert np.allclose(m2, m3, rtol=0, atol=6e-6)

    for i in range(3):
        for j in range(3):
            m3tm3 = m3[i][0] * m3[j][0] + m3[i][1] * m3[j][1] + m3[i][2] * m3[j][2]
            if i == j:
                assert isclose(m3tm3 - 1, 0, rel_tol=0, abs_tol=1e-14)
            else:
                assert isclose(m3tm3, 0, rel_tol=0, abs_tol=1e-15)


@pytest.mark.parametrize('convention', ['vector', 'frame'])
@pytest.mark.parametrize('order', [
    RotationOrder.XZX,
    RotationOrder.YXY,
    RotationOrder.ZYZ,
    RotationOrder.XYX,
    RotationOrder.YZY,
    RotationOrder.ZXZ,
])
def test_euler_angles_proper_euler(convention, order):
    it = itertools.product(
        np.arange(0.1, 6.2, 0.3) * u.rad,
        np.arange(0.05, 3.1, 0.3) * u.rad,
        np.arange(0.1, 6.2, 0.3) * u.rad,
    )
    for alpha1, alpha2, alpha3 in it:
        r = Rotation.from_euler_angles(
            order, alpha1, alpha2, alpha3,
            convention=convention)

        angles = r.get_angles(order, convention=convention)
        check_angle(angles[0], alpha1)
        check_angle(angles[1], alpha2)
        check_angle(angles[2], alpha3)


@pytest.mark.parametrize('convention', ['vector', 'frame'])
@pytest.mark.parametrize('order', [
    RotationOrder.XYZ,
    RotationOrder.XZY,
    RotationOrder.YXZ,
    RotationOrder.YZX,
    RotationOrder.ZXY,
    RotationOrder.ZYX,
])
def test_euler_angles_cardan(convention, order):
    it = itertools.product(
        np.arange(0.1, 6.2, 0.3) * u.rad,
        np.arange(-1.55, 1.55, 0.3) * u.rad,
        np.arange(0.1, 6.2, 0.3) * u.rad,
    )
    for alpha1, alpha2, alpha3 in it:
        r = Rotation.from_euler_angles(
            order, alpha1, alpha2, alpha3,
            convention=convention)

        angles = r.get_angles(order, convention=convention)
        check_angle(angles[0], alpha1)
        check_angle(angles[1], alpha2)
        check_angle(angles[2], alpha3)


@pytest.mark.parametrize('convention', ['vector', 'frame'])
def test_compose(convention):
    r1 = Rotation.from_axis_angle(
        np.array([2, -3, 5]), 1.7 * u.rad, convention=convention)

    r2 = Rotation.from_axis_angle(
        np.array([-1, 3, 2]), 0.3 * u.rad, convention=convention)

    r3 = r2.compose(r1, convention=convention)

    float_range = np.arange(-0.9, 0.9, 0.2)

    it = itertools.product(float_range, float_range, float_range)

    for x, y, z in it:
        w = np.array([x, y, z])

        if convention == 'vector':
            v1 = r2.apply_to(r1.apply_to(w))
            v2 = r3.apply_to(w)
        elif convention == 'frame':
            v1 = r1.apply_to(r2.apply_to(w))
            v2 = r3.apply_to(w)

        check_vector(v1, v2)
