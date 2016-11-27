# coding: utf-8
from __future__ import absolute_import, division, print_function

try:
    from contextlib import suppress
except ImportError:
    suppress = None


class _SuppressExceptions:
    """Helper for suppress."""
    def __init__(self, *exceptions):
        self._exceptions = exceptions

    def __enter__(self):
        pass

    def __exit__(self, exctype, excinst, exctb):
        # Unlike isinstance and issubclass, exception handling only
        # looks at the concrete type heirarchy (ignoring the instance
        # and subclass checking hooks). However, all exceptions are
        # also required to be concrete subclasses of BaseException, so
        # if there's a discrepancy in behaviour, we currently consider it
        # the fault of the strange way the exception has been defined rather
        # than the fact that issubclass can be customised while the
        # exception checks can't.
        # See http://bugs.python.org/issue12029 for more details
        return exctype is not None and issubclass(exctype, self._exceptions)


# Use a wrapper function since we don't care about supporting inheritance
# and a function gives much cleaner output in help()
def _suppress(*exceptions):
    """Context manager to suppress specified exceptions
    After the exception is suppressed, execution proceeds with the next
    statement following the with statement.
         with suppress(FileNotFoundError):
             os.remove(somefile)
         # Execution still resumes here if the file was already removed
    """
    return _SuppressExceptions(*exceptions)


suppress = suppress or _suppress
