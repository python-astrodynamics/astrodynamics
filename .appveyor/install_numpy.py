# coding: utf-8
from __future__ import absolute_import, division, print_function

import os
import pip
import struct
import ssl
import sys

from six.moves.urllib.request import urlretrieve


def download_numpy_wheel():
    base_url = os.getenv('NUMPY_URL')
    if base_url is None:
        raise ValueError('NUMPY_URL environment variable is missing.')

    version = '1.10.4+mkl'
    py = 'cp{0[0]}{0[1]}'.format(sys.version_info)
    if py not in {'cp27', 'cp34', 'cp35'}:
        print('NumPy wheel not available for {}'.format(py))
        return None

    bits = struct.calcsize('P') * 8
    if bits == 32:
        arch = 'win32'
    elif bits == 64:
        arch = 'win_amd64'
    else:
        raise ValueError("Couldn't determine 32/64 bits.")

    filename = 'numpy-{}-{}-none-{}.whl'.format(version, py, arch)

    directory = 'astrodynamics-numpy-wheels'
    os.mkdir(directory)

    filepath = os.path.join(directory, filename)
    url = base_url + filename

    # Disable SSL. Shouldn't do this ever. This is just a script.
    ssl._create_default_https_context = ssl._create_unverified_context
    urlretrieve(url, filepath)
    return filepath


def install_numpy():
    filepath = download_numpy_wheel()
    if filepath:
        pip.main(['install', filepath])
    else:
        pip.main(['install', 'numpy'])


if __name__ == '__main__':
    install_numpy()
