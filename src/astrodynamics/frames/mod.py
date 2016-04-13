# coding: utf-8
# The frames implementation in astrodynamics is a derivative work of the
# implementation in Orekit. It retains the original license (see
# licenses/OREKIT.txt)
from __future__ import absolute_import, division, print_function

import numpy as np
from astropy.time import Time

from ..rotation import Rotation, RotationOrder
from ..utils import inherit_doc
from ..utils.iers import IERSConventions2010
from .eme2000 import EME2000
from .frame import Frame, FrameProxy
from .transform import AbstractTransformProvider, Transform


@inherit_doc.resolve
class MODTransformProvider(AbstractTransformProvider):
    """Mean Equinox of Date transform provider."""
    def __init__(self, conventions):
        self.conventions = conventions
        """Implementation of :class:`AbstractIERSConventions` to use."""

        i = np.array([1, 0, 0])

        j2000_epoch = Time('J2000', scale='tt')

        eps0 = conventions.get_mean_obliquity(j2000_epoch)
        r = Rotation.from_axis_angle(i, eps0, convention='frame')

        self.ecliptic_equator_pole_rotation = r

    @inherit_doc.mark
    def get_transform(self, time):
        pa = self.conventions.get_precession_angles(time)

        precession = self.ecliptic_equator_pole_rotation.compose(
            Rotation.from_euler_angles(
                RotationOrder.ZXZ,
                -pa.psi_a,
                -pa.omega_a,
                pa.chi_a,
                convention='frame'),
            convention='frame')

        return Transform(time, rot=precession)


MOD_CONVENTIONS_2010_SIMPLE_EOP = FrameProxy()


@MOD_CONVENTIONS_2010_SIMPLE_EOP.register_factory
def _():
    mod_conventions_2010_simple_eop = Frame(
        parent=EME2000,
        transform_provider=MODTransformProvider(IERSConventions2010()),
        name='MOD_CONVENTIONS_2010_SIMPLE_EOP',
        pseudo_intertial=True)

    return mod_conventions_2010_simple_eop
