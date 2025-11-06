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
    '''
    Выводит, что в файле написано

    Параметры:
    - filename - путь к файлу, который читаем
    - mode - читаем байты или строки

    Исключения:
    - FileNotFoundError - файл не существует
    - IsADirectoryError - файл не является файлом
    - UnicodeDecodeError - файл не является текстовым файлом
    '''

    path = Path(filename)

    if not path.exists():
        logger.error(f"Файл не существует: {path}")
        raise FileNotFoundError(f"Файл не существует: {path}")

    if not path.is_file():
        logger.error(f"Не файл: {path}")
        raise IsADirectoryError(f"Не файл: {path}")

    try:
        if mode == FileReadMode.string:
            content: str = path.read_text(encoding="utf-8")
            logger.info(f"Успешно прочитано: {path}")
            return content
        elif mode == FileReadMode.bytes:
            content_bytes: bytes = path.read_bytes()
            logger.info(f"Успешно прочитано: {path}")
            return content_bytes

    except UnicodeDecodeError as e:
        logger.error(f"Ошибка при чтении файла: {e}: {path}")
        raise ValueError(f"Ошибка при чтении файла: {e}: {path}")
