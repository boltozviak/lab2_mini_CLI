import logging
import shutil
from os import PathLike
from pathlib import Path

from src.constants.denied_files import get_denied_paths

logger = logging.getLogger(__name__)

def rm_command(
    filename_source: PathLike[str] | str,
    recursive: bool = False,
) -> None:
    '''
    Удаляет файл или директорию

    Параметры:
    - filename_source - путь к файлу или директории, которые удаляем
    - recursive - удаляем директорию => ставим

    Исключения:
    - FileNotFoundError - не найдено/не существует исходный файл/директория
    - PermissionError - попытка удалить важный файл/директорию
    - IsADirectoryError - попытка удалить директорию не рекурсивно
    '''

    source_file = Path(filename_source)
    current_path = Path.cwd().resolve()
    denied_paths = get_denied_paths(current_path)


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
        shutil.rmtree(source_file)
        logger.info(f"Удалена директория: {source_file}")
    else:
        source_file.unlink()
        logger.info(f"Удален файл: {source_file}")
