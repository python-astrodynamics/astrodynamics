# coding: utf-8
# The frames implementation in astrodynamics is a derivative work of the
# implementation in Orekit. It retains the original license (see
# licenses/OREKIT.txt)
from __future__ import absolute_import, division, print_function

import errno
from collections import namedtuple

import astropy.units as u
import numpy as np
from astropy._erfa import nut06a, obl06, p06e, xy06
from astropy.time import Time
from astropy.utils.iers import IERS_A, IERS_A_URL
from scipy.interpolate import pchip_interpolate

from astrodynamics.rotation import Rotation

from ..utils.helper import get_neighbors_index, inherit_doc
from ..utils.iers import IERSConventions2010
from .frame import Frame, FrameProxy
from .mod import MOD_CONVENTIONS_2010_SIMPLE_EOP
from .transform import AbstractTransformProvider, Transform

TOD_CONVENTIONS_2010_SIMPLE_EOP = FrameProxy()

I = np.array([1, 0, 0])
K = np.array([0, 0, 1])


@inherit_doc.resolve
class TODTransformProvider(AbstractTransformProvider):
    def __init__(self, conventions):
        self.conventions = conventions

    @inherit_doc.mark
    def get_transform(self, time):
        moe = self.conventions.get_mean_obliquity(time)
        dpsi, deps = self.conventions.get_nutation_angles(time)

        # TODO: File management somewhere else
        try:
            iers_a = IERS_A.open()
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
            iers_a = IERS_A.open(IERS_A_URL)

        idx = get_neighbors_index(iers_a['MJD'], time.mjd, 4)

        mjd = iers_a['MJD'][idx]

        equinox = self.conventions.to_equinox(
            time, iers_a['dX_2000A_A'][idx], iers_a['dY_2000A_A'][idx])

        ddpsi = pchip_interpolate(
            mjd, equinox.dd_psi.si.value, time.mjd) * u.rad

        ddeps = pchip_interpolate(
            mjd, equinox.dd_epsilon.si.value, time.mjd) * u.rad

        dpsi += ddpsi
        deps += ddeps

        toe = moe + deps

        # set up the elementary rotations for nutation
        r1 = Rotation.from_axis_angle(I, toe)
        r2 = Rotation.from_axis_angle(K, dpsi)
        r3 = Rotation.from_axis_angle(I, -moe)

        nutation = r1.compose(r2.compose(r3))
        return Transform(time, rot=nutation)


@TOD_CONVENTIONS_2010_SIMPLE_EOP.register_factory
def _():
    tod_conventions_2010_simple_eop = Frame(
        parent=MOD_CONVENTIONS_2010_SIMPLE_EOP,
        transform_provider=TODTransformProvider(IERSConventions2010()),
        name='TOD_CONVENTIONS_2010_SIMPLE_EOP',
        pseudo_intertial=True)

    return tod_conventions_2010_simple_eop
