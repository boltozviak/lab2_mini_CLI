import logging
# import os
import shutil
from os import PathLike
from pathlib import Path


logger = logging.getLogger(__name__)

def rm_command(
    filename_source: PathLike[str] | str,

    recursive: bool = False,
) -> None:

    source_file = Path(filename_source)

    if not source_file.exists():
        logger.error(f"Entered source file is not exists: {source_file}")
        raise FileNotFoundError(f"Entered source file is not exists: {source_file}")



    if recursive:
        shutil.rmtree(source_file)
    else:
        source_file.unlink()
