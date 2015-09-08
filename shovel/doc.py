from __future__ import absolute_import, division, print_function

import os
from shutil import rmtree
from subprocess import call

from shovel import task


@task
def watch():
    """Renerate documentation when it changes."""

    # Start with a clean build
    call(['sphinx-build', '-b', 'html', '-E', 'doc', 'doc/_build/html'])

    call(['watchmedo', 'shell-command', '--patterns=*.rst;*.py',
          '--ignore-pattern=_build/*', '--recursive',
          '--command=sphinx-build -b html doc doc/_build/html'])


@task
def upload():
    """Generate, then upload to Read the Docs."""
    gen()
    raise NotImplementedError


@task
def gen():
    """Generate html and dirhtml output."""
    call(['sphinx-build', '-b', 'dirhtml', '-W', '-E', 'doc', 'doc/_build/dirhtml'])
    call(['sphinx-build', '-b', 'html', '-W', '-E', 'doc', 'doc/_build/html'])


@task
def clean():
    """Clean build directory."""
    rmtree('doc/_build')
    os.mkdir('doc/_build')
