# coding: utf-8
from __future__ import absolute_import, division, print_function

import re

from setuptools import setup, Command, find_packages


INIT_FILE = 'astrodynamics/__init__.py'
init_data = open(INIT_FILE).read()

metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", init_data))

VERSION = metadata['version']
LICENSE = metadata['license']
DESCRIPTION = metadata['description']
AUTHOR = metadata['author']
EMAIL = metadata['email']

requires = [
    'astropy>=1.0.5',
    'jplephem>=2.0',
    'networkx',
    'numpy',
    'represent>=1.4.0',
]

extras_require = {
    'dev': [
        'flake8',
        'flake8-coding',
        'flake8-future-import',
        'isort',
        'pep8-naming',
        'plumbum',
        'pytest>=2.7.3',
        'shovel',
        'sphinx',
        'sphinx_rtd_theme',
        'tox',
        'twine',
        'watchdog',
    ],
}


class PyTest(Command):
    """Allow 'python setup.py test' to run without first installing pytest"""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

setup(
    name='astrodynamics',
    version=VERSION,
    description=DESCRIPTION,
    long_description=open('README.rst').read(),
    author=AUTHOR,
    author_email=EMAIL,
    url='https://github.com/python-astrodynamics/astrodynamics',
    packages=find_packages(),
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    license=LICENSE,
    install_requires=requires,
    extras_require=extras_require)
