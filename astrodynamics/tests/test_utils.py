# coding: utf-8
from __future__ import absolute_import, division, print_function

import errno
import io
from pathlib import Path

import pytest
import responses
from astropy import units as u
from responses import GET

from astrodynamics.__main__ import main
from astrodynamics.utils import (
    SPK_DIR, SPK_OLD_URL, SPK_URL, DownloadProgressBar,
    DownloadProgressSpinner, InvalidCategoryError, KernelNotFoundError,
    SPKDownloadError, download_spk, format_size, suppress_file_exists_error,
    verify_unit)

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch


def test_verify_unit():
    # Implicit dimensionless values are allowed, test that Quantity is returned.
    assert verify_unit(0, u.one) == 0 * u.one
    assert verify_unit(0, '') == 0 * u.one

    # Test failure mode
    with pytest.raises(ValueError):
        verify_unit(0, u.meter)
    with pytest.raises(ValueError):
        verify_unit(0, 'm')

    # Quantity should be passed back if unit matches
    assert verify_unit(1 * u.meter, u.meter) == 1 * u.meter
    assert verify_unit(1 * u.meter, 'm') == 1 * u.meter


size_tests = (
    300, 3000, 3000000, 3000000000, 3000000000000, (300, True), (3000, True),
    (3000000, True), (300, False, True), (3000, False, True),
    (3000000, False, True), (1024, False, True), (10 ** 26 * 30, False, True),
    (10 ** 26 * 30, True), 10 ** 26 * 30, (3141592, False, False, '%.2f'),
    (3000, False, True, '%.3f'), (3000000000, False, True, '%.0f'),
    (10 ** 26 * 30, True, False, '%.3f'), 1
)

size_results = (
    '300 Bytes', '3.0 kB', '3.0 MB', '3.0 GB', '3.0 TB', '300 Bytes', '2.9 KiB',
    '2.9 MiB', '300B', '2.9K', '2.9M', '1.0K', '2481.5Y', '2481.5 YiB',
    '3000.0 YB', '3.14 MB', '2.930K', '3G', '2481.542 YiB', '1 Byte'
)


@pytest.mark.parametrize('args, string', zip(size_tests, size_results))
def test_format_size(args, string):
    if not isinstance(args, tuple):
        args = args,
    assert format_size(*args) == string

spk_data = [
    {'category': 'planets', 'kernel': 'de432s', 'old': False},
    {'category': 'planets', 'kernel': 'de410mini', 'old': True},
]


def test_suppress_file_exists_error(tmpdir):
    with suppress_file_exists_error():
        Path(str(tmpdir)).mkdir()

    with pytest.raises(OSError):
        with suppress_file_exists_error():
            raise OSError(errno.ENOENT, 'File not found')

    with suppress_file_exists_error():
        raise OSError(errno.EEXIST, 'File exists.')


@pytest.yield_fixture(scope='class', params=[False, True])
def mock_spk_url(request):
    # Mock requests so we don't hit the server
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        for data in spk_data:
            body = 'fake data for ' + data['kernel']

            # If the file is in the 'old' directory, mock a 404 response in the
            # top level directory.
            if data['old']:
                rsps.add(GET, SPK_URL.format(**data), status=404)
                url = SPK_OLD_URL
            else:

                url = SPK_URL
            if request.param:
                rsps.add(GET, url.format(**data), body=body)
            else:
                headers = {'Content-Length': str(len(body))}
                rsps.add(GET, url.format(**data), body=body, adding_headers=headers)

        rsps.add(GET, SPK_URL.format(category='planets', kernel='tatooine'),
                 status=404)
        rsps.add(GET, SPK_OLD_URL.format(category='planets', kernel='tatooine'),
                 status=404)

        yield rsps


@pytest.mark.usefixtures('mock_spk_url')
class TestDownloadSPK:
    def test_blah(self, tmpdir, capsys, mock_spk_url):
        rsps = mock_spk_url
        # Mock progress file attribute to prevent output to stderr (I had
        # trouble capturing)
        patch_bar = patch.object(DownloadProgressBar, 'file', io.StringIO())
        patch_spinner = patch.object(DownloadProgressSpinner, 'file', io.StringIO())
        with patch_bar, patch_spinner:
            for data in spk_data:
                download_spk(category=data['category'], kernel=data['kernel'],
                             download_dir=str(tmpdir))

                file = tmpdir.join(data['kernel'] + '.bsp')
                assert file.check()
                with file.open('r') as f:
                    assert f.read() == 'fake data for ' + data['kernel']

                stdout, _ = capsys.readouterr()
                lines = stdout.split('\n')
                assert lines[0].startswith('Downloading')

                headers = rsps.calls[-1].response.headers
                if 'content-length' in headers:
                    length = headers['content-length']
                    assert lines[0].endswith('{}.bsp ({})'.format(
                        data['kernel'], format_size(length)))
                else:
                    assert lines[0].endswith(data['kernel'] + '.bsp')

                assert lines[1].endswith(data['kernel'] + '.bsp')
                capsys.readouterr()

    def test_kernel_with_extension(self, tmpdir, capsys):
        """Test that kernel can still be downloaded if it has its extension."""
        with patch('astrodynamics.utils.web.download_file_with_progress',
                   autospec=True) as mock_download_file_with_progress:

            download_spk(category='planets', kernel='de432s.bsp',
                         download_dir=str(tmpdir))

            url = SPK_URL.format(category='planets', kernel='de432s')
            filepath = tmpdir.join('de432s.bsp')

            mock_download_file_with_progress.assert_called_once_with(
                url, str(filepath))

            mock_download_file_with_progress.reset_mock()
            assert not mock_download_file_with_progress.called
        capsys.readouterr()

    def test_invalid_category(self, tmpdir):
        with pytest.raises(InvalidCategoryError):
            download_spk(category='nonsense', kernel=spk_data[0]['kernel'],
                         download_dir=str(tmpdir))

    def test_kernel_not_found(self, tmpdir, capsys):
        with pytest.raises(KernelNotFoundError):
            download_spk(category='planets', kernel='tatooine',
                         download_dir=str(tmpdir))

    def test_default_dir(self, capsys):
        with patch('astrodynamics.utils.web.download_file_with_progress',
                   autospec=True) as mock:
            url = SPK_URL.format(category='planets', kernel='de432s')
            download_spk('planets', 'de432s')
            mock.assert_called_once_with(url, str(SPK_DIR / 'de432s.bsp'))
            capsys.readouterr()

    def test_main(self):
        patch_download_spk = patch(
            'astrodynamics.__main__.download_spk', autospec=True)
        with patch_download_spk as mock_download_spk:
            with patch('sys.argv', ['__main__.py', 'download_spk', 'planets',
                                    'de432s', '--download-dir=spam']):
                main()
            mock_download_spk.assert_called_with(
                category='planets', kernel='de432s', download_dir='spam')
            with patch('sys.argv', ['__main__.py', 'download_spk', 'planets', 'de432s']):
                main()
            mock_download_spk.assert_called_with(category='planets', kernel='de432s',
                                                 download_dir=None)

        mock_download_spk = Mock(side_effect=SPKDownloadError)
        with patch('astrodynamics.__main__.download_spk', mock_download_spk):
            with patch('sys.argv', ['__main__.py', 'download_spk', 'planets', 'eggs']):
                with pytest.raises(SystemExit):
                    main()
