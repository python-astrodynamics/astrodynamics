# coding: utf-8
from __future__ import absolute_import, division, print_function

try:
    from functools import singledispatch, update_wrapper
except ImportError:
    from singledispatch import singledispatch, update_wrapper
