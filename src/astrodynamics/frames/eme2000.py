# coding: utf-8
# The frames implementation in astrodynamics is a derivative work of the
# implementation in Orekit. It retains the original license (see
# licenses/OREKIT.txt)
from __future__ import absolute_import, division, print_function

import astropy.units as u
import numpy as np
from astropy._erfa import bi00
from astropy.time import Time

from ..rotation import Rotation
from .frame import Frame, FrameProxy
from .gcrf import GCRF
from .transform import FixedTransformProvider, Transform

EME2000 = FrameProxy()


@EME2000.register_factory
def _():
    # Obliquity of the ecliptic.
    EPSILON_0 = 84381.448 * u.arcsec

    D_PSI_B, D_EPSILON_B, ALPHA_0 = bi00()

    # Longitude correction
    D_PSI_B = D_PSI_B * u.rad

    # Obliquity correction
    D_EPSILON_B = D_EPSILON_B * u.rad

    # the ICRS right ascension of the J2000.0 mean equinox
    ALPHA_0 = ALPHA_0 * u.rad

    J2000_EPOCH = Time('J2000', scale='tt')

    I = np.array([1, 0, 0])
    J = np.array([0, 1, 0])
    K = np.array([0, 0, 1])

    # Obliquity correction
    r1 = Rotation.from_axis_angle(axis=I, angle=D_EPSILON_B)
    r2 = Rotation.from_axis_angle(axis=J, angle=-D_PSI_B * np.sin(EPSILON_0))
    r3 = Rotation.from_axis_angle(axis=K, angle=-ALPHA_0)

    transform_provider = FixedTransformProvider(
        Transform(date=J2000_EPOCH, rot=r1.compose(r2.compose(r3))))

    eme2000 = Frame(
        parent=GCRF,
        transform_provider=transform_provider,
        name='EME2000',
        pseudo_intertial=True)

    return eme2000
