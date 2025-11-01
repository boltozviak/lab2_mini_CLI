import logging
# import os
import shutil
from os import PathLike
from pathlib import Path


logger = logging.getLogger(__name__)

def mv_command(
    filename_source: PathLike[str] | str,
    filename_destination: PathLike[str] | str,
) -> None:

    source_file = Path(filename_source)
    destination_file = Path(filename_destination)

    if not source_file.exists():
        logger.error(f"Entered source file is not exists: {source_file}")
        raise FileNotFoundError(f"Entered source file is not exists: {source_file}")

    shutil.move(source_file, destination_file)
