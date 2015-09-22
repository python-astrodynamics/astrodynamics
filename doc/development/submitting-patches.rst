******************
Submitting patches
******************

* Always make a new branch for your work.
* Patches should be small to facilitate easier review. `Studies have shown`_
  that review quality falls off as patch size grows. Sometimes this will result
  in many small PRs to land a single large feature.
* Ideally, larger changes should be discussed in a GitHub issue before submission.
* New features and significant bug fixes should be documented in the
  :doc:`/changelog`.
* You must have legal permission to distribute any code you contribute to
  ``astrodynamics``, and it must be available under the MIT License.

Code
====

When in doubt, refer to :pep:`8` for Python code. You can check if your code
meets our automated requirements by running ``flake8`` against it. If you've
installed the development requirements this will automatically use our
configuration.

`Write comments as complete sentences.`_

Class names which contain acronyms or initialisms should always be
capitalized. A class should be named ``HTTPClient``, not ``HttpClient``.

Every Python code file must contain the following lines, both of which
are enforced by ``flake8``:

.. code-block:: python

    # coding: utf-8
    from __future__ import absolute_import, division, print_function

Tests
=====

All code changes must be accompanied by unit tests.

Documentation
=============

Docstrings should be written for `Sphinx`_. `Readability counts`_, so Google-style
docstrings as parsed by the Sphinx `Napoleon`_ extension are encouraged.

For example::

    class DirEntry(object):
        """The is the template class for the cache objects.

        Args:
            path (str): The path of the file to wrap
            field_storage (FileStorage): The :class:`FileStorage` instance to wrap
            temporary (bool): Whether or not to delete the file when the File
               instance is destructed

        Returns:
            BufferedFileStorage: A buffered writable file descriptor
        """

So, specifically:

* Always use three double quotes.
* Unless the entire docstring fits on a line, place the closing quotes on a line by themselves. 
* No blank line at the end.
* Use Google-style docstrings for the Sphinx `Napoleon`_ extension.


.. _`Write comments as complete sentences.`: http://nedbatchelder.com/blog/201401/comments_should_be_sentences.html
.. _`Studies have shown`: https://smartbear.com/smartbear/media/pdfs/wp-cc-11-best-practices-of-peer-code-review.pdf
.. _`sphinx`: https://pypi.python.org/pypi/Sphinx
.. _`readability counts`: https://www.python.org/dev/peps/pep-0020/
.. _`napoleon`: http://sphinxcontrib-napoleon.readthedocs.org/en/latest/index.html
