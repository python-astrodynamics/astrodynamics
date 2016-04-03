# coding: utf-8
# The frames implementation in astrodynamics is a derivative work of the
# implementation in Orekit. It retains the original license (see
# licenses/OREKIT.txt)
from __future__ import absolute_import, division, print_function

import errno
from math import atan2, cos, sin, sqrt

import astropy.units as u
import numpy as np
from astropy._erfa import s06, bpn2xy, pnm06a
from astropy.utils.iers import IERS_A, IERS_A_URL
from scipy.interpolate import pchip_interpolate

from ..rotation import Rotation
from .frame import Frame, FrameProxy
from .gcrf import GCRF
from .transform import AbstractTransformProvider, Transform


class CIRFConventions2010SimpleEOPTransformProvider(AbstractTransformProvider):
    def get_transform(self, date):
        try:
            iers_a = IERS_A.open()
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
            iers_a = IERS_A.open(IERS_A_URL)

        def find_nearest_index(array, value):
            idx_sorted = np.argsort(array)
            sorted_array = np.array(array[idx_sorted])
            idx = np.searchsorted(sorted_array, value, side="left")
            if idx >= len(array):
                idx_nearest = idx_sorted[len(array) - 1]
                return idx_nearest
            elif idx == 0:
                idx_nearest = idx_sorted[0]
                return idx_nearest
            else:
                if abs(value - sorted_array[idx - 1]) < abs(
                                value - sorted_array[idx]):
                    idx_nearest = idx_sorted[idx - 1]
                    return idx_nearest
                else:
                    idx_nearest = idx_sorted[idx]
                    return idx_nearest

        def get_neighbors_index(array, central, num_neighbors):
            idx = find_nearest_index(array, central)

            start = max(0, idx - (num_neighbors - 1) // 2)
            end = min(len(array), start + num_neighbors)
            start = end - num_neighbors

            return slice(start, end)

        idx = get_neighbors_index(iers_a['MJD'], date.mjd, 4)

        x, y = bpn2xy(pnm06a(date.jd1, date.jd2))

        dx = pchip_interpolate(
            iers_a['MJD'][idx],
            iers_a['dX_2000A_A'][idx].to(u.rad).value, date.mjd)

        dy = pchip_interpolate(
            iers_a['MJD'][idx],
            iers_a['dY_2000A_A'][idx].to(u.rad).value, date.mjd)

        xc = x + dx
        yc = y + dy

        sc = s06(date.jd1, date.jd2, xc, yc)

        x2Py2 = xc ** 2 + yc ** 2
        zP1 = 1 + sqrt(1 - x2Py2)
        r = sqrt(x2Py2)
        sPe2 = 0.5 * (sc + atan2(yc, xc))
        sPe2cos = cos(sPe2)
        sPe2sin = sin(sPe2)
        xPr = xc + r
        xPrcos = xPr * sPe2cos
        xPrsin = xPr * sPe2sin
        yCos = yc * sPe2cos
        ySin = yc * sPe2sin
        bpn = Rotation(zP1 * (xPrcos + ySin), -r * (yCos + xPrsin),
                       r * (xPrcos - ySin), zP1 * (yCos - xPrsin))

        return Transform(date, rot=bpn)


CIRF_CONVENTIONS_2010_SIMPLE_EOP = FrameProxy()


@CIRF_CONVENTIONS_2010_SIMPLE_EOP.register_factory
def _():
    cirf_conventions_2010_simple_eop = Frame(
        parent=GCRF,
        transform_provider=CIRFConventions2010SimpleEOPTransformProvider(),
        name='CIRF_CONVENTIONS_2010_SIMPLE_EOP',
        pseudo_intertial=True)

    return cirf_conventions_2010_simple_eop
