from src.constants.file_mode import FileReadMode
from os import PathLike
from pathlib import Path
from typing import Literal

def cat_command(
    filename: PathLike[str] | str,
    mode: Literal[FileReadMode.string, FileReadMode.bytes] = FileReadMode.string) -> str | bytes:
    path = Path(filename)

    if mode == FileReadMode.string:
        return path.read_text()
    elif mode == FileReadMode.bytes:
        return path.read_bytes()
