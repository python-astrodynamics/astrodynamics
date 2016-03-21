# coding: utf-8
from __future__ import absolute_import, division, print_function

import re
from collections import OrderedDict, namedtuple
from itertools import chain
from pathlib import Path

from shovel import task
from tabulate import tabulate

from astrodynamics.constants import Constant

from _helpers import check_git_unchanged

ParsedConstant = namedtuple('ParsedConstant', ['name', 'value'])
constant_re = re.compile('^(?P<name>[A-Z0-9_]+) = (?P<value>.+)')

TEMPLATE = """# coding: utf-8
from __future__ import absolute_import, division, print_function

from astropy import units as u  # noqa

# Absolute import used here so file can be exec'd
# standalone by documentation helper script.
from astrodynamics.constants import Constant  # noqa

__all__ = (
{all_string}
)

{constant_string}"""

INIT_TEMPLATE = """# coding: utf-8
from __future__ import absolute_import, division, print_function

from .constant import Constant
{imports}

__all__ = (
    'Constant',
{all_string}
)
"""

IMPORT_TEMPLATE = """from .{modulename} import (
{import_string}
)"""


DOC_TEMPLATE = """*********
Constants
*********

.. currentmodule:: astrodynamics.constants

.. autoclass:: Constant
   :members: name, uncertainty, reference

List of constants
=================

{value_table}

References
==========

{details_table}

.. _`license`: https://raw.githubusercontent.com/python-astrodynamics/astrodynamics/master/licenses/ASTROPY.txt
"""  # noqa


def get_constants_from_data():
    # Mapping of module names to list of constants.
    constants = dict()

    sourcedir = Path('data', 'constants')
    for constantsfile in sourcedir.glob('*.txt'):
        modulename = constantsfile.stem
        if modulename == 'README':
            continue
        constants[modulename] = []

        with constantsfile.open(encoding='utf-8') as f:
            name = value = None

            for line in f:
                if line.lstrip().startswith('#'):
                    continue
                elif line.startswith('    '):
                    # This is a multiline constant definition
                    assert value is not None
                    value += line
                else:
                    match = constant_re.match(line)
                    if match:
                        # This means new constant is being defined.

                        if name is not None:
                            constants[modulename].append(
                                ParsedConstant(name=name, value=value))
                            name = value = None

                        name = match.group('name')
                        value = match.group('value') + '\n'

            if name is not None:
                constants[modulename].append(
                    ParsedConstant(name=name, value=value))

    return constants


@task
def make_module(yes=False):
    """Use the templates defined above to create the astrodynamics.constants
    module.
    """
    constants = get_constants_from_data()
    init_imports = dict()
    pythondir = Path('astrodynamics', 'constants')

    for modulename, constants_list in constants.items():
        pythonfile = pythondir / '{}.py'.format(modulename)
        if pythonfile.exists():
            check_git_unchanged(str(pythonfile), yes=yes)

        all_lines = ("    '{}',".format(c.name) for c in constants_list)
        all_string = '\n'.join(all_lines)

        init_import_lines = ('    {},'.format(c.name) for c in constants_list)
        init_import_string = '\n'.join(init_import_lines)

        init_imports[modulename] = IMPORT_TEMPLATE.format(
            modulename=modulename,
            import_string=init_import_string)

        line = '{c.name} = {c.value}'
        constant_lines = (line.format(c=c) for c in constants_list)
        constant_string = '\n'.join(constant_lines)

        with pythonfile.open('w', encoding='utf-8') as f:
            f.write(TEMPLATE.format(all_string=all_string,
                                    constant_string=constant_string))

    initfile = pythondir / '__init__.py'
    if initfile.exists():
        check_git_unchanged(str(initfile), yes=yes)

    # Sort init_imports and constants by key
    init_imports = OrderedDict(sorted(init_imports.items(), key=lambda t: t[0]))
    imports = '\n'.join(init_imports.values())

    constants = OrderedDict(sorted(constants.items(), key=lambda t: t[0]))
    flat_constants = chain.from_iterable(constants.values())
    all_lines = ("    '{}',".format(c.name) for c in flat_constants)
    all_string = '\n'.join(all_lines)

    with initfile.open('w', encoding='utf-8') as f:
        f.write(INIT_TEMPLATE.format(imports=imports, all_string=all_string))


@task
def make_documentation(yes=False):
    """Use the templates defined above to create the astrodynamics.constants
    documentation.
    """
    constants = get_constants_from_data()
    docfile = Path('docs', 'modules', 'constants.rst')

    pythondir = Path('astrodynamics', 'constants')
    for pythonfile in pythondir.glob('*.py'):
        if pythonfile.stem not in constants:
            # Skip non-definition files: __init__.py, constant.py
            continue

        with pythonfile.open() as f:
            exec(f.read())

    # Sort constants by key
    constants = OrderedDict(sorted(constants.items(), key=lambda t: t[0]))

    # Hide individual modules from constants documentation
    flat_constants = chain.from_iterable(constants.values())

    value_table_data = []
    value_table_headers = ['Constant', 'Value', 'Uncertainty']

    details_table_data = []
    details_table_headers = ['Constant', 'Full name', 'Reference']

    for constant in flat_constants:
        name = constant.name
        value = eval(name)
        latex = value._repr_latex_()[1:-1]
        if isinstance(value, Constant):
            value_table_data.append(
                [name,
                 ':math:`{latex}`'.format(latex=latex),
                 value.uncertainty])
            details_table_data.append([name, value.name, value.reference])
        else:
            value_table_data.append(
                [name,
                 ':math:`{latex}`'.format(latex=latex),
                 'N/A'])

    if docfile.exists():
        check_git_unchanged(str(docfile), yes=yes)

    with docfile.open('w', encoding='utf-8') as f:
        f.write(DOC_TEMPLATE.format(
            value_table=tabulate(value_table_data, value_table_headers,
                                 tablefmt='rst'),
            details_table=tabulate(details_table_data, details_table_headers,
                                   tablefmt='rst')))


@task
def make(yes=False):
    make_module(yes)
    make_documentation(yes)
