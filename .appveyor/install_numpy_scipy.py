# coding: utf-8
from __future__ import absolute_import, division, print_function

import os
import pip
import struct
import ssl
import sys

from six.moves.urllib.request import urlretrieve


def download_wheel(name, version):
    base_url = os.getenv('WHEEL_URL')
    if base_url is None:
        raise ValueError('WHEEL_URL environment variable is missing.')

    py = 'cp{0[0]}{0[1]}'.format(sys.version_info)
    if py not in {'cp27', 'cp34', 'cp35'}:
        print('{} wheel not available for {}'.format(name, py))
        return None

    bits = struct.calcsize('P') * 8
    if bits == 32:
        arch = 'win32'
    elif bits == 64:
        arch = 'win_amd64'
    else:
        raise ValueError("Couldn't determine 32/64 bits.")

    filename = '{}-{}-{}-none-{}.whl'.format(name, version, py, arch)

    directory = 'astrodynamics-wheels'
    try:
        os.mkdir(directory)
    except OSError:
        pass

    filepath = os.path.join(directory, filename)
    url = base_url + filename

    urlretrieve(url, filepath)
    return filepath


def install_numpy():
    filepath = download_wheel('numpy', '1.10.4+mkl')
    if filepath:
        pip.main(['install', filepath])
    else:
        pip.main(['install', 'numpy'])


def install_scipy():
    filepath = download_wheel('scipy', '0.17.0')
    if filepath:
        pip.main(['install', filepath])
    else:
        pip.main(['install', 'scipy'])

if __name__ == '__main__':
    # Disable SSL. Shouldn't do this ever. This is just a script.
    ssl._create_default_https_context = ssl._create_unverified_context
    install_numpy()
    install_scipy()
