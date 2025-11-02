import logging
import shutil
from os import PathLike
from pathlib import Path


logger = logging.getLogger(__name__)

def cp_command(
    filename_source: PathLike[str] | str,
    filename_destination: PathLike[str] | str,
    recursive: bool = False,
) -> None:

    src = Path(filename_source)
    dst = Path(filename_destination)

    if not src.exists():
        logger.error(f"Entered source file is not exists: {src}")
        raise FileNotFoundError(f"Source file {src} not found or is not a file.")


    try:
        if src.is_file():
            shutil.copy(src, dst)
            logger.info(f"Successfully copied the file: {src} to {dst}")
        elif src.is_dir():
            if not recursive:
                logger.error(f"Source is a directory - use -r: {src}")
                raise IsADirectoryError("Source is a directory - use -r")
            else:
                if dst.exists() and dst.is_file():
                    logger.error(f"Destination is a file: {dst}")
                    raise IsADirectoryError(f"Destination is a file: {dst}")
                elif dst.exists() and dst.is_dir():
                    destination_path = dst / src.name
                    shutil.copytree(src, destination_path)
                    logger.info(f"Successfully copied the directory: {src} to {dst}")
                else:
                    shutil.copytree(src, dst)
                    logger.info(f"Successfully copied the directory: {src} to {dst}")
    except shutil.Error as e:
        logger.error(f"Error copying {src} to {dst}: {e}")
        raise
    except OSError as e:
        logger.error(f"Error copying {src} to {dst}: {e}")
        raise
