import logging
import shutil
from os import PathLike
from pathlib import Path


logger = logging.getLogger(__name__)

def mv_command(
    filename_source: PathLike[str] | str,
    filename_destination: PathLike[str] | str,
) -> None:

    src = Path(filename_source)
    dst = Path(filename_destination)

    if not src.exists():
        logger.error(f"Entered source file is not exists: {src}")
        raise FileNotFoundError(f"Entered source file is not exists: {src}")

    try:
        shutil.move(src, dst)
        logger.info(f"Successfully moved the file: {src} to {dst}")
    except OSError as e:
        logger.error(f"{e}: {src} to {dst}")
        raise
