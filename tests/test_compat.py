# coding: utf-8
from __future__ import absolute_import, division, print_function

import pytest

from astrodynamics.compat.contextlib import suppress


class TestSuppress:
    def test_instance_docs(self):
        # Issue 19330: ensure context manager instances have good docstrings
        cm_docstring = suppress.__doc__
        obj = suppress()
        obj.__doc__ == cm_docstring

    def test_no_result_from_enter(self):
        with suppress(ValueError) as enter_result:
            assert enter_result is None

    def test_no_exception(self):
        with suppress(ValueError):
            pow(2, 5) == 32

    def test_exact_exception(self):
        with suppress(TypeError):
            len(5)

    def test_exception_hierarchy(self):
        with suppress(LookupError):
            'Hello'[50]

    def test_other_exception(self):
        with pytest.raises(ZeroDivisionError):
            with suppress(TypeError):
                1 / 0

    def test_no_args(self):
        with pytest.raises(ZeroDivisionError):
            with suppress():
                1 / 0

    def test_multiple_exception_args(self):
        with suppress(ZeroDivisionError, TypeError):
            1 / 0
        with suppress(ZeroDivisionError, TypeError):
            len(5)

    def test_cm_is_reentrant(self):
        ignore_exceptions = suppress(Exception)
        with ignore_exceptions:
            pass
        with ignore_exceptions:
            len(5)
        ignored = False
        with ignore_exceptions:
            with ignore_exceptions:  # Check nested usage
                len(5)
            ignored = True
            1 / 0
        assert ignored
