# coding: utf-8
# The frames implementation in astrodynamics is a derivative work of the
# implementation in Orekit. It retains the original license (see
# licenses/OREKIT.txt)
from __future__ import absolute_import, division, print_function

from collections import namedtuple

import numpy as np
from astropy._erfa import p06e, obl06

from ..rotation import Rotation, RotationOrder
from .frame import Frame, FrameProxy
from .eme2000 import EME2000
from .transform import AbstractTransformProvider, Transform


class MODConventions2010TransformProvider(AbstractTransformProvider):
    def get_transform(self, date):
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


MOD_CONVENTIONS_2010 = FrameProxy()


@MOD_CONVENTIONS_2010.register_factory
def _():
    mod_conventions_2010 = Frame(
        parent=EME2000,
        transform_provider=MODConventions2010TransformProvider(),
        name='MOD_CONVENTIONS_2010',
        pseudo_intertial=True)

    return mod_conventions_2010
