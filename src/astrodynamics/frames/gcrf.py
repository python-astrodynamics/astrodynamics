# coding: utf-8
# The frames implementation in astrodynamics is a derivative work of the
# implementation in Orekit. It retains the original license (see
# licenses/OREKIT.txt)
from __future__ import absolute_import, division, print_function

from astropy.time import Time

from .frame import Frame, FrameProxy
from .transform import FixedTransformProvider, Transform

GCRF = FrameProxy()


@GCRF.register_factory
def _():
    j2000_epoch = Time('J2000', scale='tt')

    transform_provider = FixedTransformProvider(
        transform=Transform(date=j2000_epoch))

    gcrf = Frame(
        parent=None,
        transform_provider=transform_provider,
        name='GCRF',
        pseudo_intertial=True)

    return gcrf
