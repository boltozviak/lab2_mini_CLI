import logging
import shutil
from os import PathLike
from pathlib import Path


logger = logging.getLogger(__name__)

def mv_command(
    filename_source: PathLike[str] | str,
    filename_destination: PathLike[str] | str,
) -> None:
    '''
    Перемещает/переименовывает файл или директорию

    Параметры:
    - filename_source - путь к файлу или директории, которые перемещаем/переименовываем
    - filename_destination - путь к файлу или директории, в которую перемещаем/переименовываем

    Исключения:
    - FileNotFoundError - не найдено/не существует исходный файл/директория
    '''

    src = Path(filename_source)
    dst = Path(filename_destination)

    if not src.exists():
        logger.error(f"Файл не существует: {src}")
        raise FileNotFoundError(f"Файл не существует: {src}")

    shutil.move(src, dst)
    logger.info(f"Успешно перемещено/переименовано: {src} в {dst}")
