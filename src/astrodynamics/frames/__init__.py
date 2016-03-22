# coding: utf-8
# The frames implementation in astrodynamics is a derivative work of the
# implementation in Orekit. It retains the original license (see
# licenses/OREKIT.txt)
from __future__ import absolute_import, division, print_function

import weakref
from collections import Sequence
from math import sin

import astropy.units as u
import numpy as np
from astropy.time import Time
from represent import ReprHelper

from ..lowlevel.rotation import Rotation, RotationOrder
from ..utils import read_only_property
from .transform import Transform, FixedTransformProvider, AbstractTransformProvider


class AncestorsDescriptor(object):
    def __init__(self):
        self.instances = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if instance not in self.instances:
            self.instances[instance] = AncestorsProxy(instance)

        return self.instances[instance]


class AncestorsProxy(Sequence):
    def __init__(self, frame):
        self._ancestor_refs = [weakref.ref(frame)]

    def __getitem__(self, item):
        # Calculate index of last item we need to return
        if isinstance(item, int):
            if item >= 0:
                last = item
            else:
                last = len(self) + item
        elif isinstance(item, slice):
            _, stop, _ = item.indices(len(self))
            last = stop - 1
        else:
            raise TypeError('Ancestor indices must be integers or slices.')

        if last > len(self._ancestor_refs) - 1:
            ref = self._ancestor_refs[-1]
            current = ref()

            for i in range(len(self._ancestor_refs), last + 1):
                if current.parent is None:
                    raise IndexError('{} has no parent.'.format(current))
                self._ancestor_refs.append(weakref.ref(current.parent))
                current = current.parent

        if isinstance(item, int):
            ref = self._ancestor_refs[item]
            return ref()
        elif isinstance(item, slice):
            return [ref() for ref in self._ancestor_refs[item]]

    def __len__(self):
        return self.depth + 1


class Frame(object):
    ancestors = AncestorsDescriptor()

    def __init__(self, parent, transform_provider, name, pseudo_intertial):
        self._parent = parent
        self._depth = parent.depth + 1 if parent is not None else 0
        self._transform_provider = transform_provider
        self._name = name
        self._pseudo_intertial = pseudo_intertial

    parent = read_only_property('_parent')
    depth = read_only_property('_depth')
    transform_provider = read_only_property('_transform_provider')
    name = read_only_property('_name')
    pseudo_intertial = read_only_property('_pseudo_intertial')

    def transform_to(self, destination_frame, date):
        if destination_frame is self:
            return Transform(date)

        common = Frame.find_common_ancestor(self, destination_frame)

        common_to_instance = Transform(date)
        for frame in self.ancestors:
            if frame is common:
                break
            common_to_instance = (
                frame.transform_provider.get_transform(date) +
                common_to_instance)

        common_to_destination = Transform(date)
        for frame in destination_frame.ancestors:
            if frame is common:
                break
            common_to_destination = (
                frame.transform_provider.get_transform(date) +
                common_to_destination)

        return ~common_to_instance + common_to_destination

    @staticmethod
    def find_common_ancestor(from_, to):
        if from_.depth > to.depth:
            current_from = from_.ancestors[from_.depth - to.depth]
            current_to = to
        else:
            current_from = from_
            current_to = to.ancestors[to.depth - from_.depth]

        while current_from != current_to:
            current_from = current_from.parent
            current_to = current_to.parent

        return current_from

    def __repr__(self):
        r = ReprHelper(self)
        r.parantheses = ('<', '>')
        r.keyword_from_attr('name')
        return str(r)


class FrameProxy(object):
    """Proxy a :class:`Frame` using a factory function for lazy initialisation."""
    def __init__(self, factory):
        self._factory = factory
        self._frame = None

    def __getattr__(self, name):
        if self._frame is None:
            self._frame = self._factory()
        return getattr(self._frame, name)


def gcrf_factory():
    J2000_EPOCH = Time('J2000', scale='tt')

    transform_provider = FixedTransformProvider(
        transform=Transform(date=J2000_EPOCH))

    GCRF = Frame(
        parent=None,
        transform_provider=transform_provider,
        name='GCRF',
        pseudo_intertial=True)

    return GCRF

GCRF = FrameProxy(gcrf_factory)


def eme2000_factory():
    from astropy._erfa import bi00

    # Obliquity of the ecliptic.
    EPSILON_0 = 84381.448 * u.arcsec

    # D_PSI_B: Longitude correction
    # D_EPSILON_B: Obliquity correction
    # ALPHA_0: the ICRS right ascension of the J2000.0 mean equinox
    D_PSI_B, D_EPSILON_B, ALPHA_0 = bi00()

    J2000_EPOCH = Time('J2000', scale='tt')

    I = np.array([1, 0, 0])
    J = np.array([0, 1, 0])
    K = np.array([0, 0, 1])

    # Obliquity correction
    r1 = Rotation.from_axis_angle(axis=I, angle=D_EPSILON_B)
    r2 = Rotation.from_axis_angle(axis=J, angle=-D_PSI_B * sin(EPSILON_0))
    r3 = Rotation.from_axis_angle(axis=K, angle=-ALPHA_0)

    transform_provider = FixedTransformProvider(
        Transform(date=J2000_EPOCH, rot=r1.apply_to(r2.apply_to(r3))))

    EME2000 = Frame(
        parent=GCRF,
        transform_provider=transform_provider,
        name='EME2000',
        pseudo_intertial=True)

    return EME2000

EME2000 = FrameProxy(eme2000_factory)


def mod_conventions_2010_factory():

    class MODConventions2010TransformProvider(AbstractTransformProvider):
        def get_transform(self, date):
            from astropy._erfa import p06e, obl06
            from collections import namedtuple

            P06eResults = namedtuple(
                'P06eResults', [
                    'eps0',
                    'psia',
                    'oma',
                    'bpa',
                    'bqa',
                    'pia',
                    'bpia',
                    'epsa',
                    'chia',
                    'za',
                    'zetaa',
                    'thetaa',
                    'pa',
                    'gam',
                    'phi',
                    'psi'])

            I = np.array([1, 0, 0])

            eps0 = obl06(date.jd1, date.jd2)
            r4 = Rotation.from_axis_angle(I, eps0, convention='frame')

            results = P06eResults(*p06e(date.jd1, date.jd2))

            psia = results.psia
            oma = results.oma
            chia = results.chia

            precession = r4.compose(Rotation.from_euler_angles(
                RotationOrder.ZXZ, -psia, -oma, chia, convention='frame'))

            return Transform(date, rot=precession)

    MOD_CONVENTIONS_2010 = Frame(
        parent=EME2000,
        transform_provider=MODConventions2010TransformProvider(),
        name='MOD_CONVENTIONS_2010',
        pseudo_intertial=True,
    )

    return MOD_CONVENTIONS_2010

MOD_CONVENTIONS_2010 = FrameProxy(mod_conventions_2010_factory)
