***************
Getting started
***************

Working on ``astrodynamics`` requires the installation of some
development dependencies. These can be installed in a `virtualenv`_
using `pip`_ with the ``dev`` extras. You should install
``astrodynamics`` in ``editable`` mode.

For example:

.. code-block:: console

    $ # Create a virtualenv and activate it
    $ pip install --editable .[dev]

You are now ready to run the tests and build the documentation.

Running tests
=============

``astrodynamics`` unit tests are found in the ``astrodynamics/tests/``
directory and are designed to be run using `pytest`_. `pytest`_ will discover
the tests automatically, so all you have to do is:

.. code-block:: console

    $ py.test
    ...
    2 passed in 0.78 seconds

This runs the tests with the default Python interpreter.

You can also verify that the tests pass on other supported Python interpreters.
For this we use `tox`_, which will automatically create a `virtualenv`_ for
each supported Python version and run the tests. For example:

.. code-block:: console

    $ tox
    ...
     py27: commands succeeded
    ERROR:   py32: InterpreterNotFound: python3.3
    ERROR:   py33: InterpreterNotFound: python3.4
     py35: commands succeeded

You may not have all the required Python versions installed, in which case you
will see one or more ``InterpreterNotFound`` errors.

Building documentation
======================

``astrodynamics`` documentation is stored in the ``docs/`` directory. It is
written in `reStructured Text`_ and rendered using `Sphinx`_.

Use `shovel`_ to build the documentation. For example:

.. code-block:: console

    $ shovel docs.gen
    ...

The HTML documentation index can now be found at
``docs/_build/html/index.html``.

The documentation can be re-built as-you-edit like so:

.. code-block:: console

    $ shovel docs.watch
    ...

Adding/modifying constants
==========================

The constants package is created from source files stored in
``data/constants``. Each text file becomes a module in
``astrodynamics/constants``. Users import all constants directly from
:mod:`astrodynamics.constants`, but the modules are used for organisation.

After editing the data files, the constants can be updated with the following
commands:

.. code-block:: console

    $ shovel constants.make_module
    $ shovel constants.make_documentation
    ...
    # Or, to do both:
    $ shovel constants.make
    ...

.. _`pip`: https://pypi.python.org/pypi/pip
.. _`pytest`: https://pypi.python.org/pypi/pytest
.. _`reStructured Text`: http://sphinx-doc.org/rest.html
.. _`shovel`: https://github.com/seomoz/shovel#shovel
.. _`sphinx`: https://pypi.python.org/pypi/Sphinx
.. _`tox`: https://pypi.python.org/pypi/tox
.. _`virtualenv`: https://pypi.python.org/pypi/virtualenv

Import order
============

A consistent import order is used in ``astrodynamics``. The order is as
follows:

- ``from __future__ import ...``
- Standard library
- Third party modules
- Current project [#]_
- Local imports (``from . import ...``, ``from .module import ...``)

This order, and the formatting of the imports, can be enforced by running the
following commands:

.. code-block:: console

    $ shovel code.format_imports
    ...

.. [#] Although this order is enforced, within ``astrodynamics/``, use relative
   imports rather than absolute imports:

   .. code-block:: python

       # Bad
       from astrodynamics.bodies import ReferenceEllipsoid

       # Good
       from ..bodies import ReferenceEllipsoid
