# coding: utf-8
from __future__ import absolute_import, division, print_function

import os
import sys

import six

PY2 = six.PY2
PY3 = six.PY3
PY33 = sys.version_info >= (3, 3)

# windows detection, covers cpython and ironpython
WINDOWS = (sys.platform.startswith("win") or
           (sys.platform == 'cli' and os.name == 'nt'))
