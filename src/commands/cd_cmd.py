import logging
from os import PathLike
from pathlib import Path
import os

logger = logging.getLogger(__name__)

def cd_command(
    path: PathLike[str] | str
) -> None:
    path = Path(path)
    const_path = Path.cwd()

    if str(path) == '~':
        os.chdir(os.path.expanduser('~'))
        logger.info(f"Changed directory from: '{const_path}' to: '{Path.cwd()}'")
        return

    if not path.exists():
        logger.error(f"Path is not exists: {Path.cwd()}")
        raise FileNotFoundError(f"Path is not exists: {Path.cwd()}")

    if not path.is_dir():
        logger.error(f"Path is not a directory: {Path.cwd()}")
        raise NotADirectoryError(f"Path is not a directory: {Path.cwd()}")

    os.chdir(path)
    logger.info(f"Changed directory from: '{const_path}' to: '{Path.cwd()}'")
    return
