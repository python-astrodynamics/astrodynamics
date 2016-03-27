# coding: utf-8
# This file is a port of some functionality from the Rotation class in
# commons-math. It retains the original license (see licenses/COMMONS-MATH.txt)
from __future__ import absolute_import, division, print_function

from enum import Enum, unique
from math import acos, asin, atan2, cos, pi, sin, sqrt

import astropy.units as u
import numpy as np
from represent import ReprHelperMixin
from scipy.linalg import sqrtm, inv

from ..compat.math import isclose
from ..utils import read_only_property

I = np.array([1, 0, 0])
J = np.array([0, 1, 0])
K = np.array([0, 0, 1])

TWOPI = 2 * pi


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

        half_angle = -0.5 * angle if convention == 'vector' else 0.5 * angle
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

        r1 = Rotation.from_axis_angle(order.axis1, alpha1, convention)
        r2 = Rotation.from_axis_angle(order.axis2, alpha2, convention)
        r3 = Rotation.from_axis_angle(order.axis3, alpha3, convention)

        composed = r1.compose(r2.compose(r3, convention), convention)

        q0 = composed.q0
        q1 = composed.q1
        q2 = composed.q2
        q3 = composed.q3

        return Rotation(q0, q1, q2, q3, normalized=True)

    @property
    def angle(self):
        if self.q0 < -0.1 or self.q0 > 0.1:
            return 2 * asin(sqrt(self.q1 ** 2 + self.q2 ** 2 + self.q3 ** 2))
        elif self.q0 < 0:
            return 2 * acos(-self.q0)
        else:
            return 2 * acos(self.q0)

    def get_axis(self, convention='vector'):
        check_convention(convention)

        squared_sine = self.q1 ** 2 + self.q2 ** 2 + self.q3 ** 2
        if squared_sine == 0:
            return I if convention == 'vector' else -I
        else:
            sign = 1 if convention == 'vector' else -1

            if self.q0 < 0:
                inverse = sign / sqrt(squared_sine)
                return np.array([
                    self.q1 * inverse, self.q2 * inverse, self.q3 * inverse])

            inverse = -sign / sqrt(squared_sine)
            return np.array([
                self.q1 * inverse, self.q2 * inverse, self.q3 * inverse])

    def get_angles(self, order, convention='vector'):
        check_convention(convention)

        tait_bryan_angles = {
            RotationOrder.XYZ,
            RotationOrder.XZY,
            RotationOrder.YXZ,
            RotationOrder.YZX,
            RotationOrder.ZXY,
            RotationOrder.ZYX,
        }

        a1y_sign = 1
        a1x_sign = 1
        a2_sign = 1
        a3y_sign = 1
        a3x_sign = 1

        if order in tait_bryan_angles:
            if order in (RotationOrder.XYZ, RotationOrder.YZX,
                         RotationOrder.ZXY):
                a1y_sign = -1
                a3y_sign = -1
            elif order in (RotationOrder.XZY, RotationOrder.YXZ,
                           RotationOrder.ZYX):
                a2_sign = -1

            if convention == 'vector':
                v1 = self.apply_to(order.axis3)
                v2 = (~self).apply_to(order.axis1)
                a1_v = v1
                a2_index = order.index3
                a3_v = v2
            else:
                v1 = self.apply_to(order.axis1)
                v2 = (~self).apply_to(order.axis3)
                a1_v = v2
                a2_index = order.index1
                a3_v = v1

            if isclose(abs(v2[a2_index]), 1, abs_tol=1e-15):
                raise ValueError

            return (
                atan2(a1y_sign * a1_v[order.index2], a1x_sign * a1_v[order.index3]),
                a2_sign * asin(v2[a2_index]),
                atan2(a3y_sign * a3_v[order.index2], a3x_sign * a3_v[order.index1])
            )
        else:
            if order in (RotationOrder.XZX, RotationOrder.YXY,
                         RotationOrder.ZYZ):
                a3x_sign = -1
            elif order in (RotationOrder.XYX, RotationOrder.YZY,
                           RotationOrder.ZXZ):
                a1x_sign = -1

            other_index = {0, 1, 2} - {order.index1, order.index2, order.index3}
            other_index, = other_index

            v1 = self.apply_to(order.axis3)
            v2 = (~self).apply_to(order.axis1)

            if isclose(abs(v2[order.index3]), 1, abs_tol=1e-15):
                raise ValueError

            if convention == 'vector':
                a1_v = v1
                a3_v = v2
            else:
                a1_v = v2
                a3_v = v1

            return (
                atan2(a1y_sign * a1_v[order.index2], a1x_sign * a1_v[other_index]),
                a2_sign * acos(v2[order.index3]),
                atan2(a3y_sign * a3_v[order.index2], a3x_sign * a3_v[other_index])
            )

    @property
    def matrix(self):
        q0q0 = self.q0 * self.q0
        q0q1 = self.q0 * self.q1
        q0q2 = self.q0 * self.q2
        q0q3 = self.q0 * self.q3
        q1q1 = self.q1 * self.q1
        q1q2 = self.q1 * self.q2
        q1q3 = self.q1 * self.q3
        q2q2 = self.q2 * self.q2
        q2q3 = self.q2 * self.q3
        q3q3 = self.q3 * self.q3

        m = np.zeros((3, 3))
        m[0][0] = 2 * (q0q0 + q1q1) - 1
        m[1][0] = 2 * (q1q2 - q0q3)
        m[2][0] = 2 * (q1q3 + q0q2)

        m[0][1] = 2 * (q1q2 + q0q3)
        m[1][1] = 2 * (q0q0 + q2q2) - 1
        m[2][1] = 2 * (q2q3 - q0q1)

        m[0][2] = 2 * (q1q3 - q0q2)
        m[1][2] = 2 * (q2q3 + q0q1)
        m[2][2] = 2 * (q0q0 + q3q3) - 1

        return m

    def apply_to(self, vector):
        x = vector[0]
        y = vector[1]
        z = vector[2]

        r = self.q1 * x + self.q2 * y + self.q3 * z
        s = self

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

    def __invert__(self):
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


@unique
class RotationOrder(Enum):
    XYZ = 1
    XZY = 2
    YXZ = 3
    YZX = 4
    ZXY = 5
    ZYX = 6
    XYX = 7
    XZX = 8
    YXY = 9
    YZY = 10
    ZXZ = 11
    ZYZ = 12

    def __init__(self, value):
        axis1, axis2, axis3 = self.name
        indices = {'X': 0, 'Y': 1, 'Z': 2}

        arrays = [I, J, K]

        index1 = indices[axis1]
        index2 = indices[axis2]
        index3 = indices[axis3]

        self.axis1 = np.array(arrays[index1])
        self.axis2 = np.array(arrays[index2])
        self.axis3 = np.array(arrays[index3])

        self.index1 = index1
        self.index2 = index2
        self.index3 = index3


def normalize_angle(a, center=pi):
    return a - TWOPI * np.floor((a + pi - center) / TWOPI)
