# coding: utf-8
from __future__ import absolute_import, division, print_function

from abc import ABCMeta, abstractmethod
from collections import namedtuple

import numpy as np
from astropy import units as u
from astropy._erfa import bpn2xy, nut06a, obl06, p06e, pnm06a, s06
from astropy.time import Time
from six import add_metaclass

from .helper import inherit_doc, verify_unit

P06eResults = namedtuple(
    'P06eResults', [
        'eps0',
        'psia',
        'oma',
        'bpa',
        'bqa',
        'pia',
        'bpia',
        'epsa',
        'chia',
        'za',
        'zetaa',
        'thetaa',
        'pa',
        'gam',
        'phi',
        'psi'])

PrecessionAngles = namedtuple('PrecessionAngles', ['psi_a', 'omega_a', 'chi_a'])

Position = namedtuple('Position', ['x', 'y'])

NutationAngles = namedtuple('NutationAngles', ['d_psi', 'd_epsilon'])

EquinoxNutationCorrection = namedtuple(
    'EquinoxNutationCorrection', ['dd_psi', 'dd_epsilon'])


@add_metaclass(ABCMeta)
class AbstractIERSConventions(object):
    """Abstract class for implementing IERS Conventions."""
    @abstractmethod
    def get_mean_obliquity(self, time):
        # TODO: docstring
        raise NotImplementedError

    @abstractmethod
    def get_precession_angles(self, time):
        # TODO: docstring
        raise NotImplementedError

    @abstractmethod
    def get_cip_position(self, time):
        # TODO: docstring
        raise NotImplementedError

    @abstractmethod
    def get_cio_locator(self, time, x, y):
        # TODO: docstring
        raise NotImplementedError

    @abstractmethod
    def get_nutation_angles(self, time):
        # TODO: docstring
        raise NotImplementedError

    @abstractmethod
    def to_equinox(self, time, dx, dy):
        # TODO: docstring
        raise NotImplementedError


@inherit_doc.resolve
class IERSConventions2010(AbstractIERSConventions):
    """IERS Conventions 2010"""
    def __init__(self):
        self.nutation_reference_epoch = Time('J2000', scale='tt')
        self.epsilon0 = self.get_mean_obliquity(self.nutation_reference_epoch)

    @inherit_doc.mark
    def get_mean_obliquity(self, time):
        return obl06(time.jd1, time.jd2) * u.rad

    @inherit_doc.mark
    def get_precession_angles(self, time):
        p = P06eResults(*p06e(time.jd1, time.jd2))
        return PrecessionAngles(
            psi_a=p.psia * u.rad, omega_a=p.oma * u.rad, chi_a=p.chia * u.rad)

    @inherit_doc.mark
    def get_cip_position(self, time):
        x, y = bpn2xy(pnm06a(time.jd1, time.jd2))
        return Position(x=x * u.one, y=y * u.one)

    @inherit_doc.mark
    def get_cio_locator(self, time, x, y):
        x = verify_unit(x, '')
        y = verify_unit(y, '')
        return s06(time.jd1, time.jd2, x.value, y.value) * u.rad

    @inherit_doc.mark
    def get_nutation_angles(self, time):
        dpsi, deps = nut06a(time.jd1, time.jd2)
        return NutationAngles(d_psi=dpsi * u.rad, d_epsilon=deps * u.rad)

    @inherit_doc.mark
    def to_equinox(self, time, dx, dy):
        dx = verify_unit(dx, 'rad').si.value
        dy = verify_unit(dy, 'rad').si.value

        angles = self.get_precession_angles(time)

        psi_a = angles.psi_a.si.value
        chi_a = angles.chi_a.si.value

        sin_ea = np.sin(self.get_mean_obliquity(time))
        cos_e0 = np.cos(self.epsilon0)
        c = psi_a * cos_e0 - chi_a
        o_p_c2 = 1 + c ** 2

        ddpsi = (dx - c * dy) / (sin_ea * o_p_c2) * u.rad
        ddeps = (dy + c * dx) / o_p_c2 * u.rad

        return EquinoxNutationCorrection(dd_psi=ddpsi, dd_epsilon=ddeps)
