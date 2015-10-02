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
        mu: Standard gravitational parameter [m\ :sup:`3`\ ·s\ :sup:`-2`]

    :type ellipsoid: :py:class:`~astrodynamics.bodies.ellipsoid.Ellipsoid`
    """
    def __init__(self, ellipsoid, mass, mu):
        self._ellipsoid = ellipsoid
        self._mass = verify_unit(mass, 'kg')
        self._mu = verify_unit(mu, 'm3 / s2')

    @classmethod
    def from_reference_ellipsoid(cls, ellipsoid, mass):
        """Construct from a
        :py:class:`~astrodynamics.bodies.ellipsoid.ReferenceEllipsoid`, which
        supplies ``mu``.

        Parameters:
            ellipsoid: Representative ellipsoid.
            mass: Mass of the body [kg].

        :type ellipsoid: :py:class:`~astrodynamics.bodies.ellipsoid.ReferenceEllipsoid`
        """
        return cls(ellipsoid=ellipsoid, mass=mass, mu=ellipsoid.mu)

    ellipsoid = read_only_property('_ellipsoid')
    mass = read_only_property('_mass')
    mu = read_only_property('_mu')

    def _repr_helper_(self, r):
        r.keyword_from_attr('ellipsoid')
        # View as Quantity to prevent full Constant repr.
        r.keyword_with_value('mass', self.mass.view(Quantity))
        r.keyword_with_value('mu', self.mu.view(Quantity))

earth = CelestialBody.from_reference_ellipsoid(ellipsoid=wgs84, mass=EARTH_MASS)
