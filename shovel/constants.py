# coding: utf-8
from __future__ import absolute_import, division, print_function

import re
from collections import OrderedDict, namedtuple
from itertools import chain
from pathlib import Path

from astropy import units as u  # flake8: noqa
from plumbum.cmd import git
from shovel import task

Constant = namedtuple('Constant', ['name', 'value'])
constant_re = re.compile('^(?P<name>[A-Z0-9_]+) = (?P<value>.+)')

TEMPLATE = """# coding: utf-8
from __future__ import absolute_import, division, print_function

from astropy import units as u

__all__ = (
{all_string}
)

{constant_string}
"""

INIT_TEMPLATE = """# coding: utf-8
from __future__ import absolute_import, division, print_function

{imports}

__all__ = (
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

{constants}
"""

DOC_CONSTANT_TEMPLATE = """.. py:data:: {name}

    :math:`{latex}`"""


def get_constants_from_data():
    # Mapping of module names to list of constants.
    constants = dict()

    sourcedir = Path('data', 'constants')
    for constantsfile in sourcedir.glob('*.txt'):
        modulename = constantsfile.stem
        constants[modulename] = []

        with constantsfile.open(encoding='utf-8') as f:
            for line in f:
                if line.lstrip().startswith('#'):
                    continue

                match = constant_re.match(line)
                if match:
                    # Append constant to list for this module name
                    d = match.groupdict()
                    constants[modulename].append(Constant(**d))
    return constants


@task
def make_module():
    """Use the templates defined above to create the astrodynamics.constants
    module.
    """
    constants = get_constants_from_data()
    init_imports = dict()
    pythondir = Path('astrodynamics', 'constants')

    for modulename, constants_list in constants.items():
        pythonfile = pythondir / '{}.py'.format(modulename)
        if pythonfile.exists():
            check_git_unchanged(str(pythonfile))

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
        check_git_unchanged(str(initfile))

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
def make_documentation():
    """Use the templates defined above to create the astrodynamics.constants
    documentation.
    """
    constants = get_constants_from_data()
    docfile = Path('doc', 'modules', 'constants.rst')

    # Sort constants by key
    constants = OrderedDict(sorted(constants.items(), key=lambda t: t[0]))

    # Hide individual modules from constants documentation
    flat_constants = chain.from_iterable(constants.values())

    doc_constants = []
    for constant in flat_constants:
        name = constant.name
        value = eval(constant.value)
        latex = value._repr_latex_()[1:-1]
        doc_constants.append(DOC_CONSTANT_TEMPLATE.format(name=name, latex=latex))
    constants_string = '\n\n'.join(doc_constants)

    if docfile.exists():
        check_git_unchanged(str(docfile))

    with docfile.open('w', encoding='utf-8') as f:
        f.write(DOC_TEMPLATE.format(constants=constants_string))


@task
def make():
    make_module()
    make_documentation()


def check_git_unchanged(filename):
    """Check git to avoid overwriting user changes."""
    if check_staged(filename):
        s = 'There are staged changes in {}, overwrite? [y/n] '.format(filename)
        if input(s) in ('y', 'yes'):
            return
        else:
            raise RuntimeError('There are staged changes in '
                               '{}, aborting.'.format(filename))
    if check_unstaged(filename):
        s = 'There are unstaged changes in {}, overwrite? [y/n] '.format(filename)
        if input(s) in ('y', 'yes'):
            return
        else:
            raise RuntimeError('There are unstaged changes in '
                               '{}, aborting.'.format(filename))


def check_staged(filename=None):
    """Check if there are 'changes to be committed' in the index."""
    retcode, _, stdout = git['diff-index', '--quiet', '--cached', 'HEAD',
                             filename].run(retcode=None)
    if retcode == 1:
        return True
    elif retcode == 0:
        return False
    else:
        raise RuntimeError(stdout)


def check_unstaged(filename):
    """Check if there are 'changes not staged for commit' in the working
    directory.
    """
    retcode, _, stdout = git['diff-files', '--quiet',
                             filename].run(retcode=None)
    if retcode == 1:
        return True
    elif retcode == 0:
        return False
    else:
        raise RuntimeError(stdout)
