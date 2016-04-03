# coding: utf-8
from __future__ import absolute_import, division, print_function

try:
    from abc import abstractstaticmethod
except ImportError:
    abstractstaticmethod = None


class _abstractstaticmethod(staticmethod):
    """
    A decorator indicating abstract staticmethods.

    Similar to abstractmethod.

    Usage:

        class C(metaclass=ABCMeta):
            @abstractstaticmethod
            def my_abstract_staticmethod(...):
                ...

    'abstractstaticmethod' is deprecated. Use 'staticmethod' with
    'abstractmethod' instead.
    """

    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super().__init__(callable)

abstractstaticmethod = abstractstaticmethod or _abstractstaticmethod
