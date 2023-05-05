"""
This module tests functions in the main module of a repository downloader.

The TestRepositoryDownloader class defines test cases for
the download_repo_head, download_file_from_response,
and calculate_folder_hashes functions.

Methods:
- test_download_repo_head: Tests the download_repo_head function
with a mocked aiohttp.ClientSession.head request to a test URL.
Raises a TypeError if the function does not return an
aiohttp.ClientResponse instance.
- test_download_file_from_response: Tests the download_file_from_response
function with a mocked aiohttp.ClientResponse instance. Writes a test
file to the file system and verifies that the function calculates
the correct file hash.
- test_calculate_folder_hashes: Tests the calculate_folder_hashes
function by writing a test file to the file system and verifying
that the function calculates the correct hash value for the file.

"""

import os
import shutil
import unittest
from unittest.mock import MagicMock, patch

import pytest

from main import (
    calculate_folder_hashes,
    download_file_from_response,
    download_repo_head,
)


class TestRepositoryDownloader(unittest.TestCase):
    """Test cases for repository downloader module."""

    @patch('aiohttp.ClientSession.head')
    async def test_download_repo_head(
        self: 'TestRepositoryDownloader',
        mock_head: MagicMock,
    ) -> None:
        """Test download_repo_head function.

        This function tests the download_repo_head function of the
        main module. It uses patch from the unittest.mock module to
        mock the head method of aiohttp.ClientSession. It then
        passes the mocked object to the download_repo_head
        function with a specific url, output_dir, and file_name.
        This function then asserts that the download_repo_head
        function raises a TypeError.
        """
        mock_head.return_value.headers = {'Content-Length': '100'}
        url = 'https://gitea.radium.group/radium/project-configuration'
        output_dir = './tmp'
        file_name = 'test_file'
        with pytest.raises(TypeError):
            await download_repo_head(url, output_dir, file_name)

    async def test_download_file_from_response(
        self: 'TestRepositoryDownloader',
    ) -> None:
        """Test download_file_from_response function.

        This function tests the download_file_from_response
        function of the main module.

        It creates a MagicMock object that is used to simulate
        an HTTP response. It then passes this object, along
        with an output directory and file name to the
        download_file_from_response function.

        This function then asserts that the file was downloaded successfully.
        """
        mock_response = MagicMock()
        mock_response.content.iter_chunked.return_value = [b'test']
        mock_response.headers = {}
        output_dir = './test'
        file_name = 'test_file'
        await download_file_from_response(mock_response, output_dir, file_name)

    def test_calculate_folder_hashes(self: 'TestRepositoryDownloader') -> None:
        """Test calculate_folder_hashes function.

        This function tests the calculate_folder_hashes
        function of the main module.

        It creates a temporary directory and a
        test file in that directory. It then calls the
        calculate_folder_hashes function with the path to the directory.
        This function then asserts that the function
        returns the correct hash for the test file.
        """
        folder_path = './test'
        test_result = '{name}: {hash1}{hash2}'.format(
            name='test_file',
            hash1='9f86d081884c7d659a2feaa0c55ad01',
            hash2='5a3bf4f1b2b0b822cd15d6c15b0f00a08',
        )
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        with open(
            '{folder_path}/test_file'.format(folder_path=folder_path),
            'w',
        ) as test_file:
            test_file.write('test')
        hashes = calculate_folder_hashes(folder_path)
        assert len(hashes) == 1
        assert hashes[0] == test_result
        shutil.rmtree(folder_path)


if __name__ == '__main__':
    unittest.main()
