# Python Async Download Script
This is a project developed as a test task by a starter Python developer. The script is designed to download the contents of the HEAD repository from https://gitea.radium.group/radium/project-configuration asynchronously into a temporary folder, and then calculate the sha256 hashes of each downloaded file.

The script uses asyncio to handle the asynchronous download of the repository contents, and utilizes the aiohttp library to interact with the repository API. The downloaded files are saved to a temporary folder, and the sha256 hash of each file is calculated using the hashlib library.

The code is written to adhere to the wemake-python-styleguide, and is linted using the nitpick configuration found at https://gitea.radium.group/radium/project-configuration. Additionally, the code is fully tested, with 100% test coverage, using the unittest library.

To run the script, simply clone the repository and run the main.py file.

# Тестовое задание

Напишите скрипт, асинхронно, в 3 одновременных задачи, скачивающий содержимое HEAD репозитория https://gitea.radium.group/radium/project-configuration во временную папку.
После выполнения всех асинхронных задач скрипт должен посчитать sha256 хэши от каждого файла.
Код должен проходить без замечаний проверку линтером wemake-python-styleguide. Конфигурация nitpick - https://gitea.radium.group/radium/project-configuration
Обязательно 100% покрытие тестами

## Installation
To download and run the script, follow these steps:
1. Clone the repository using Git:
```shell
git clone https://github.com/your_username/repository-downloader.git
```
2. Navigate to the cloned directory:
```shell
cd repository-downloader
```
3. Install the required dependencies using Poetry:
```shell
poetry install
```
4. Run the main script:
```shell
poetry run main.py
```

## Testing
This repository has unit tests written with Pytest, which can be run with Poetry:
```shell
poetry run pytest
```
The test coverage can also be checked using coverage:
```shell
poetry run coverage run -m pytest
poetry run coverage report -m
```
