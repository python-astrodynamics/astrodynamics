# coding: utf-8
"""astrodynamics

Usage:
    astrodynamics download_spk [options] <category> <kernel>

Options:
    --download-dir <dir>  Default: {default}

Example:
    astrodynamics download_spk planets de421
"""
from __future__ import absolute_import, division, print_function

import sys
from pathlib import Path

import requests
from appdirs import AppDirs
from docopt import docopt
from requests import HTTPError
from six.moves.urllib.parse import quote

from .progress import DownloadProgressBar, DownloadProgressSpinner
from .util import format_size

SPK_URL = "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/{category}{old}/{kernel}.bsp"
OLD_DIR = '/a_old_versions'

appdirs = AppDirs('astrodynamics')
spk_dir = Path(appdirs.user_data_dir, 'spk')

def main():
    args = docopt(__doc__.format(default=spk_dir))

    if args['download_spk']:
        categories = ['asteroids', 'comets', 'lagrange_point', 'planets',
                      'satellites', 'stations']
        category = args['<category>']
        kernel = args['<kernel>']
        if category not in categories:
            print(categories)

        if kernel.endswith('.bsp'):
            kernel = kernel[:-4]

        urls = [
            SPK_URL.format(category=category, old='', kernel=quote(kernel)),
            SPK_URL.format(category=category, old=OLD_DIR, kernel=quote(kernel))
            # SPK_URL.format(category=category, old='', kernel=quote(kernel + '_part-1'))
            # SPK_URL.format(category=category, old=OLD_DIR, kernel=quote(kernel + '_part-1'))
        ]

        # Get last path component for filename.
        filename = kernel.split('/')[-1] + '.bsp'

        download_dir = args['--download-dir']
        if download_dir:
            download_dir = Path(download_dir)

            if not download_dir.is_dir():
                sys.exit('Not a directory: {}'.format(download_dir))

            filepath = download_dir / filename
        else:
            try:
                spk_dir.mkdir(parents=True)
            except OSError:
                pass

            filepath = spk_dir / filename

        downloaded = False

        for url in urls:
            try:
                download_url(url, filepath)
            except HTTPError:
                continue
            else:
                downloaded = True
                break

        if not downloaded:
            print('Kernel not found in the following locations:')
            for url in urls:
                print('  {}'.format(url))
            sys.exit(1)


def download_url(url, filepath):
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

    with filepath.open('wb') as f:
        for chunk in progress_indicator(resp.iter_content(4096), 4096):
            f.write(chunk)
    print('Kernel downloaded to', filepath)

if __name__ == '__main__':
    main()
