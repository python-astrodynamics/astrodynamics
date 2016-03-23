# coding: utf-8
from __future__ import absolute_import, division, print_function

import re
import sys
from collections import defaultdict

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand  # noqa


INIT_FILE = 'src/astrodynamics/__init__.py'
init_data = open(INIT_FILE).read()

metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", init_data))

VERSION = metadata['version']
LICENSE = metadata['license']
DESCRIPTION = metadata['description']
AUTHOR = metadata['author']
EMAIL = metadata['email']

requires = {
    'appdirs',
    'astropy>=1.0.5',
    'colorama',
    'docopt',
    'jplephem>=2.0',
    'networkx>=1.11',
    'numpy',
    'progress',
    'represent>=1.4.0',
    'requests',
    'scipy',
    'six',
}


def add_to_extras(extras_require, dest, source):
    """Add dependencies from `source` extra to `dest` extra, handling
    conditional dependencies.
    """
    for key, deps in list(extras_require.items()):
        extra, _, condition = key.partition(':')
        if extra == source:
            if condition:
                extras_require[dest + ':' + condition] |= deps
            else:
                extras_require[dest] |= deps

extras_require = defaultdict(set)

extras_require[':python_version<"3.4"'] = {'enum34', 'pathlib'}

extras_require['test'] = {
    'pytest>=2.7.3',
    'responses',
}

extras_require['test:python_version<"3.3"'] = {'mock'}

extras_require['dev'] = {
    'doc8',
    'flake8',
    'flake8-coding',
    'flake8-future-import',
    'isort',
    'pep8-naming',
    'plumbum>=1.6.0',
    'pyenchant',
    'pytest-cov',
    'shovel',
    'sphinx',
    'sphinx_rtd_theme',
    'sphinxcontrib-spelling',
    'tabulate',
    'tox',
    'twine',
    'watchdog',
}

add_to_extras(extras_require, 'dev', 'test')

extras_require = dict(extras_require)


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='astrodynamics',
    version=VERSION,
    description=DESCRIPTION,
    long_description=open('README.rst').read(),
    author=AUTHOR,
    author_email=EMAIL,
    url='https://github.com/python-astrodynamics/astrodynamics',
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    license=LICENSE,
    install_requires=requires,
    extras_require=extras_require,
    tests_require=extras_require['test'])
