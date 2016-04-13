# coding: utf-8
# The frames implementation in astrodynamics is a derivative work of the
# implementation in Orekit. It retains the original license (see
# licenses/OREKIT.txt)
from __future__ import absolute_import, division, print_function

import errno
from math import atan2, cos, sin, sqrt

import astropy.units as u
import numpy as np
from astropy._erfa import bpn2xy, pnm06a, s06
from astropy.utils.iers import IERS_A, IERS_A_URL
from scipy.interpolate import pchip_interpolate

from ..rotation import Rotation
from ..utils.helper import get_neighbors_index
from ..utils.iers import IERSConventions2010
from .frame import Frame, FrameProxy
from .gcrf import GCRF
from .transform import AbstractTransformProvider, Transform


class CIRFSimpleEOPTransformProvider(AbstractTransformProvider):
    def __init__(self, conventions):
        self.conventions = conventions
        """Implementation of :class:`AbstractIERSConventions` to use."""

    def get_transform(self, time):
        # TODO: File management somewhere else
        try:
            iers_a = IERS_A.open()
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
            iers_a = IERS_A.open(IERS_A_URL)

        idx = get_neighbors_index(iers_a['MJD'], time.mjd, 4)

        x, y = self.conventions.get_cip_position(time)
        x, y = x.si.value, y.si.value

        dx = pchip_interpolate(
            iers_a['MJD'][idx],
            iers_a['dX_2000A_A'][idx].to(u.rad).value, time.mjd)

        dy = pchip_interpolate(
            iers_a['MJD'][idx],
            iers_a['dY_2000A_A'][idx].to(u.rad).value, time.mjd)

        # Position of the Celestial Intermediate Pole (CIP)
        xc = x + dx
        yc = y + dy

        # Position of the Celestial Intermediate Origin (CIO)
        sc = self.conventions.get_cio_locator(time, xc, yc).si.value

        # Set up the bias, precession and nutation rotation
        x2py2 = xc ** 2 + yc ** 2
        zp1 = 1 + sqrt(1 - x2py2)
        r = sqrt(x2py2)
        spe2 = 0.5 * (sc + atan2(yc, xc))
        spe2_cos = cos(spe2)
        spe2_sin = sin(spe2)
        xpr = xc + r
        xpr_cos = xpr * spe2_cos
        xpr_sin = xpr * spe2_sin
        y_cos = yc * spe2_cos
        y_sin = yc * spe2_sin
        bpn = Rotation(zp1 * (xpr_cos + y_sin), -r * (y_cos + xpr_sin),
                       r * (xpr_cos - y_sin), zp1 * (y_cos - xpr_sin))

        return Transform(time, rot=bpn)


CIRF_CONVENTIONS_2010_SIMPLE_EOP = FrameProxy()


@CIRF_CONVENTIONS_2010_SIMPLE_EOP.register_factory
def _():
    cirf_conventions_2010_simple_eop = Frame(
        parent=GCRF,
        transform_provider=CIRFSimpleEOPTransformProvider(IERSConventions2010()),
        name='CIRF_CONVENTIONS_2010_SIMPLE_EOP',
        pseudo_intertial=True)

    return cirf_conventions_2010_simple_eop
