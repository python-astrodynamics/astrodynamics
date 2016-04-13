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
    epsilon_0 = 84381.448 * u.arcsec

    # We get the angles from bi00 directly rather than use the rb matrix from
    # bp00 which returns additional matrices we don't need.
    d_psi_b, d_epsilon_b, alpha_0 = bi00()

    # Longitude correction
    d_psi_b = d_psi_b * u.rad

    # Obliquity correction
    d_epsilon_b = d_epsilon_b * u.rad

    # the ICRS right ascension of the J2000.0 mean equinox
    alpha_0 = alpha_0 * u.rad

    j2000_epoch = Time('J2000', scale='tt')

    i = np.array([1, 0, 0])
    j = np.array([0, 1, 0])
    k = np.array([0, 0, 1])

    # Obliquity correction
    r1 = Rotation.from_axis_angle(axis=i, angle=d_epsilon_b)
    r2 = Rotation.from_axis_angle(axis=j, angle=-d_psi_b * np.sin(epsilon_0))
    r3 = Rotation.from_axis_angle(axis=k, angle=-alpha_0)

    transform_provider = FixedTransformProvider(
        Transform(date=j2000_epoch, rot=r1.compose(r2.compose(r3))))

    eme2000 = Frame(
        parent=GCRF,
        transform_provider=transform_provider,
        name='EME2000',
        pseudo_intertial=True)

    return eme2000
