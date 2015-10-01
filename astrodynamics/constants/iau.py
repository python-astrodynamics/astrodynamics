# coding: utf-8
from __future__ import absolute_import, division, print_function

from astropy import units as u  # flake8: noqa

# Absolute import used here so file can be exec'd standalone by documentation helper script.
from astrodynamics.constants import Constant  # flake8: noqa

__all__ = (
    'CONSTANT_OF_GRAVITATION',
    'SOLAR_MASS_PARAMETER',
    'EARTH_RADIUS_EQUATORIAL',
    'J2',
    'GEOCENTRIC_GRAVITATIONAL_CONSTANT',
    'GEOID_POTENTIAL',
    'EARTH_ANGULAR_VELOCITY',
    'MASS_RATIO_MOON_TO_EARTH',
    'MASS_RATIO_SUN_TO_MERCURY',
    'MASS_RATIO_SUN_TO_VENUS',
    'MASS_RATIO_SUN_TO_MARS',
    'MASS_RATIO_SUN_TO_JUPITER',
    'MASS_RATIO_SUN_TO_SATURN',
    'MASS_RATIO_SUN_TO_URANUS',
    'MASS_RATIO_SUN_TO_NEPTUNE',
    'MASS_RATIO_SUN_TO_PLUTO',
    'MASS_RATIO_CERES_TO_SUN',
    'MASS_RATIO_PALLAS_TO_SUN',
    'MASS_RATIO_VESTA_TO_SUN',
    'MERCURY_RADIUS_EQUATORIAL',
    'VENUS_RADIUS_EQUATORIAL',
    'EARTH_RADIUS_MEAN',
    'EARTH_RADIUS_POLAR',
    'MARS_RADIUS_MEAN',
    'MARS_RADIUS_EQUATORIAL',
    'MARS_RADIUS_POLAR',
    'JUPITER_RADIUS_MEAN',
    'JUPITER_RADIUS_EQUATORIAL',
    'JUPITER_RADIUS_POLAR',
    'SATURN_RADIUS_MEAN',
    'SATURN_RADIUS_EQUATORIAL',
    'SATURN_RADIUS_POLAR',
    'URANUS_RADIUS_MEAN',
    'URANUS_RADIUS_EQUATORIAL',
    'URANUS_RADIUS_POLAR',
    'NEPTUNE_RADIUS_MEAN',
    'NEPTUNE_RADIUS_EQUATORIAL',
    'NEPTUNE_RADIUS_POLAR',
    'PLUTO_RADIUS_EQUATORIAL',
    'MOON_RADIUS_MEAN',
    'MOON_RADIUS_EQUATORIAL',
    'MOON_RADIUS_POLAR',
    'SUN_RADIUS_EQUATORIAL',
    'SUN_MASS',
    'EARTH_MASS',
    'MOON_MASS',
    'MERCURY_MASS',
    'VENUS_MASS',
    'MARS_MASS',
    'JUPITER_MASS',
    'SATURN_MASS',
    'URANUS_MASS',
    'NEPTUNE_MASS',
    'PLUTO_MASS',
)

CONSTANT_OF_GRAVITATION = Constant(
    name='Constant of gravitation',
    value=6.67428e-11,
    unit='m3 / (kg s2)',
    uncertainty=6.7e-15,
    reference='IAU 2009/2012 System of Astronomical Constants')

SOLAR_MASS_PARAMETER = Constant(
    name='Solar mass parameter (TCB)',
    value=1.32712442099e20,
    unit='m3 / s2',
    uncertainty=1e10,
    reference='IAU 2009/2012 System of Astronomical Constants')

EARTH_RADIUS_EQUATORIAL = Constant(
    name='Equatorial radius of Earth (TT)',
    value=6378136.6,
    unit='m',
    uncertainty=0.1,
    reference='IAU 2009/2012 System of Astronomical Constants')

J2 = Constant(
    name='Dynamical form-factor for the Earth',
    value=0.0010826359,
    unit='',
    uncertainty=1e-10,
    reference='IAU 2009/2012 System of Astronomical Constants')

GEOCENTRIC_GRAVITATIONAL_CONSTANT = Constant(
    name='Geocentric gravitational constant (TCB)',
    value=3.986004418e14,
    unit='m3 / s2',
    uncertainty=8e5,
    reference='IAU 2009/2012 System of Astronomical Constants')

GEOID_POTENTIAL = Constant(
    name='Potential of the geoid',
    value=6.26368560e7,
    unit='m2 / s2',
    uncertainty=0.5,
    reference='IAU 2009/2012 System of Astronomical Constants')

EARTH_ANGULAR_VELOCITY = Constant(
    name='Nominal mean angular velocity of the Earth (TT)',
    value=7.292115e-5,
    unit='rad / s',
    uncertainty=0,
    reference='IAU 2009/2012 System of Astronomical Constants')

MASS_RATIO_MOON_TO_EARTH = Constant(
    name='Mass ratio: Moon to Earth',
    value=1.23000371e-2,
    unit='',
    uncertainty=4e-10,
    reference='IAU 2009/2012 System of Astronomical Constants')

MASS_RATIO_SUN_TO_MERCURY = Constant(
    name='Mass ratio: Sun to Mercury',
    value=6.0236e6,
    unit='',
    uncertainty=3e2,
    reference='IAU 2009/2012 System of Astronomical Constants')

MASS_RATIO_SUN_TO_VENUS = Constant(
    name='Mass ratio: Sun to Venus',
    value=4.08523719e5,
    unit='',
    uncertainty=8e-3,
    reference='IAU 2009/2012 System of Astronomical Constants')

MASS_RATIO_SUN_TO_MARS = Constant(
    name='Mass ratio: Sun to Mars',
    value=3.09870359e6,
    unit='',
    uncertainty=2e-2,
    reference='IAU 2009/2012 System of Astronomical Constants')

MASS_RATIO_SUN_TO_JUPITER = Constant(
    name='Mass ratio: Sun to Jupiter',
    value=1.047348644e3,
    unit='',
    uncertainty=1.7e-5,
    reference='IAU 2009/2012 System of Astronomical Constants')

MASS_RATIO_SUN_TO_SATURN = Constant(
    name='Mass ratio: Sun to Saturn',
    value=3.4979018e3,
    unit='',
    uncertainty=1e-4,
    reference='IAU 2009/2012 System of Astronomical Constants')

MASS_RATIO_SUN_TO_URANUS = Constant(
    name='Mass ratio: Sun to Uranus',
    value=2.290298e4,
    unit='',
    uncertainty=3e-2,
    reference='IAU 2009/2012 System of Astronomical Constants')

MASS_RATIO_SUN_TO_NEPTUNE = Constant(
    name='Mass ratio: Sun to Neptune',
    value=1.941226e4,
    unit='',
    uncertainty=3e-2,
    reference='IAU 2009/2012 System of Astronomical Constants')

MASS_RATIO_SUN_TO_PLUTO = Constant(
    name='Mass ratio: Sun to Pluto (134340)',
    value=1.36566e8,
    unit='',
    uncertainty=2.8e4,
    reference='IAU 2009/2012 System of Astronomical Constants')

MASS_RATIO_CERES_TO_SUN = Constant(
    name='Mass ratio: Ceres to Sun',
    value=4.72e-10,
    unit='',
    uncertainty=3e-12,
    reference='IAU 2009/2012 System of Astronomical Constants')

MASS_RATIO_PALLAS_TO_SUN = Constant(
    name='Mass ratio: Pallas to Sun',
    value=1.03e-10,
    unit='',
    uncertainty=3e-12,
    reference='IAU 2009/2012 System of Astronomical Constants')

MASS_RATIO_VESTA_TO_SUN = Constant(
    name='Mass ratio: Vesta to Sun',
    value=1.35e-10,
    unit='',
    uncertainty=3e-12,
    reference='IAU 2009/2012 System of Astronomical Constants')

MERCURY_RADIUS_EQUATORIAL = Constant(
    name='Equatorial radius of Mercury',
    value=2439.9,
    unit='km',
    uncertainty=1,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

VENUS_RADIUS_EQUATORIAL = Constant(
    name='Equatorial radius of Venus',
    value=6051.8,
    unit='km',
    uncertainty=1,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

EARTH_RADIUS_MEAN = Constant(
    name='Mean radius of Earth',
    value=6371.0084,
    unit='km',
    uncertainty=0.0001,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

EARTH_RADIUS_POLAR = Constant(
    name='Polar radius of Earth',
    value=6356.7519,
    unit='km',
    uncertainty=0.0001,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

MARS_RADIUS_MEAN = Constant(
    name='Mean radius of Mars',
    value=3389.50,
    unit='km',
    uncertainty=0.2,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

MARS_RADIUS_EQUATORIAL = Constant(
    name='Equatorial radius of Mars',
    value=3396.19,
    unit='km',
    uncertainty=0.1,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

MARS_RADIUS_POLAR = Constant(
    name='Polar radius of Mars',
    value=3376.20,
    unit='km',
    uncertainty=0.1,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

JUPITER_RADIUS_MEAN = Constant(
    name='Mean radius of Jupiter',
    value=69911,
    unit='km',
    uncertainty=6,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

JUPITER_RADIUS_EQUATORIAL = Constant(
    name='Equatorial radius of Jupiter',
    value=71492,
    unit='km',
    uncertainty=4,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

JUPITER_RADIUS_POLAR = Constant(
    name='Polar radius of Jupiter',
    value=66854,
    unit='km',
    uncertainty=10,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

SATURN_RADIUS_MEAN = Constant(
    name='Mean radius of Saturn',
    value=58232,
    unit='km',
    uncertainty=6,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

SATURN_RADIUS_EQUATORIAL = Constant(
    name='Equatorial radius of Saturn',
    value=60268,
    unit='km',
    uncertainty=4,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

SATURN_RADIUS_POLAR = Constant(
    name='Polar radius of Saturn',
    value=54364,
    unit='km',
    uncertainty=10,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

URANUS_RADIUS_MEAN = Constant(
    name='Mean radius of Uranus',
    value=25362,
    unit='km',
    uncertainty=7,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

URANUS_RADIUS_EQUATORIAL = Constant(
    name='Equatorial radius of Uranus',
    value=25559,
    unit='km',
    uncertainty=4,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

URANUS_RADIUS_POLAR = Constant(
    name='Polar radius of Uranus',
    value=24973,
    unit='km',
    uncertainty=20,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

NEPTUNE_RADIUS_MEAN = Constant(
    name='Mean radius of Neptune',
    value=24622,
    unit='km',
    uncertainty=19,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

NEPTUNE_RADIUS_EQUATORIAL = Constant(
    name='Equatorial radius of Neptune',
    value=24764,
    unit='km',
    uncertainty=15,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

NEPTUNE_RADIUS_POLAR = Constant(
    name='Polar radius of Neptune',
    value=24341,
    unit='km',
    uncertainty=30,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

PLUTO_RADIUS_EQUATORIAL = Constant(
    name='Equatorial radius of Pluto (134340)',
    value=1195,
    unit='km',
    uncertainty=5,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

MOON_RADIUS_MEAN = Constant(
    name='Mean radius of Moon',
    value=1737.4,
    unit='km',
    uncertainty=1,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

MOON_RADIUS_EQUATORIAL = Constant(
    name='Equatorial radius of Moon',
    value=1737.4,
    unit='km',
    uncertainty=1,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

MOON_RADIUS_POLAR = Constant(
    name='Polar radius of Moon',
    value=1737.4,
    unit='km',
    uncertainty=1,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

SUN_RADIUS_EQUATORIAL = Constant(
    name='Equatorial radius of Sun',
    value=696000,
    unit='km',
    uncertainty=1,
    reference='IAU WG on Cartographic Coordinates and Rotational Elements 2009')

SUN_MASS = SOLAR_MASS_PARAMETER / CONSTANT_OF_GRAVITATION

EARTH_MASS = GEOCENTRIC_GRAVITATIONAL_CONSTANT / CONSTANT_OF_GRAVITATION

MOON_MASS = MASS_RATIO_MOON_TO_EARTH * EARTH_MASS

MERCURY_MASS = SUN_MASS / MASS_RATIO_SUN_TO_MERCURY

VENUS_MASS = SUN_MASS / MASS_RATIO_SUN_TO_VENUS

MARS_MASS = SUN_MASS / MASS_RATIO_SUN_TO_MARS

JUPITER_MASS = SUN_MASS / MASS_RATIO_SUN_TO_JUPITER

SATURN_MASS = SUN_MASS / MASS_RATIO_SUN_TO_SATURN

URANUS_MASS = SUN_MASS / MASS_RATIO_SUN_TO_URANUS

NEPTUNE_MASS = SUN_MASS / MASS_RATIO_SUN_TO_NEPTUNE

PLUTO_MASS = SUN_MASS / MASS_RATIO_SUN_TO_PLUTO
