"""
Repository downloader.

This module contains a function for
downloading and hashing HEAD content of repository by
https://gitea.radium.group/radium/project-configuration.
"""
import asyncio
import hashlib
import logging
import os
import shutil
from typing import List

import aiohttp

logging.basicConfig(
    level=logging.INFO,
)


def calculate_folder_hashes(folder_path: str) -> List[str]:
    """Calculate the SHA256 hash of every file in a folder.

    Args:
        folder_path (str):
            The path to the folder to calculate hashes for.

    Returns:
        A list of strings, where each string is in the format
        "<filename>: <sha256 hash>".
    """
    hashes = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as dir_file:
                file_hash = hashlib.sha256(dir_file.read()).hexdigest()
                hashes.append('{file_name}: {file_hash}'.format(
                    file_name=file_name,
                    file_hash=file_hash,
                ))
    return hashes


async def download_repo_head(
    url: str, output_dir: str, file_name: str,
) -> None:
    """Download the HEAD content of a repository given its URL.

    Saves the HEAD content to a file in the specified output directory with the
    specified name. If the 'Content-Length' header is not present in the
    response, nothing is downloaded.

    Args:
        url (str):
            The URL of the repository.
        output_dir (str):
            The directory to save the downloaded file to.
        file_name (str):
            The name to give the downloaded file.

    Raises:
        Any exceptions that can be raised by aiohttp.ClientSession.get().
    """
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as head_response:
            if 'Content-Length' in head_response.headers:
                return
            await download_file_from_response(
                response=await session.get(url),
                output_dir=output_dir,
                file_name='{file_s}_{file_e}'.format(
                    file_s=url.split('/')[-1],
                    file_e=file_name,
                ),
            )


async def download_file_from_response(
    response: aiohttp.ClientResponse,
    output_dir: str,
    file_name: str,
) -> None:
    """Download the file from an HTTP response and save it to the directory.

    Args:
        response (aiohttp.ClientResponse):
            An object representing the HTTP response to download.
        output_dir (str):
            The directory to save the downloaded file to.
        file_name (str):
            The name to give the downloaded file.

    Raises:
        OSError: If there is an error creating or writing to the output file.
    """
    file_path = os.path.join(output_dir, file_name)
    try:
        with open(file_path, 'wb') as output_file:
            async for chunk in response.content.iter_chunked(1024):
                output_file.write(chunk)
    except OSError as exception:
        raise OSError('Error creating or writing to outfile') from exception


async def main() -> None:
    """Download HEAD content, save and calculate SHA256 hash for each file.

    The repository URL is hard-coded to
    'https://gitea.radium.group/radium/project-configuration', and the
    output directory is also hard-coded to './tmp'. Three files
    will be downloaded, with sequential file indices starting at 0.

    Raises:
        Any exceptions raised by called functions will be propagated.
    """
    tmp_dir = 'tmp'
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)

    await asyncio.gather(*[
        download_repo_head(
            'https://gitea.radium.group/radium/project-configuration',
            './tmp',
            str(file_index),
        ) for file_index in range(1, 4)
    ])

    for hash_string in calculate_folder_hashes(tmp_dir):
        logging.info(hash_string)
    shutil.rmtree(tmp_dir)


if __name__ == '__main__':
    asyncio.run(main())
