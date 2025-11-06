import shutil
import zipfile
import tarfile
import logging
from os import PathLike
from pathlib import Path

logger = logging.getLogger(__name__)

def zip_command(
    src: PathLike[str] | str,
    archive_name: PathLike[str] | str,
) -> None:
    src = Path(src)
    archive_name = Path(archive_name)

    if not archive_name.suffix == '.zip':
        logger.error(f"Не zip архив: {archive_name}")
        raise ValueError(f"Не zip архив: {archive_name}")

    if archive_name.exists():
        logger.error(f"Архив уже существует: {archive_name}")
        raise FileExistsError(f"Архив уже существует: {archive_name}")

    if not src.exists():
        logger.error(f"Директория не существует: {src}")
        raise FileNotFoundError(f"Директория не существует: {src}")

    if not src.is_dir():
        logger.error(f"Не директория: {src}")
        raise NotADirectoryError(f"Не директория: {src}")

    try:
        base_name = str(archive_name.with_suffix(''))
        shutil.make_archive(base_name, 'zip', str(src.parent), src.name)
        logger.info(f"Успешно создан zip-архив: {archive_name}")
    except OSError as e:
        logger.error(f"Ошибка при создании zip-архива: {e}: {src} to {archive_name}")
        raise


def unzip_command(
    archive_name: PathLike[str] | str,

) -> None:
    archive_name = Path(archive_name)
    destination = Path.cwd()

    if not archive_name.exists():
        logger.error(f"Архив не существует: {archive_name}")
        raise FileNotFoundError(f"Архив не существует: {archive_name}")

    if not zipfile.is_zipfile(archive_name):
        logger.error(f"Не zip архив: {archive_name}")
        raise ValueError(f"Не zip архив: {archive_name}")

    try:
        shutil.unpack_archive(str(archive_name), str(destination), 'zip')
        logger.info(f"Успешно распакован zip-архив: {archive_name} в {destination}")
    except OSError as e:
        logger.error(f"Ошибка при распаковке zip-архива: {e}: {archive_name} в {destination}")
        raise

def tar_command(
    src: PathLike[str] | str,
    archive_name: PathLike[str] | str,
) -> None:
    src = Path(src)
    archive_name = Path(archive_name)

    if archive_name.suffixes != ['.tar', '.gz']:
        logger.error(f"Не tar.gz архив: {archive_name}")
        raise ValueError(f"Не tar.gz архив: {archive_name}")

    if archive_name.exists():
        logger.error(f"Архив уже существует: {archive_name}")
        raise FileExistsError(f"Архив уже существует: {archive_name}")

    if not src.exists():
        logger.error(f"Директория не существует: {src}")
        raise FileNotFoundError(f"Директория не существует: {src}")

    if not src.is_dir():
        logger.error(f"Не директория: {src}")
        raise NotADirectoryError(f"Не директория: {src}")

    try:
        with tarfile.open(archive_name, 'w:gz') as tarf:
            tarf.add(str(src), arcname=src.name, recursive=True)
            logger.info(f"Успешно создан tar.gz-архив: {archive_name}")
    except OSError as e:
        logger.error(f"Ошибка при создании tar.gz-архива: {e}: {src} в {archive_name}")
        raise

def untar_command(
    archive_name: PathLike[str] | str,
) -> None:
    archive_name = Path(archive_name)
    destination = Path.cwd()

    if not archive_name.exists():
        logger.error(f"Архив не существует: {archive_name}")
        raise FileNotFoundError(f"Архив не существует: {archive_name}")

    if not tarfile.is_tarfile(archive_name):
        logger.error(f"Не tar.gz архив: {archive_name}")
        raise ValueError(f"Не tar.gz архив: {archive_name}")

    try:
        with tarfile.open(archive_name, 'r:gz') as tarf:
            tarf.extractall(destination)
            logger.info(f"Успешно распакован tar.gz-архив: {archive_name} в {destination}")
    except OSError as e:
        logger.error(f"Ошибка при распаковке tar.gz-архива: {e}: {archive_name} в {destination}")
        raise
