# coding: utf-8
from __future__ import absolute_import, division, print_function

import pytest


def test_import_u():
    """constants module uses astropy.units. Check that none of the submodules
    leak variable 'u' into our namespace.
    """
    with pytest.raises(ImportError):
        from astrodynamics.constants import u  # noqa
