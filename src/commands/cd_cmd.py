import logging
from os import PathLike
from pathlib import Path
import os

logger = logging.getLogger(__name__)

def cd_command(
    path: PathLike[str] | str
) -> None:
    '''
    Меняет текущую директорию на указанную

    Параметры:
    - path - путь к директории, куда подрываемся

    Исключения:
    - FileNotFoundError - директория не найдена/не существует
    - NotADirectoryError - путь ведёт не в директорию
    '''

    src_path = Path.cwd()

    if str(path) == '~':
        dest_path = Path(os.path.expanduser('~'))
    else:
        dest_path = Path(path)

    if not dest_path.exists():
        logger.error(f"Файл не существует: {dest_path}")
        raise FileNotFoundError(f"Файл не существует: {dest_path}")

    if not dest_path.is_dir():
        logger.error(f"Не директория: {dest_path}")
        raise NotADirectoryError(f"Не директория: {dest_path}")

    os.chdir(dest_path)
    logger.info(f"Сменили директорию с: '{src_path}' на: '{Path.cwd()}'")
