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
    call(['sphinx-build', '-b', 'html', '-E', 'docs', 'docs/_build/html'])

    call(['watchmedo', 'shell-command', '--patterns=*.rst;*.py',
          '--ignore-pattern=_build/*', '--recursive',
          '--command=sphinx-build -b html docs docs/_build/html'])


@task
def gen(skipdirhtml=False):
    """Generate html and dirhtml output."""
    docs_changelog = 'docs/changelog.rst'
    check_git_unchanged(docs_changelog)
    pandoc('--from=markdown', '--to=rst', '--output=' + docs_changelog, 'CHANGELOG.md')
    if not skipdirhtml:
        call(['sphinx-build', '-b', 'dirhtml', '-W', '-E', 'docs', 'docs/_build/dirhtml'])
    call(['sphinx-build', '-b', 'html', '-W', '-E', 'docs', 'docs/_build/html'])


@task
def clean():
    """Clean build directory."""
    rmtree('docs/_build')
    os.mkdir('docs/_build')
