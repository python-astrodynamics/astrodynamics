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

from docopt import docopt

from .utils import SPK_DIR, SPKDownloadError, download_spk


def main():
    args = docopt(__doc__.format(default=SPK_DIR))

    if args['download_spk']:
        category = args['<category>']
        kernel = args['<kernel>']
        download_dir = args['--download-dir']
        try:
            download_spk(category=category, kernel=kernel, download_dir=download_dir)
        except SPKDownloadError as e:
            sys.exit(e)


if __name__ == '__main__':
    main()
