# coding: utf-8
from __future__ import absolute_import, division, print_function

from pathlib import Path

from isort import SortImports
from shovel import task

# isort multi_line_output modes
GRID = 0
VERTICAL = 1
HANGING_INDENT = 2
VERTICAL_HANGING_INDENT = 3
HANGING_GRID = 4
HANGING_GRID_GROUPED = 5


@task
def format_imports():
    """Sort imports into a consistent style."""
    for initfile in Path('.').glob('astrodynamics/**/__init__.py'):
        SortImports(str(initfile),
                    multi_line_output=VERTICAL_HANGING_INDENT,
                    not_skip=['__init__.py'])

    for pyfile in Path('.').glob('astrodynamics/**/*.py'):
        SortImports(str(pyfile),
                    multi_line_output=HANGING_GRID,
                    skip=['__init__.py'])
