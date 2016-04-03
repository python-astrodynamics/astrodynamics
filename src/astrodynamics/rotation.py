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

from .compat.math import isclose
from .utils import read_only_property, verify_unit

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
    """This class implements rotations in a three-dimensional space.

    Rotations can be represented by several different mathematical entities
    (matrices, axis and angle, Cardan or Euler angles, quaternions). This class
    presents an higher level abstraction, more user-oriented and hiding this
    implementation details. Well, for the curious, we use quaternions for the
    internal representation. The user can build a rotation from any of these
    representations, and any of these representations can be retrieved from a
    :class:`Rotation` instance (see the various constructors and getters). In
    addition, a rotation can also be built implicitly from a set of vectors and
    their image.

    This implies that this class can be used to convert from one representation
    to another one. For example, converting a rotation matrix into a set of
    Cardan angles can be done using the following single line of code:

    .. code-block:: python

        angles = Rotation.from_matrix(matrix).get_angles(RotationOrder.XYZ)

    Focus is oriented on what a rotation *does* rather than on its underlying
    representation. Once it has been built, and regardless of its internal
    representation, a rotation is an *operator* which basically transforms three
    dimensional vectors into other three dimensional vectors. Depending on the
    application, the meaning of these vectors may vary and the semantics of the
    rotation also.

    Since a rotation is basically a vectorial operator, several rotations can be
    composed together and the composite operation :math:`r = r_{1} \circ r_{2}`
    (which means that for each vector :math:`u`, :math:`r(u) = r_{1}(r_{2}(u))`)
    is also a rotation. Hence we can consider that in addition to vectors, a
    rotation can be applied to other rotations as well (or to itself). With our
    previous notations, we would say we can apply :math:`r_{1}` to :math:`r_{2}`
    and the result we get is :math:`r = r_{1} \circ r_{2}`. For this purpose,
    the class provides the :meth:`compose` method.

    Rotations are immutable.
    """
    q0 = read_only_property('_q0')
    q1 = read_only_property('_q1')
    q2 = read_only_property('_q2')
    q3 = read_only_property('_q3')

    def __init__(self, q0, q1, q2, q3, normalized=False):
        """Build a rotation from the quaternion coordinates. A rotation can be
        built from a *normalized* quaternion, i.e. a quaternion for which
        :math:`q_{0}^{2} + q_{1}^{2} + q_{2}^{2} + q_{3}^{2} = 1`. By default,
        the constructor normalizes the quaternion. This step can be skipped
        using the ``normalized`` parameter.

        Note that some conventions put the scalar part of the quaternion as the
        4th component and the vector part as the first three components. This is
        *not* our convention. We put the scalar part as the first component.

        Parameters:
            q0: Scalar part of the quaternion.
            q1: First coordinate of the vectorial part of the quaternion.
            q2: Second coordinate of the vectorial part of the quaternion.
            q3: Third coordinate of the vectorial part of the quaternion.
            normalized: If the coordinates are already normalized, you may pass
                        ``True`` to skip the normalization step.
        """
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
        """Build a roation from an axis and an angle.

        Parameters:
            axis: Axis around which to rotate.
            angle: rotation angle [rad]

        Raises:
            TypeError: When the axis isn't a 1-D array with length 3.
            ValueError: When the axis norm is zero.

        :type angle: :class:`~astropy.units.quantity.Quantity`
        """
        check_convention(convention)
        angle = verify_unit(angle, 'rad')
        angle = angle.si.value

        if axis.shape != (3,):
            raise TypeError('axis should be a 1-D array with length 3')

        norm = np.linalg.norm(axis)
        if norm == 0:
            raise ValueError('Zero norm for rotation axis.')

        half_angle = -0.5 * angle if convention == 'vector' else 0.5 * angle
        coeff = sin(half_angle) / norm

        q0 = cos(half_angle)
        q1 = coeff * axis[0]
        q2 = coeff * axis[1]
        q3 = coeff * axis[2]

        return cls(q0, q1, q2, q3, normalized=True)

    @classmethod
    def from_matrix(cls, matrix):
        """Build a rotation from a 3X3 matrix.

        Rotation matrices are orthogonal matrices, i.e. unit matrices
        (which are matrices for which :math:`m \cdot m^{T} = I`) with real
        coefficients. The module of the determinant of unit matrices is
        1, among the orthogonal 3×3 matrices, only the ones having a
        positive determinant (+1) are rotation matrices.

        When a rotation is defined by a matrix with truncated values (typically
        when it is extracted from a technical sheet where only four to five
        significant digits are available), the matrix is not orthogonal anymore.
        This constructor handles this case transparently by using a copy of the
        given matrix and applying a correction to the copy in order to perfect
        its orthogonality. If the Frobenius norm of the correction needed is
        above the given threshold, then the matrix is considered to be too far
        from a true rotation matrix and an exception is thrown.

        Parameters:
            matrix: Rotation matrix.

        Raises:
            TypeError: When the matrix isn't a 3×3 matrix.
            ValueError: When the determinant of the computed orthogonal matrix
                        is negative.

        """
        if matrix.shape != (3, 3):
            raise TypeError('matrix should have shape (3, 3)')

        ort = matrix.dot(inv(sqrtm(matrix.T.dot(matrix))))

        if np.linalg.det(ort) < 0:
            raise ValueError('Not a rotation matrix.')

        return cls(*_quaternion_from_matrix(ort), normalized=True)

    @classmethod
    def from_euler_angles(cls, order, alpha1, alpha2, alpha3, convention='vector'):
        """Build a rotation from three Euler elementary rotations.

        Cardan rotations are three successive rotations around the
        canonical axes X, Y and Z, each axis being used once. There are
        6 such sets of rotations (XYZ, XZY, YXZ, YZX, ZXY and ZYX). Euler
        rotations are three successive rotations around the canonical
        axes X, Y and Z, the first and last rotations being around the
        same axis. There are 6 such sets of rotations (XYX, XZX, YXY,
        YZY, ZXZ and ZYZ), the most popular one being ZXZ.

        Beware that many people routinely use the term Euler angles even
        for what really are Cardan angles (this confusion is especially
        widespread in the aerospace business where Roll, Pitch and Yaw angles
        are often wrongly tagged as Euler angles).

        Parameters:
            order: Order of rotations to compose, from left to right.
            alpha1: Angle of the first elementary rotation.
            alpah2: Angle of the second elementary rotation.
            alpha3: Angle of the third elementary rotation.
            convention: Convention to use for the semantics of the angle.

        :type order: :class:`RotationOrder`

        .. seealso:: :ref:`Rotation Convention`
        """
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
        """Angle of the rotation (between 0 and :math:`\pi`)"""
        if self.q0 < -0.1 or self.q0 > 0.1:
            angle = 2 * asin(sqrt(self.q1 ** 2 + self.q2 ** 2 + self.q3 ** 2))
        elif self.q0 < 0:
            angle = 2 * acos(-self.q0)
        else:
            angle = 2 * acos(self.q0)

        return angle * u.rad

    def get_axis(self, convention='vector'):
        """Get the normalized axis of the rotation.

        Note that as :attr:`Rotation.angle` always returns an angle between 0
        and :math:`\pi`, changing the convention changes the direction of the
        axis, not the sign of the angle.

        Parameters:
            convention: Convention to use for the semantics of the angle.

        Returns:
            Normalized axis of the rotation.

        .. seealso:: :ref:`Rotation Convention`
        """
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
        """Get the Euler angles corresponding to the rotation.

        The equations show that each rotation can be defined by two different
        values of the Cardan or Euler angles set. For example if Cardan angles
        are used, the rotation defined by the angles :math:`a_{1}`,
        :math:`a_{2}` and :math:`a_{3}` is the same as the rotation defined by
        the angles :math:`\pi + a_{1}`, :math:`\pi - a_{2}` and
        :math:`\pi + a_{3}`. This method implements the following arbitrary
        choices:

        * for Cardan angles, the chosen set is the one for which the second
          angle is between :math:`-\\frac{\pi}{2}` and :math:`\\frac{pi}{2}`
          (i.e its cosine is positive),
        * for Proper Euler angles, the chosen set is the one for which the
          second angle is between 0 and :math:`\pi` (i.e its sine is positive).

        Cardan and Proper Euler angles have a very disappointing drawback: all
        of them have singularities. This means that if the instance is too close
        to the singularities corresponding to the given rotation order, it will
        be impossible to retrieve the angles. For Cardan angles, this is often
        called gimbal lock. There is *nothing* to do to prevent this, it is an
        intrinsic problem with Cardan and Proper Euler representation (but not a
        problem with the rotation itself, which is perfectly well defined). For
        Cardan angles, singularities occur when the second angle is close to
        :math:`\pm\\frac{\pi}{2}`, for Proper Euler angle singularities occu
        when the second angle is close to 0 or :math:`\pi`, this implies that
        the identity rotation is always singular for Euler angles!

        Parameters:
            order: Rotation order to use.
            convention: Convention to use for the semantics of the angle.

        Returns:
            An array of three angles, in the specified order.

        Raises:
            ValueError: When the rotation is singular with respect to the
                        specified order.

        :type order: :class:`RotationOrder`

        .. seealso:: :ref:`Rotation Convention`
        """
        check_convention(convention)

        cardan_angles = {
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

        if order in cardan_angles:
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
                raise ValueError('Cardan angles singularity.')

            return (
                atan2(a1y_sign * a1_v[order.index2],
                      a1x_sign * a1_v[order.index3]) * u.rad,
                a2_sign * asin(v2[a2_index]) * u.rad,
                atan2(a3y_sign * a3_v[order.index2],
                      a3x_sign * a3_v[order.index1]) * u.rad
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
                raise ValueError('Proper Euler angles singularity.')

            if convention == 'vector':
                a1_v = v1
                a3_v = v2
            else:
                a1_v = v2
                a3_v = v1

            return (
                atan2(a1y_sign * a1_v[order.index2],
                      a1x_sign * a1_v[other_index]) * u.rad,
                a2_sign * acos(v2[order.index3]) * u.rad,
                atan2(a3y_sign * a3_v[order.index2],
                      a3x_sign * a3_v[other_index]) * u.rad
            )

    @property
    def matrix(self):
        """Get the 3×3 matrix corresponding to the rotation."""
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
        """Apply the rotation to a vector.

        Parameters:
            vector: Vector to apply the rotation to.

        Returns:
            A new vector which is the image of `vector` by the rotation.

        Raises:
            TypeError: When the vector isn't a 1-D array with length 3.
        """

        if vector.shape != (3,):
            raise TypeError('vector should be a 1-D array with length 3')

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
        """Compose the instance with another rotation.

        If the semantics of the rotation's composition corresponds to the
        :ref:`Vector Operator` convention, applying the rotation to another
        rotation is computing the composition in an order compliant such that
        the following is true:

        .. testsetup::

            import astropy.units as un
            import numpy as np
            from astrodynamics.rotation import Rotation

            r1 = Rotation.from_axis_angle(np.array([1, 0, 0]), 5 * un.deg)
            r2 = Rotation.from_axis_angle(np.array([0, 1, 0]), 15 * un.deg)

        .. doctest::

            >>> import numpy as np
            >>> u = np.array([4, 5, 6])
            >>> v = r1.apply_to(u)
            >>> w = r2.apply_to(v)
            >>> comp = r2.compose(r1, convention='vector')
            >>> np.allclose(comp.apply_to(u), w)
            True

        If the semantics of the rotations' composition corresponds to the
        :ref:`Frame Transform` convention, the application order will be
        reversed:

        .. doctest::

            >>> comp = r1.compose(r2, convention='frame')
            >>> np.allclose(comp.apply_to(u), w)
            True

        Parameters:
            rotation: Rotation to apply the rotation to.
            convention: Convention to use for the semantics of the angle.

        :type rotation: :class:`Rotation`

        Returns:
            A new rotation which is the composition of `rotation` by the
            instance.

        .. seealso:: :ref:`Rotation Convention`
        """
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

    if ort.shape != (3, 3):
        raise TypeError('matrix should have shape (3, 3)')

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
    """This class is a utility representing a rotation order specification for
    Euler angles.

    **Cardan Angles**

    .. attribute:: XYZ

        This ordered set of rotations is around X, then around Y, then around Z.

    .. attribute:: XZY

        This ordered set of rotations is around X, then around Z, then around Y.

    .. attribute:: YXZ

        This ordered set of rotations is around Y, then around X, then around Z.

    .. attribute:: YZX

        This ordered set of rotations is around Y, then around Z, then around X.

    .. attribute:: ZXY

        This ordered set of rotations is around Z, then around X, then around Y.

    .. attribute:: ZYX

        This ordered set of rotations is around Z, then around Y, then around X.

    **Proper Euler Angles**

    .. attribute:: XYX

        This ordered set of rotations is around X, then around Y, then around X.

    .. attribute:: XZX

        This ordered set of rotations is around X, then around Z, then around X.

    .. attribute:: YXY

        This ordered set of rotations is around Y, then around X, then around Y.

    .. attribute:: YZY

        This ordered set of rotations is around Y, then around Z, then around Y.

    .. attribute:: ZXZ

        This ordered set of rotations is around Z, then around X, then around Z.

    .. attribute:: ZYZ

        This ordered set of rotations is around Z, then around Y, then around Z.

    **Instance Attributes**

    .. attribute:: axis1

        The axis of the first rotation.

    .. attribute:: axis2

        The axis of the second rotation.

    .. attribute:: axis3

        The axis of the third rotation.

    .. attribute:: index1

        The index of the first rotation.

    .. attribute:: index2

        The index of the second rotation.

    .. attribute:: index3

        The index of the third rotation.

    .. doctest::

        >>> from astrodynamics.rotation import RotationOrder
        >>> xyz = RotationOrder.XYZ
        >>> xyz.axis1
        array([1, 0, 0])
        >>> xyz.index1, xyz.index2, xyz.index3
        (0, 1, 2)

    """
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
        # Use the name to derive the axes.
        axis1, axis2, axis3 = self.name

        # Map axis names to array indices, e.g. v[0] is x coordinate of v
        indices = {'X': 0, 'Y': 1, 'Z': 2}

        # The axes in array form.
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


def normalize_angle(a, center=pi * u.rad):
    a = verify_unit(a, 'rad')
    center = verify_unit(center, 'rad')
    return a - TWOPI * np.floor((a + (pi * u.rad) - center) / TWOPI)
