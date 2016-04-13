# coding: utf-8
from __future__ import absolute_import, division, print_function

from abc import ABCMeta, abstractmethod

import astropy.units as u
import numpy as np
import six

from ..rotation import Rotation
from ..utils import read_only_property, verify_unit


@six.add_metaclass(ABCMeta)
class AbstractTransformProvider(object):
    @abstractmethod
    def get_transform(self, time):
        # TODO: docstring
        raise NotImplementedError


def check_shape(v, shape):
    if v.shape != shape:
        raise ValueError('vector should be an array with shape {}'.format(shape))


class Transform(object):
    date = read_only_property('_date')
    translation = read_only_property('_translation')
    velocity = read_only_property('_velocity')
    acceleration = read_only_property('_acceleration')
    rotation = read_only_property('_rotation')
    angular_velocity = read_only_property('_angular_velocity')
    angular_acceleration = read_only_property('_angular_acceleration')

    def __init__(self, date, trans=None, vel=None, acc=None, rot=None,
                 ang_vel=None, ang_acc=None):
        self._date = date

        if trans is None:
            trans = np.array([0, 0, 0]) * u.m

        if vel is None:
            vel = np.array([0, 0, 0]) * u.m / u.s

        if acc is None:
            acc = np.array([0, 0, 0]) * u.m / u.s ** 2

        if rot is None:
            rot = Rotation(1, 0, 0, 0, normalized=True)

        if ang_vel is None:
            ang_vel = np.array([0, 0, 0]) * u.rad / u.s

        if ang_acc is None:
            ang_acc = np.array([0, 0, 0]) * u.rad / u.s ** 2

        check_shape(trans, (3,))
        check_shape(vel, (3,))
        check_shape(acc, (3,))
        check_shape(ang_vel, (3,))
        check_shape(ang_acc, (3,))

        self._translation = verify_unit(trans, 'm')
        self._velocity = verify_unit(vel, 'm / s')
        self._acceleration = verify_unit(acc, 'm / s2')
        self._rotation = rot
        self._angular_velocity = verify_unit(ang_vel, 'rad / s')
        self._angular_acceleration = verify_unit(ang_acc, 'rad / s2')

    def transform_position(self, position):
        verify_unit(position, 'm')
        return self.rotation.apply_to(self.translation.si.value + position.si.value) * u.m

    def transform(self, position, velocity, acceleration=None):
        p1 = self.translation.si.value
        v1 = self.velocity.si.value
        a1 = self.acceleration.si.value
        o1 = self.angular_velocity.si.value
        o1_dot = self.angular_acceleration.si.value

        p2 = verify_unit(position, 'm').si.value
        v2 = verify_unit(velocity, 'm / s').si.value

        if acceleration is not None:
            a2 = verify_unit(acceleration, 'm / s2').si.value
        else:
            a2 = np.zeros(3)

        p2 = vector_linear_combination(1, p2, 1, p1)
        v2 = vector_linear_combination(1, v2, 1, v1)
        a2 = vector_linear_combination(1, a2, 1, a1)

        pt = self.rotation.apply_to(p2)
        cross_p = np.cross(o1, pt)
        vt = self.rotation.apply_to(v2) - cross_p
        cross_v = np.cross(o1, cross_p)
        cross_cross_p = np.cross(o1, cross_p)
        cross_dot_p = np.cross(o1_dot, pt)

        u1 = self.rotation.apply_to(a2)
        u2 = cross_v
        u3 = cross_cross_p
        u4 = cross_dot_p

        at = vector_linear_combination(1, u1, -2, u2, -1, u3, -1, u4)
        return pt * u.m, vt * u.m / u.s, at * u.m / u.s ** 2

    def __add__(self, other):
        if not isinstance(other, Transform):
            return NotImplemented

        assert self.date == other.date

        p1 = self.translation.to(u.m).value
        v1 = self.velocity.to(u.m / u.s).value
        a1 = self.acceleration.to(u.m / u.s ** 2).value
        r1 = self.rotation
        o1 = self.angular_velocity.to(u.rad / u.s).value
        o1_dot = self.angular_acceleration.to(u.rad / u.s ** 2).value

        p2 = other.translation.to(u.m).value
        v2 = other.velocity.to(u.m / u.s).value
        a2 = other.acceleration.to(u.m / u.s ** 2).value
        r2 = other.rotation
        o2 = other.angular_velocity.to(u.rad / u.s).value
        o2_dot = other.angular_acceleration.to(u.rad / u.s ** 2).value

        trans = p1 + (~r1).apply_to(p2)

        o1_x_p2 = np.cross(o1, p2)

        vel = v1 + (~r1).apply_to(v2 + o1_x_p2)

        o1_x_o1_x_p2 = np.cross(o1, o1_x_p2)
        o1_x_v2 = np.cross(o1, v2)
        o1_dot_x_p2 = np.cross(o1_dot, p2)

        u1 = a2
        u2 = o1_x_v2
        u3 = o1_x_o1_x_p2
        u4 = o1_dot_x_p2

        vec1 = vector_linear_combination(1, u1, 2, u2, 1, u3, 1, u4)

        acc = a1 + (~r1).apply_to(vec1)

        rot = r1.compose(r2, convention='frame')

        ang_vel = o2 + r2.apply_to(o1)

        u1 = o2_dot
        u2 = r2.apply_to(o1_dot)
        u3 = np.cross(o2, r2.apply_to(o1))

        ang_acc = vector_linear_combination(1, u1, 1, u2, -1, u3)

        return Transform(
            date=self.date,
            trans=trans * u.m,
            vel=vel * u.m / u.s,
            acc=acc * u.m / u.s ** 2,
            rot=rot,
            ang_vel=ang_vel * u.rad / u.s,
            ang_acc=ang_acc * u.rad / u.s ** 2)

    def __invert__(self):
        p = self.translation.to(u.m).value
        v = self.velocity.to(u.m / u.s).value
        a = self.acceleration.to(u.m / u.s ** 2).value
        r = self.rotation
        o = self.angular_velocity.to(u.rad / u.s).value
        o_dot = self.angular_acceleration.to(u.rad / u.s ** 2).value

        rp = r.apply_to(p)
        rv = r.apply_to(v)
        ra = r.apply_to(a)

        o_x_rp = np.cross(o, rp)

        trans = -rp
        vel = o_x_rp - rv

        o_x_rv = np.cross(o, rv)
        o_dot_x_rp = np.cross(o_dot, rp)
        o_x_o_x_rp = np.cross(o, o_x_rp)

        u1 = ra
        u2 = o_x_rv
        u3 = o_dot_x_rp
        u4 = o_x_o_x_rp

        acc = vector_linear_combination(-1, u1, 2, u2, 1, u3, -1, u4)

        rot = ~self.rotation
        ang_vel = -rot.apply_to(o)
        ang_acc = -rot.apply_to(o_dot)

        return Transform(
            date=self.date,
            trans=trans * u.m,
            vel=vel * u.m / u.s,
            acc=acc * u.m / u.s ** 2,
            rot=rot,
            ang_vel=ang_vel * u.rad / u.s,
            ang_acc=ang_acc * u.rad / u.s ** 2)


def vector_linear_combination(a1, u1, a2, u2, a3=None, u3=None, a4=None, u4=None):
    if u3 is None:
        u3 = (None, None, None)

    if u4 is None:
        u4 = (None, None, None)

    return np.array([
        linear_combination(a1, u1[0], a2, u2[0], a3, u3[0], a4, u4[0]),
        linear_combination(a1, u1[1], a2, u2[1], a3, u3[1], a4, u4[1]),
        linear_combination(a1, u1[2], a2, u2[2], a3, u3[2], a4, u4[2]),
    ])


def linear_combination(a1, b1, a2, b2, a3=None, b3=None, a4=None, b4=None):
    if a4 is not None or b4 is not None:
        if a4 is None or b4 is None:
            raise ValueError('a4 and b4 cannot be None if either is passed.')

        if a3 is None or b3 is None:
            raise ValueError('a3 and b3 cannot be None if a4 and b4 are passed.')
    else:
        a4 = 0
        b4 = 1

    if a3 is not None or b3 is not None:
        if a3 is None or b3 is None:
            raise ValueError('a3 and b3 cannot be None if either is passed.')
    else:
        a3 = 0
        b3 = 1

    x = np.array([
        [b1, 0, 0, 0],
        [0, b2, 0, 0],
        [0, 0, b3, 0],
        [0, 0, 0, b4],
    ])
    y = np.array([a1, a2, a3, a4])
    try:
        result = np.sum(np.linalg.solve(x, y))
    except np.linalg.LinAlgError:
        result = a1 * b1 + a2 * b2 + a3 * b3 + a4 * b4
    return result


class FixedTransformProvider(AbstractTransformProvider):
    def __init__(self, transform):
        self.transform = transform

    def get_transform(self, date):
        self.transform._date = date
        # TODO: 'replace' method for new date
        return self.transform
