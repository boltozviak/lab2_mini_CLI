import logging
import shutil
from os import PathLike
from pathlib import Path

logger = logging.getLogger(__name__)

def rm_command(
    filename_source: PathLike[str] | str,
    recursive: bool = False,
) -> None:

    source_file = Path(filename_source)
    current_path = Path.cwd().resolve()
    denied_paths = {Path.home().resolve(), Path("/").resolve(), Path.cwd().resolve()}


    if not source_file.exists():
        logger.error(f"Файл не существует: {source_file}")
        raise FileNotFoundError(f"Файл не существует: {source_file}")

    source_file = source_file.resolve()

    if source_file in denied_paths:
        logger.error(f"Попытка удалить важный файл: {source_file}")
        raise PermissionError(f"Вы не можете удалить этот файл: {source_file}")

    if current_path != source_file:
        if current_path.is_relative_to(source_file):
            logger.error(f"Попытка удалить важный файл: {source_file}")
            raise PermissionError(f"Вы не можете удалить этот файл: {source_file}")

    if source_file.is_dir() and not recursive:
        logger.error(f"Директория не пуста: {source_file}")
        raise IsADirectoryError(f"Директория не пуста: {source_file}")

    if source_file.is_dir():
        try:
            shutil.rmtree(source_file)
            logger.info(f"Удалена директория: {source_file}")
        except OSError:
            logger.error(f"Ошибка при удалении: {source_file}")
            raise
    else:
        try:
            source_file.unlink()
            logger.info(f"Удален файл: {source_file}")
        except OSError:
            logger.error(f"Ошибка при удалении файла: {source_file}")
            raise
