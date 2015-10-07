# coding: utf-8
from __future__ import absolute_import, division, print_function

from pathlib import Path

import requests
from appdirs import AppDirs
from requests import HTTPError
from six.moves.urllib.parse import quote

from ..compat.contextlib import suppress
from .helper import format_size, prefix, suppress_file_exists_error
from .progress import DownloadProgressBar, DownloadProgressSpinner

SPK_URL = ("http://naif.jpl.nasa.gov/pub/naif/generic_kernels/"
           "spk/{category}/{kernel}.bsp")
SPK_OLD_URL = ("http://naif.jpl.nasa.gov/pub/naif/generic_kernels/"
               "spk/{category}/a_old_versions/{kernel}.bsp")

appdirs = AppDirs('astrodynamics')
SPK_DIR = Path(appdirs.user_data_dir, 'spk')


class SPKDownloadError(Exception):
    """Raised when SPK download fails."""


class KernelNotFoundError(SPKDownloadError):
    """Raised when SPK kernel not found on website."""


class InvalidCategoryError(SPKDownloadError):
    """Raised for invalid category."""


def download_spk(category, kernel, download_dir=None):
    """Download generic kernel SPK files from
    http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/

    Parameters:
        category: asteroids, comets, lagrange_point, planets, satellites, or stations
        kernel: Kernel name, e.g. `de430` will download `de430.bsp`
        download_dir: Directory to download file to. By default, this is to a
                      platform-dependent astrodynamics directory: :py:const:`SPK_DIR`
    """
    valid_categories = ['asteroids', 'comets', 'lagrange_point', 'planets',
                        'satellites', 'stations']

    if category not in valid_categories:
        s = 'Invalid category. Valid categories: {}'
        raise InvalidCategoryError(s.format(', '.join(valid_categories)))

    # We only wanted the name, strip the extension.
    if kernel.endswith('.bsp'):
        kernel = kernel[:-4]

    urls = [
        SPK_URL.format(category=category, kernel=quote(kernel)),
        SPK_OLD_URL.format(category=category, kernel=quote(kernel))
    ]

    # Get last path component for filename.
    # e.g. 'de423_for_mercury_and_venus/de423' => 'de423.bsp'
    #      'de421' => 'de421.bsp'
    filename = kernel.split('/')[-1] + '.bsp'

    if download_dir:
        download_dir = Path(download_dir)

        filepath = download_dir / filename
    else:
        with suppress_file_exists_error():
            SPK_DIR.mkdir(parents=True)

        filepath = SPK_DIR / filename

    downloaded = False

    for url in urls:
        with suppress(HTTPError):
            download_file_with_progress(url, str(filepath))
            print('Kernel downloaded to', filepath)
            downloaded = True
            break

    if not downloaded:
        s = 'Kernel not found in the following locations:\n{}'
        raise KernelNotFoundError(s.format('\n'.join(prefix('  ', urls))))


def download_file_with_progress(url, filepath):
    """Download URL to file with progress bar or spinner printed to stderr.

    Parameters:
        url (str): URL to download.
        filepath (str): File path URL will be saved to.
    """
    resp = requests.get(url, stream=True)
    resp.raise_for_status()

    try:
        total_length = int(resp.headers['content-length'])
    except (ValueError, KeyError, TypeError):
        total_length = 0

    if total_length:
        print('Downloading {} ({})'.format(url, format_size(total_length)))
        progress_indicator = DownloadProgressBar(max=total_length).iter
    else:
        print('Downloading {}'.format(url))
        progress_indicator = DownloadProgressSpinner().iter

    with open(filepath, 'wb') as f:
        for chunk in progress_indicator(resp.iter_content(4096), 4096):
            f.write(chunk)
