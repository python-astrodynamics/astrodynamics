*********
Constants
*********

.. py:module:: astrodynamics.constants

.. currentmodule:: astrodynamics.constants

.. autoclass:: Constant
   :members: name, uncertainty, reference

List of constants
=================

=================================  ===================================================================  =============
Constant                           Value                                                                Uncertainty
=================================  ===================================================================  =============
CONSTANT_OF_GRAVITATION            :math:`6.67428 \times 10^{-11} \; \mathrm{\frac{m^{3}}{kg\,s^{2}}}`  6.7e-15
SOLAR_MASS_PARAMETER               :math:`1.3271244 \times 10^{20} \; \mathrm{\frac{m^{3}}{s^{2}}}`     10000000000.0
EARTH_RADIUS_EQUATORIAL            :math:`6378136.6 \; \mathrm{m}`                                      0.1
J2                                 :math:`0.0010826359 \; \mathrm{}`                                    1e-10
GEOCENTRIC_GRAVITATIONAL_CONSTANT  :math:`3.9860044 \times 10^{14} \; \mathrm{\frac{m^{3}}{s^{2}}}`     800000.0
GEOID_POTENTIAL                    :math:`62636856 \; \mathrm{\frac{m^{2}}{s^{2}}}`                     0.5
EARTH_ANGULAR_VELOCITY             :math:`7.292115 \times 10^{-5} \; \mathrm{\frac{rad}{s}}`            0
MASS_RATIO_MOON_TO_EARTH           :math:`0.012300037 \; \mathrm{}`                                     4e-10
MASS_RATIO_SUN_TO_MERCURY          :math:`6023600 \; \mathrm{}`                                         300.0
MASS_RATIO_SUN_TO_VENUS            :math:`408523.72 \; \mathrm{}`                                       0.008
MASS_RATIO_SUN_TO_MARS             :math:`3098703.6 \; \mathrm{}`                                       0.02
MASS_RATIO_SUN_TO_JUPITER          :math:`1047.3486 \; \mathrm{}`                                       1.7e-05
MASS_RATIO_SUN_TO_SATURN           :math:`3497.9018 \; \mathrm{}`                                       0.0001
MASS_RATIO_SUN_TO_URANUS           :math:`22902.98 \; \mathrm{}`                                        0.03
MASS_RATIO_SUN_TO_NEPTUNE          :math:`19412.26 \; \mathrm{}`                                        0.03
MASS_RATIO_SUN_TO_PLUTO            :math:`1.36566 \times 10^{8} \; \mathrm{}`                           28000.0
MERCURY_RADIUS_MEAN                :math:`2439.9 \; \mathrm{km}`                                        1
MERCURY_RADIUS_EQUATORIAL          :math:`2439.9 \; \mathrm{km}`                                        1
MERCURY_RADIUS_POLAR               :math:`2439.9 \; \mathrm{km}`                                        1
VENUS_RADIUS_MEAN                  :math:`6051.8 \; \mathrm{km}`                                        1
VENUS_RADIUS_EQUATORIAL            :math:`6051.8 \; \mathrm{km}`                                        1
VENUS_RADIUS_POLAR                 :math:`6051.8 \; \mathrm{km}`                                        1
EARTH_RADIUS_MEAN                  :math:`6371.0084 \; \mathrm{km}`                                     0.0001
EARTH_RADIUS_POLAR                 :math:`6356.7519 \; \mathrm{km}`                                     0.0001
MARS_RADIUS_MEAN                   :math:`3389.5 \; \mathrm{km}`                                        0.2
MARS_RADIUS_EQUATORIAL             :math:`3396.19 \; \mathrm{km}`                                       0.1
MARS_RADIUS_POLAR                  :math:`3376.2 \; \mathrm{km}`                                        0.1
JUPITER_RADIUS_MEAN                :math:`69911 \; \mathrm{km}`                                         6
JUPITER_RADIUS_EQUATORIAL          :math:`71492 \; \mathrm{km}`                                         4
JUPITER_RADIUS_POLAR               :math:`66854 \; \mathrm{km}`                                         10
SATURN_RADIUS_MEAN                 :math:`58232 \; \mathrm{km}`                                         6
SATURN_RADIUS_EQUATORIAL           :math:`60268 \; \mathrm{km}`                                         4
SATURN_RADIUS_POLAR                :math:`54364 \; \mathrm{km}`                                         10
URANUS_RADIUS_MEAN                 :math:`25362 \; \mathrm{km}`                                         7
URANUS_RADIUS_EQUATORIAL           :math:`25559 \; \mathrm{km}`                                         4
URANUS_RADIUS_POLAR                :math:`24973 \; \mathrm{km}`                                         20
NEPTUNE_RADIUS_MEAN                :math:`24622 \; \mathrm{km}`                                         19
NEPTUNE_RADIUS_EQUATORIAL          :math:`24764 \; \mathrm{km}`                                         15
NEPTUNE_RADIUS_POLAR               :math:`24341 \; \mathrm{km}`                                         30
PLUTO_RADIUS_MEAN                  :math:`1195 \; \mathrm{km}`                                          5
PLUTO_RADIUS_EQUATORIAL            :math:`1195 \; \mathrm{km}`                                          5
PLUTO_RADIUS_POLAR                 :math:`1195 \; \mathrm{km}`                                          5
MOON_RADIUS_MEAN                   :math:`1737.4 \; \mathrm{km}`                                        1
MOON_RADIUS_EQUATORIAL             :math:`1737.4 \; \mathrm{km}`                                        1
MOON_RADIUS_POLAR                  :math:`1737.4 \; \mathrm{km}`                                        1
SUN_RADIUS_EQUATORIAL              :math:`696000 \; \mathrm{km}`                                        1
SUN_MASS                           :math:`1.9884159 \times 10^{30} \; \mathrm{kg}`                      N/A
EARTH_MASS                         :math:`5.9721864 \times 10^{24} \; \mathrm{kg}`                      N/A
MOON_MASS                          :math:`7.3458114 \times 10^{22} \; \mathrm{kg}`                      N/A
MERCURY_MASS                       :math:`3.3010423 \times 10^{23} \; \mathrm{kg}`                      N/A
VENUS_MASS                         :math:`4.8673205 \times 10^{24} \; \mathrm{kg}`                      N/A
MARS_MASS                          :math:`6.4169283 \times 10^{23} \; \mathrm{kg}`                      N/A
JUPITER_MASS                       :math:`1.8985234 \times 10^{27} \; \mathrm{kg}`                      N/A
SATURN_MASS                        :math:`5.684596 \times 10^{26} \; \mathrm{kg}`                       N/A
URANUS_MASS                        :math:`8.6819089 \times 10^{25} \; \mathrm{kg}`                      N/A
NEPTUNE_MASS                       :math:`1.0243093 \times 10^{26} \; \mathrm{kg}`                      N/A
PLUTO_MASS                         :math:`1.4560109 \times 10^{22} \; \mathrm{kg}`                      N/A
WGS84_EQUATORIAL_RADIUS            :math:`6378137 \; \mathrm{m}`                                        0
WGS84_FLATTENING                   :math:`0.0033528107 \; \mathrm{}`                                    0
WGS84_MU                           :math:`3.9860044 \times 10^{14} \; \mathrm{\frac{m^{3}}{s^{2}}}`     0
WGS84_ANGULAR_VELOCITY             :math:`7.292115 \times 10^{-5} \; \mathrm{\frac{rad}{s}}`            0
=================================  ===================================================================  =============

References
==========

=================================  ===============================================  ===============================================================
Constant                           Full name                                        Reference
=================================  ===============================================  ===============================================================
CONSTANT_OF_GRAVITATION            Constant of gravitation                          IAU 2009/2012 System of Astronomical Constants
SOLAR_MASS_PARAMETER               Solar mass parameter (TCB)                       IAU 2009/2012 System of Astronomical Constants
EARTH_RADIUS_EQUATORIAL            Equatorial radius of Earth (TT)                  IAU 2009/2012 System of Astronomical Constants
J2                                 Dynamical form-factor for the Earth              IAU 2009/2012 System of Astronomical Constants
GEOCENTRIC_GRAVITATIONAL_CONSTANT  Geocentric gravitational constant (TCB)          IAU 2009/2012 System of Astronomical Constants
GEOID_POTENTIAL                    Potential of the geoid                           IAU 2009/2012 System of Astronomical Constants
EARTH_ANGULAR_VELOCITY             Nominal mean angular velocity of the Earth (TT)  IAU 2009/2012 System of Astronomical Constants
MASS_RATIO_MOON_TO_EARTH           Mass ratio: Moon to Earth                        IAU 2009/2012 System of Astronomical Constants
MASS_RATIO_SUN_TO_MERCURY          Mass ratio: Sun to Mercury                       IAU 2009/2012 System of Astronomical Constants
MASS_RATIO_SUN_TO_VENUS            Mass ratio: Sun to Venus                         IAU 2009/2012 System of Astronomical Constants
MASS_RATIO_SUN_TO_MARS             Mass ratio: Sun to Mars                          IAU 2009/2012 System of Astronomical Constants
MASS_RATIO_SUN_TO_JUPITER          Mass ratio: Sun to Jupiter                       IAU 2009/2012 System of Astronomical Constants
MASS_RATIO_SUN_TO_SATURN           Mass ratio: Sun to Saturn                        IAU 2009/2012 System of Astronomical Constants
MASS_RATIO_SUN_TO_URANUS           Mass ratio: Sun to Uranus                        IAU 2009/2012 System of Astronomical Constants
MASS_RATIO_SUN_TO_NEPTUNE          Mass ratio: Sun to Neptune                       IAU 2009/2012 System of Astronomical Constants
MASS_RATIO_SUN_TO_PLUTO            Mass ratio: Sun to Pluto (134340)                IAU 2009/2012 System of Astronomical Constants
MERCURY_RADIUS_MEAN                Mean radius of Mercury                           IAU WG on Cartographic Coordinates and Rotational Elements 2009
MERCURY_RADIUS_EQUATORIAL          Equatorial radius of Mercury                     IAU WG on Cartographic Coordinates and Rotational Elements 2009
MERCURY_RADIUS_POLAR               Polar radius of Mercury                          IAU WG on Cartographic Coordinates and Rotational Elements 2009
VENUS_RADIUS_MEAN                  Mean radius of Venus                             IAU WG on Cartographic Coordinates and Rotational Elements 2009
VENUS_RADIUS_EQUATORIAL            Equatorial radius of Venus                       IAU WG on Cartographic Coordinates and Rotational Elements 2009
VENUS_RADIUS_POLAR                 Polar radius of Venus                            IAU WG on Cartographic Coordinates and Rotational Elements 2009
EARTH_RADIUS_MEAN                  Mean radius of Earth                             IAU WG on Cartographic Coordinates and Rotational Elements 2009
EARTH_RADIUS_POLAR                 Polar radius of Earth                            IAU WG on Cartographic Coordinates and Rotational Elements 2009
MARS_RADIUS_MEAN                   Mean radius of Mars                              IAU WG on Cartographic Coordinates and Rotational Elements 2009
MARS_RADIUS_EQUATORIAL             Equatorial radius of Mars                        IAU WG on Cartographic Coordinates and Rotational Elements 2009
MARS_RADIUS_POLAR                  Polar radius of Mars                             IAU WG on Cartographic Coordinates and Rotational Elements 2009
JUPITER_RADIUS_MEAN                Mean radius of Jupiter                           IAU WG on Cartographic Coordinates and Rotational Elements 2009
JUPITER_RADIUS_EQUATORIAL          Equatorial radius of Jupiter                     IAU WG on Cartographic Coordinates and Rotational Elements 2009
JUPITER_RADIUS_POLAR               Polar radius of Jupiter                          IAU WG on Cartographic Coordinates and Rotational Elements 2009
SATURN_RADIUS_MEAN                 Mean radius of Saturn                            IAU WG on Cartographic Coordinates and Rotational Elements 2009
SATURN_RADIUS_EQUATORIAL           Equatorial radius of Saturn                      IAU WG on Cartographic Coordinates and Rotational Elements 2009
SATURN_RADIUS_POLAR                Polar radius of Saturn                           IAU WG on Cartographic Coordinates and Rotational Elements 2009
URANUS_RADIUS_MEAN                 Mean radius of Uranus                            IAU WG on Cartographic Coordinates and Rotational Elements 2009
URANUS_RADIUS_EQUATORIAL           Equatorial radius of Uranus                      IAU WG on Cartographic Coordinates and Rotational Elements 2009
URANUS_RADIUS_POLAR                Polar radius of Uranus                           IAU WG on Cartographic Coordinates and Rotational Elements 2009
NEPTUNE_RADIUS_MEAN                Mean radius of Neptune                           IAU WG on Cartographic Coordinates and Rotational Elements 2009
NEPTUNE_RADIUS_EQUATORIAL          Equatorial radius of Neptune                     IAU WG on Cartographic Coordinates and Rotational Elements 2009
NEPTUNE_RADIUS_POLAR               Polar radius of Neptune                          IAU WG on Cartographic Coordinates and Rotational Elements 2009
PLUTO_RADIUS_MEAN                  Mean radius of Pluto (134340)                    IAU WG on Cartographic Coordinates and Rotational Elements 2009
PLUTO_RADIUS_EQUATORIAL            Equatorial radius of Pluto (134340)              IAU WG on Cartographic Coordinates and Rotational Elements 2009
PLUTO_RADIUS_POLAR                 Polar radius of Pluto (134340)                   IAU WG on Cartographic Coordinates and Rotational Elements 2009
MOON_RADIUS_MEAN                   Mean radius of Moon                              IAU WG on Cartographic Coordinates and Rotational Elements 2009
MOON_RADIUS_EQUATORIAL             Equatorial radius of Moon                        IAU WG on Cartographic Coordinates and Rotational Elements 2009
MOON_RADIUS_POLAR                  Polar radius of Moon                             IAU WG on Cartographic Coordinates and Rotational Elements 2009
SUN_RADIUS_EQUATORIAL              Equatorial radius of Sun                         IAU WG on Cartographic Coordinates and Rotational Elements 2009
WGS84_EQUATORIAL_RADIUS            WGS84 semi-major axis                            World Geodetic System 1984
WGS84_FLATTENING                   WGS84 Earth flattening factor                    World Geodetic System 1984
WGS84_MU                           WGS84 geocentric gravitational constant          World Geodetic System 1984
WGS84_ANGULAR_VELOCITY             WGS84 nominal earth mean angular velocity        World Geodetic System 1984
=================================  ===============================================  ===============================================================

.. _`license`: https://raw.githubusercontent.com/python-astrodynamics/astrodynamics/master/licenses/ASTROPY.txt
