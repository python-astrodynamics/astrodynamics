# coding: utf-8
from __future__ import absolute_import, division, print_function

from astropy.units import Quantity
from represent import ReprHelperMixin

from ..constants import EARTH_MASS
from ..util import read_only_property, verify_unit
from .ellipsoid import wgs84

__all__ = (
    'CelestialBody',
    'earth',
)

class CelestialBody(ReprHelperMixin, object):
    """Celestial body.

    Parameters:
        ellipsoid: Representative ellipsoid.
        mass: Mass of the body [kg].

    :type ellipsoid: :py:class:`~astrodynamics.bodies.ellipsoid.Ellipsoid`
    """
    def __init__(self, ellipsoid, mass):
        self._ellipsoid = ellipsoid
        self._mass = verify_unit(mass, 'kg')

    ellipsoid = read_only_property('_ellipsoid')
    mass = read_only_property('_mass')

    def _repr_helper_(self, r):
        r.keyword_from_attr('ellipsoid')
        # View as Quantity to prevent full Constant repr.
        r.keyword_with_value('mass', self.mass.view(Quantity))

earth = CelestialBody(ellipsoid=wgs84, mass=EARTH_MASS)
