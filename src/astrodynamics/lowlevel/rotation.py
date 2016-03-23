# coding: utf-8
# This file is a port of some functionality from the Rotation class in
# commons-math. It retains the original license (see licenses/COMMONS-MATH.txt)
from __future__ import absolute_import, division, print_function

from enum import Enum, unique
from math import cos, sin, sqrt

import astropy.units as u
import numpy as np
from represent import ReprHelperMixin
from scipy.linalg import sqrtm, inv

from ..utils import read_only_property, singledispatch_method


def check_convention(convention):
    if convention not in ('vector', 'frame'):
        raise TypeError(
            "convention must be 'vector' for vector operator semantics, or "
            "'frame' for frame transform semantics.")


class Rotation(ReprHelperMixin):
    q0 = read_only_property('_q0')
    q1 = read_only_property('_q1')
    q2 = read_only_property('_q2')
    q3 = read_only_property('_q3')

    def __init__(self, q0, q1, q2, q3, normalized=False):
        if not normalized:
            inv = 1 / sqrt(q0 ** 2 + q1 ** 2 + q2 ** 2 + q3 ** 2)
            q0 *= inv
            q1 *= inv
            q2 *= inv
            q3 *= inv

        self._q0 = q0
        self._q1 = q1
        self._q2 = q2
        self._q3 = q3

    @classmethod
    def from_axis_angle(cls, axis, angle, convention='vector'):
        check_convention(convention)

        if axis.shape != (3,):
            raise ValueError('axis should be an array with shape (3,)')

        norm = np.linalg.norm(axis)
        if norm == 0:
            raise ValueError('Zero norm for rotation axis.')

        if isinstance(angle, u.Quantity):
            angle = angle.to(u.rad).value

        half_angle = -0.5 * angle if convention == 'vector' else 0.5
        coeff = sin(half_angle) / norm

        q0 = cos(half_angle)
        q1 = coeff * axis[0]
        q2 = coeff * axis[1]
        q3 = coeff * axis[2]

        return cls(q0, q1, q2, q3, normalized=True)

    @classmethod
    def from_matrix(cls, matrix):
        if matrix.shape != (3, 3):
            raise ValueError('matrix should have shape (3, 3)')

        ort = matrix.dot(inv(sqrtm(matrix.T.dot(matrix))))

        if np.linalg.det(ort) < 0:
            raise ValueError('Not a rotation matrix.')

        return cls(*_quaternion_from_matrix(ort), normalized=True)

    @classmethod
    def from_euler_angles(cls, order, alpha1, alpha2, alpha3, convention='vector'):
        check_convention(convention)

        r1 = Rotation.from_axis_angle(order.a1, alpha1, convention)
        r2 = Rotation.from_axis_angle(order.a2, alpha2, convention)
        r3 = Rotation.from_axis_angle(order.a3, alpha3, convention)

        composed = r1.compose(r2.compose(r3, convention), convention)

        q0 = composed.q0
        q1 = composed.q1
        q2 = composed.q2
        q3 = composed.q3

        return Rotation(q0, q1, q2, q3, normalized=True)

    @singledispatch_method
    def apply_to(self, rotation, convention='vector'):
        check_convention(convention)

        r = rotation
        s = self

        q0 = r.q0 * s.q0 - (r.q1 * s.q1 + r.q2 * s.q2 + r.q3 * s.q3)
        q1 = r.q1 * s.q0 + r.q0 * s.q1 + (r.q2 * s.q3 - r.q3 * s.q2)
        q2 = r.q2 * s.q0 + r.q0 * s.q2 + (r.q3 * s.q1 - r.q1 * s.q3)
        q3 = r.q3 * s.q0 + r.q0 * s.q3 + (r.q1 * s.q2 - r.q2 * s.q1)

        return Rotation(q0, q1, q2, q3, normalized=True)

    @apply_to.register(np.ndarray)
    def _(self, vector):
        x = vector[0]
        y = vector[1]
        z = vector[2]

        r = self.q1 * x + self.q2 * y + self.q3 * z
        s = self

        print([
            2 * (s.q0 * (x * s.q0 - (s.q2 * z - s.q3 * y)) + r * s.q1) - x,
            2 * (s.q0 * (y * s.q0 - (s.q3 * x - s.q1 * z)) + r * s.q2) - y,
            2 * (s.q0 * (z * s.q0 - (s.q1 * y - s.q2 * x)) + r * s.q3) - z
        ])

        return np.array([
            2 * (s.q0 * (x * s.q0 - (s.q2 * z - s.q3 * y)) + r * s.q1) - x,
            2 * (s.q0 * (y * s.q0 - (s.q3 * x - s.q1 * z)) + r * s.q2) - y,
            2 * (s.q0 * (z * s.q0 - (s.q1 * y - s.q2 * x)) + r * s.q3) - z
        ])

    def compose(self, rotation, convention='vector'):
        check_convention(convention)

        a = self
        b = rotation

        if convention == 'frame':
            a, b = b, a

        q0 = b.q0 * a.q0 - (b.q1 * a.q1 + b.q2 * a.q2 + b.q3 * a.q3)
        q1 = b.q1 * a.q0 + b.q0 * a.q1 + (b.q2 * a.q3 - b.q3 * a.q2)
        q2 = b.q2 * a.q0 + b.q0 * a.q2 + (b.q3 * a.q1 - b.q1 * a.q3)
        q3 = b.q3 * a.q0 + b.q0 * a.q3 + (b.q1 * a.q2 - b.q2 * a.q1)

        return Rotation(q0, q1, q2, q3, normalized=True)

    def __inv__(self):
        return Rotation(self.q0, -self.q1, -self.q2, -self.q3, normalized=True)

    def __eq__(self, other):
        if isinstance(other, Rotation):
            return all([
                self.q0 == other.q0,
                self.q1 == other.q1,
                self.q2 == other.q2,
                self.q3 == other.q3,
            ])
        else:
            return NotImplemented

    def _repr_helper_(self, r):
        r.keyword_from_attr('q0')
        r.keyword_from_attr('q1')
        r.keyword_from_attr('q2')
        r.keyword_from_attr('q3')


def _quaternion_from_matrix(ort):
    quat = np.zeros(4)

    # There are different ways to compute the quaternions elements
    # from the matrix. They all involve computing one element from
    # the diagonal of the matrix, and computing the three other ones
    # using a formula involving a division by the first element,
    # which unfortunately can be zero. Since the norm of the
    # quaternion is 1, we know at least one element has an absolute
    # value greater or equal to 0.5, so it is always possible to
    # select the right formula and avoid division by zero and even
    # numerical inaccuracy. Checking the elements in turn and using
    # the first one greater than 0.45 is safe (this leads to a simple
    # test since qi = 0.45 implies 4 qi^2 - 1 = -0.19)
    s = ort[0][0] + ort[1][1] + ort[2][2]
    if s > -0.19:
        # compute q0 and deduce q1, q2 and q3
        quat[0] = 0.5 * sqrt(s + 1)
        inv = 0.25 / quat[0]
        quat[1] = inv * (ort[1][2] - ort[2][1])
        quat[2] = inv * (ort[2][0] - ort[0][2])
        quat[3] = inv * (ort[0][1] - ort[1][0])

        return quat

    s = ort[0][0] - ort[1][1] - ort[2][2]
    if s > -0.19:
        # compute q1 and deduce q0, q2 and q3
        quat[1] = 0.5 * sqrt(s + 1)
        inv = 0.25 / quat[1]
        quat[0] = inv * (ort[1][2] - ort[2][1])
        quat[2] = inv * (ort[0][1] + ort[1][0])
        quat[3] = inv * (ort[0][2] + ort[2][0])

        return quat

    s = ort[1][1] - ort[0][0] - ort[2][2]
    if s > -0.19:
        # compute q2 and deduce q0, q1 and q3
        quat[2] = 0.5 * sqrt(s + 1)
        inv = 0.25 / quat[2]
        quat[0] = inv * (ort[2][0] - ort[0][2])
        quat[1] = inv * (ort[0][1] + ort[1][0])
        quat[3] = inv * (ort[2][1] + ort[1][2])

        return quat

    # compute q3 and deduce q0, q1 and q2
    s = ort[2][2] - ort[0][0] - ort[1][1]
    quat[3] = 0.5 * sqrt(s + 1)
    inv = 0.25 / quat[3]
    quat[0] = inv * (ort[0][1] - ort[1][0])
    quat[1] = inv * (ort[0][2] + ort[2][0])
    quat[2] = inv * (ort[2][1] + ort[1][2])

    return quat


I = [1, 0, 0]
J = [0, 1, 0]
K = [0, 0, 1]


@unique
class RotationOrder(Enum):
    XYZ = (I, J, K)
    XZY = (I, K, J)
    YXZ = (J, I, K)
    YZX = (J, K, I)
    ZXY = (K, I, J)
    ZYX = (K, J, I)
    XYX = (I, J, I)
    XZX = (I, K, I)
    YXY = (J, I, J)
    YZY = (J, K, J)
    ZXZ = (K, I, K)
    ZYZ = (K, J, K)

    def __init__(self, a1, a2, a3):
        self.a1 = np.array(a1)
        self.a2 = np.array(a2)
        self.a3 = np.array(a3)
