# coding: utf-8
from __future__ import absolute_import, division, print_function

import numpy as np
from astropy.units import Quantity, Unit
from astropy.utils import lazyproperty
from represent import ReprHelperMixin

from ..util import read_only_property


class Constant(ReprHelperMixin, Quantity):
    """A physical or astronomical constant.

    These objects are quantities that are meant to represent physical
    constants.

    Parameters:
        name: The full name of the constant.
        value: Numerical value of constant
        unit (str): Units for given value. Must be parsable by
                    :py:class:`astropy.units.Unit`
        uncertainty: The known uncertainty in this constant's value.
        reference: The source used for the value of this constant.

    This class is modified from :py:class:`astropy.constants.Constant`. It
    retains the original `license`_.
    """
    def __new__(cls, name, value, unit, uncertainty, reference):
        # By-pass Quantity initialization, since units may not yet be
        # initialized here, and we store the unit in string form.
        inst = np.array(value).view(cls)

        inst._name = name
        inst._value = value
        inst._unit_string = unit
        inst._uncertainty = uncertainty
        inst._reference = reference

        return inst

    def _repr_helper_(self, r):
        r.keyword_from_attr('name')
        r.keyword_from_attr('value')
        r.keyword_with_value('unit', str(self.unit))
        r.keyword_from_attr('uncertainty')
        r.keyword_from_attr('reference')

    def __quantity_subclass__(self, unit):
        return super(Constant, self).__quantity_subclass__(unit)[0], False

    def copy(self):
        """
        Return a copy of this `Constant` instance.  Since they are by
        definition immutable, this merely returns another reference to
        ``self``.
        """
        return self

    __deepcopy__ = __copy__ = copy

    name = read_only_property('_name', 'The full name of the constant.')

    uncertainty = read_only_property(
        name='_uncertainty',
        docstring="The known uncertainty in this constant's value")

    reference = read_only_property(
        name='_reference',
        docstring='The source used for the value of this constant.')

    @lazyproperty
    def _unit(self):
        """The unit(s) in which this constant is defined."""

        return Unit(self._unit_string)

    def __array_finalize__(self, obj):
        for attr in ('_name', '_value', '_unit_string',
                     '_uncertainty', '_reference', '_system'):
            setattr(self, attr, getattr(obj, attr, None))
