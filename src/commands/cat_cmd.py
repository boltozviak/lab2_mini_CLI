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
        raise FileNotFoundError(f"Entered path is not exists: {path}")

    if not path.is_file():
        logger.error(f"Path is not a file: {path}")
        raise IsADirectoryError(f"Entered path is not a file: {path}")

    try:
        if mode == FileReadMode.string:
            content: str = path.read_text(encoding="utf-8")
            logger.info(f"Successfully read the file: {path}")
            return content
        elif mode == FileReadMode.bytes:
            content_bytes: bytes = path.read_bytes()
            logger.info(f"Successfully read the file: {path}")
            return content_bytes

    except UnicodeDecodeError as e:
        logger.error(f"{e}: {path}")
        raise ValueError(f"{e}: {path}")
