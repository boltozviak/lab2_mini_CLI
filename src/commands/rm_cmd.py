import logging
import shutil
from os import PathLike
from pathlib import Path

logger = logging.getLogger(__name__)

def rm_command(
    filename_source: PathLike[str] | str,
    recursive: bool = False,
) -> None:

    source_file = Path(filename_source)
    current_path = Path.cwd().resolve()
    denied_paths = {Path.home().resolve(), Path("/").resolve(), Path.cwd().resolve()}


    if not source_file.exists():
        logger.error(f"Entered source file is not exists: {source_file}")
        raise FileNotFoundError(f"Entered source file is not exists: {source_file}")

    source_file = source_file.resolve()

    if source_file in denied_paths:
        logger.error(f"Try to remove important file: {source_file}")
        raise PermissionError(f"You can't remove this file: {source_file}")

    if current_path != source_file:
        if current_path.is_relative_to(source_file):
            logger.error(f"Try to remove important file: {source_file}")
            raise PermissionError(f"You can't remove this file: {source_file}")

    if source_file.is_dir() and not recursive:
        logger.error(f"Entered source is not a file: {source_file}")
        raise IsADirectoryError(f"Entered source is not a file: {source_file}")

    if source_file.is_dir():
        try:
            shutil.rmtree(source_file)
            logger.info(f"Removed directory: {source_file}")
        except OSError:
            logger.error(f"Failed to remove: {source_file}")
            raise
    else:
        try:
            source_file.unlink()
            logger.info(f"Removed file: {source_file}")
        except OSError:
            logger.error(f"Failed to remove file: {source_file}")
            raise
