# coding: utf-8
from __future__ import absolute_import, division, print_function

import platform
import sys

from represent import ReprMixin


class Machine(ReprMixin, object):
    def __init__(self, os, python_version, x64):
        self.os = os
        self.python_version = python_version
        self.x64 = x64

        super(Machine, self).__init__()

    def __eq__(self, other):
        return (self.os == other.os and
                self.python_version == other.python_version and
                self.x64 == other.x64)


def test_platform_coverage():
    machine = Machine(os=platform.system(),
                      python_version=sys.version_info[:2],
                      x64=sys.maxsize > 2 ** 32)

    assert machine.os in ('Darwin', 'Linux', 'Windows')
    assert machine.python_version in [
        (2, 7),
        (3, 3),
        (3, 4),
        (3, 5),
    ]

    # The charade below is so that in our unified coverage sourced from Travis
    # and AppVeyor, we can see that all the combinations of Python version, OS,
    # and 32/64 bits (Windows only) are tested.

    testmachine = Machine(os='Darwin', python_version=(2, 7), x64=True)
    if machine == testmachine:
        print('\n> Machine matched {}'.format(testmachine))

    testmachine = Machine(os='Darwin', python_version=(3, 3), x64=True)
    if machine == testmachine:
        print('\n> Machine matched {}'.format(testmachine))

    testmachine = Machine(os='Darwin', python_version=(3, 4), x64=True)
    if machine == testmachine:
        print('\n> Machine matched {}'.format(testmachine))

    testmachine = Machine(os='Darwin', python_version=(3, 5), x64=True)
    if machine == testmachine:
        print('\n> Machine matched {}'.format(testmachine))

    testmachine = Machine(os='Linux', python_version=(2, 7), x64=True)
    if machine == testmachine:
        print('\n> Machine matched {}'.format(testmachine))

    testmachine = Machine(os='Linux', python_version=(3, 3), x64=True)
    if machine == testmachine:
        print('\n> Machine matched {}'.format(testmachine))

    testmachine = Machine(os='Linux', python_version=(3, 4), x64=True)
    if machine == testmachine:
        print('\n> Machine matched {}'.format(testmachine))

    testmachine = Machine(os='Linux', python_version=(3, 5), x64=True)
    if machine == testmachine:
        print('\n> Machine matched {}'.format(testmachine))

    testmachine = Machine(os='Windows', python_version=(2, 7), x64=True)
    if machine == testmachine:
        print('\n> Machine matched {}'.format(testmachine))

    testmachine = Machine(os='Windows', python_version=(2, 7), x64=False)
    if machine == testmachine:
        print('\n> Machine matched {}'.format(testmachine))

    testmachine = Machine(os='Windows', python_version=(3, 3), x64=True)
    if machine == testmachine:
        print('\n> Machine matched {}'.format(testmachine))

    testmachine = Machine(os='Windows', python_version=(3, 3), x64=False)
    if machine == testmachine:
        print('\n> Machine matched {}'.format(testmachine))

    testmachine = Machine(os='Windows', python_version=(3, 4), x64=True)
    if machine == testmachine:
        print('\n> Machine matched {}'.format(testmachine))

    testmachine = Machine(os='Windows', python_version=(3, 4), x64=False)
    if machine == testmachine:
        print('\n> Machine matched {}'.format(testmachine))

    testmachine = Machine(os='Windows', python_version=(3, 5), x64=True)
    if machine == testmachine:
        print('\n> Machine matched {}'.format(testmachine))

    testmachine = Machine(os='Windows', python_version=(3, 5), x64=False)
    if machine == testmachine:
        print('\n> Machine matched {}'.format(testmachine))

    platforms = [
        Machine(os='Darwin', python_version=(2, 7), x64=True),
        Machine(os='Darwin', python_version=(3, 3), x64=True),
        Machine(os='Darwin', python_version=(3, 4), x64=True),
        Machine(os='Darwin', python_version=(3, 5), x64=True),
        Machine(os='Linux', python_version=(2, 7), x64=True),
        Machine(os='Linux', python_version=(3, 3), x64=True),
        Machine(os='Linux', python_version=(3, 4), x64=True),
        Machine(os='Linux', python_version=(3, 5), x64=True),
        Machine(os='Windows', python_version=(2, 7), x64=True),
        Machine(os='Windows', python_version=(2, 7), x64=False),
        Machine(os='Windows', python_version=(3, 3), x64=True),
        Machine(os='Windows', python_version=(3, 3), x64=False),
        Machine(os='Windows', python_version=(3, 4), x64=True),
        Machine(os='Windows', python_version=(3, 4), x64=False),
        Machine(os='Windows', python_version=(3, 5), x64=True),
        Machine(os='Windows', python_version=(3, 5), x64=False),
    ]

    print('\n> {}'.format(machine))

    assert machine in platforms
