import logging
from os import PathLike
from pathlib import Path
import os

logger = logging.getLogger(__name__)

def cd_command(
    path: PathLike[str] | str
) -> None:
    path = Path(path)

    if str(path) == '~':
        os.chdir(os.path.expanduser('~'))
        logger.info(os.getcwd())
        return

    if not path.exists():
        logger.error(f"Path is not exists: {os.getcwd()}")
        raise FileNotFoundError(f"Path is not exists: {path}")

    if not path.is_dir():
        logger.error(f"Path is not a directory: {os.getcwd()}")
        raise NotADirectoryError(f"Path is not a directory: {path}")


    os.chdir(path)
    logger.info(os.getcwd())
    return
