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
        logger.error(f"Entered archive file is not a zip file: {archive_name}")
        raise ValueError(f"Entered archive file is not a zip file: {archive_name}")

    if archive_name.exists():
        logger.error(f"Archive file already exists: {archive_name}")
        raise FileExistsError(f"Archive file already exists: {archive_name}")

    if not src.exists():
        logger.error(f"Source file is not exists: {src}")
        raise FileNotFoundError(f"Source file is not exists: {src}")

    if not src.is_dir():
        logger.error(f"Source file is not a dir: {src}")
        raise NotADirectoryError(f"Source file is not a dir: {src}")

    try:
        base_name = str(archive_name.with_suffix(''))
        shutil.make_archive(base_name, 'zip', str(src.parent), src.name)
        logger.info(f"Successfully created archive: {archive_name}")
    except OSError as e:
        logger.error(f"Error creating archive: {e}: {src} to {archive_name}")
        raise


def unzip_command(
    archive_name: PathLike[str] | str,

) -> None:
    archive_name = Path(archive_name)
    destination = Path.cwd()

    if not archive_name.exists():
        logger.error(f"Archive file is not exists: {archive_name}")
        raise FileNotFoundError(f"Archive file is not exists: {archive_name}")

    if not zipfile.is_zipfile(archive_name):
        logger.error(f"File is not a zip file: {archive_name}")
        raise ValueError(f"File is not a zip file: {archive_name}")

    try:
        shutil.unpack_archive(str(archive_name), str(destination), 'zip')
        logger.info(f"Successfully extracted archive: {archive_name} to {destination}")
    except OSError as e:
        logger.error(f"Error extracting archive: {e}: {archive_name} to {destination}")
        raise

def tar_command(
    src: PathLike[str] | str,
    archive_name: PathLike[str] | str,
) -> None:
    src = Path(src)
    archive_name = Path(archive_name)

    if archive_name.suffixes != ['.tar', '.gz']:
        logger.error(f"Entered archive file is not a tar.gz file: {archive_name}")
        raise ValueError(f"Entered archive file is not a tar.gz file: {archive_name}")

    if archive_name.exists():
        logger.error(f"Archive file already exists: {archive_name}")
        raise FileExistsError(f"Archive file already exists: {archive_name}")

    if not src.exists():
        logger.error(f"Source file is not exists: {src}")
        raise FileNotFoundError(f"Source file is not exists: {src}")

    if not src.is_dir():
        logger.error(f"Source file is not a dir: {src}")
        raise NotADirectoryError(f"Source file is not a dir: {src}")

    try:
        with tarfile.open(archive_name, 'w:gz') as tarf:
            tarf.add(str(src), arcname=src.name, recursive=True)
            logger.info(f"Successfully created archive: {archive_name}")
    except OSError as e:
        logger.error(f"Error creating archive: {e}: {src} to {archive_name}")
        raise

def untar_command(
    archive_name: PathLike[str] | str,
) -> None:
    archive_name = Path(archive_name)
    destination = Path.cwd()

    if not archive_name.exists():
        logger.error(f"Archive file is not exists: {archive_name}")
        raise FileNotFoundError(f"Archive file is not exists: {archive_name}")

    if not tarfile.is_tarfile(archive_name):
        logger.error(f"File is not a tar.gz file: {archive_name}")
        raise ValueError(f"File is not a tar.gz file: {archive_name}")

    try:
        with tarfile.open(archive_name, 'r:gz') as tarf:
            tarf.extractall(destination)
            logger.info(f"Successfully extracted archive: {archive_name} to {destination}")
    except OSError as e:
        logger.error(f"Error extracting archive: {e}: {archive_name} to {destination}")
        raise
