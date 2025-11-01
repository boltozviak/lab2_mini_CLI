import logging
from src.constants.file_mode import FileReadMode
from os import PathLike
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)

def cat_command(
    filename: PathLike[str] | str,
    mode: Literal[FileReadMode.string, FileReadMode.bytes] = FileReadMode.string
) -> str | bytes:

    path = Path(filename)

    if not path.exists():
        logger.error(f"Path is not exists: {path}")
        raise FileNotFoundError(f"Is not exists: {path}")

    if not path.is_file():
        logger.error(f"Path is not a file: {path}")
        raise IsADirectoryError(f"Is not a file: {path}")

    if mode == FileReadMode.string:
        return path.read_text()
    elif mode == FileReadMode.bytes:
        return path.read_bytes()
