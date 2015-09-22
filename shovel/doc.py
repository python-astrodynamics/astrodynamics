# coding: utf-8
from __future__ import absolute_import, division, print_function

import os
from shutil import rmtree
from subprocess import call

from plumbum.cmd import pandoc
from shovel import task

from _helpers import check_git_unchanged


@task
def watch():
    """Renerate documentation when it changes."""

    # Start with a clean build
    call(['sphinx-build', '-b', 'html', '-E', 'doc', 'doc/_build/html'])

    call(['watchmedo', 'shell-command', '--patterns=*.rst;*.py',
          '--ignore-pattern=_build/*', '--recursive',
          '--command=sphinx-build -b html doc doc/_build/html'])


@task
def gen(skipdirhtml=False):
    """Generate html and dirhtml output."""
    doc_changelog = 'doc/changelog.rst'
    check_git_unchanged(doc_changelog)
    pandoc('--from=markdown', '--to=rst', '--output=' + doc_changelog, 'CHANGELOG.md')
    if not skipdirhtml:
        call(['sphinx-build', '-b', 'dirhtml', '-W', '-E', 'doc', 'doc/_build/dirhtml'])
    call(['sphinx-build', '-b', 'html', '-W', '-E', 'doc', 'doc/_build/html'])


@task
def clean():
    """Clean build directory."""
    rmtree('doc/_build')
    os.mkdir('doc/_build')
