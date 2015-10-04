# coding: utf-8
from __future__ import absolute_import, division, print_function

import platform
import sys


def test_platform_coverage():
    python_version = sys.version_info[:2]
    os = platform.system()
    is64bit = sys.maxsize > 2 ** 32

    machine = (os, python_version, is64bit)

    if machine == ('Darwin', (2, 7), True):
        pass
    elif machine == ('Darwin', (2, 7), False):
        pass
    elif machine == ('Darwin', (3, 2), True):
        pass
    elif machine == ('Darwin', (3, 2), False):
        pass
    elif machine == ('Darwin', (3, 3), True):
        pass
    elif machine == ('Darwin', (3, 3), False):
        pass
    elif machine == ('Darwin', (3, 4), True):
        pass
    elif machine == ('Darwin', (3, 4), False):
        pass
    elif machine == ('Darwin', (3, 5), True):
        pass
    elif machine == ('Darwin', (3, 5), False):
        pass
    elif machine == ('Linux', (2, 7), True):
        pass
    elif machine == ('Linux', (2, 7), False):
        pass
    elif machine == ('Linux', (3, 2), True):
        pass
    elif machine == ('Linux', (3, 2), False):
        pass
    elif machine == ('Linux', (3, 3), True):
        pass
    elif machine == ('Linux', (3, 3), False):
        pass
    elif machine == ('Linux', (3, 4), True):
        pass
    elif machine == ('Linux', (3, 4), False):
        pass
    elif machine == ('Linux', (3, 5), True):
        pass
    elif machine == ('Linux', (3, 5), False):
        pass
    elif machine == ('Windows', (2, 7), True):
        pass
    elif machine == ('Windows', (2, 7), False):
        pass
    elif machine == ('Windows', (3, 2), True):
        pass
    elif machine == ('Windows', (3, 2), False):
        pass
    elif machine == ('Windows', (3, 3), True):
        pass
    elif machine == ('Windows', (3, 3), False):
        pass
    elif machine == ('Windows', (3, 4), True):
        pass
    elif machine == ('Windows', (3, 4), False):
        pass
    elif machine == ('Windows', (3, 5), True):
        pass
    elif machine == ('Windows', (3, 5), False):
        pass
