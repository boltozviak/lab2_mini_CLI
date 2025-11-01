import logging
# import os
import shutil
from os import PathLike
from pathlib import Path


logger = logging.getLogger(__name__)

def cp_command(
    filename_source: PathLike[str] | str,
    filename_destination: PathLike[str] | str,
    recursive: bool = False,
) -> None:

    source_file = Path(filename_source)
    destination_dir = Path(filename_destination)

    if not source_file.exists():
        logger.error(f"Entered source file is not exists: {source_file}")
        raise FileNotFoundError(f"Entered source file is not exists: {source_file}")



    if recursive:
        shutil.copytree(source_file, destination_dir)
    else:
        shutil.copy(source_file, destination_dir)
