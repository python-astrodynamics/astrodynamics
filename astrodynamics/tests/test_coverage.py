# coding: utf-8
from __future__ import absolute_import, division, print_function

import platform
import sys


def test_platform_coverage():
    python_version = sys.version_info[:2]
    os = platform.system()
    is64bit = sys.maxsize > 2 ** 32

    machine = (os, python_version, is64bit)

    assert os in ('Darwin', 'Linux', 'Windows')
    assert python_version in [
        (2, 7),
        (3, 3),
        (3, 4),
        (3, 5),
    ]

    # The charade below is so that in our unified coverage sourced from Travis
    # and AppVeyor, we can see that all the combinations of Python version, OS,
    # and 32/64 bits (Windows only) are tested.
    if machine == ('Darwin', (2, 7), True):
        pass
    elif machine == ('Darwin', (3, 3), True):
        pass
    elif machine == ('Darwin', (3, 4), True):
        pass
    elif machine == ('Darwin', (3, 5), True):
        pass
    elif machine == ('Linux', (2, 7), True):
        pass
    elif machine == ('Linux', (3, 3), True):
        pass
    elif machine == ('Linux', (3, 4), True):
        pass
    elif machine == ('Linux', (3, 5), True):
        pass
    elif machine == ('Windows', (2, 7), True):
        pass
    elif machine == ('Windows', (2, 7), False):
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

    platforms = [
        ('Darwin', (3, 3), True),
        ('Darwin', (3, 4), True),
        ('Darwin', (3, 5), True),
        ('Linux', (2, 7), True),
        ('Linux', (3, 3), True),
        ('Linux', (3, 4), True),
        ('Linux', (3, 5), True),
        ('Windows', (2, 7), True),
        ('Windows', (2, 7), False),
        ('Windows', (3, 3), True),
        ('Windows', (3, 3), False),
        ('Windows', (3, 4), True),
        ('Windows', (3, 4), False),
        ('Windows', (3, 5), True),
        ('Windows', (3, 5), False),
    ]

    assert machine in platforms
