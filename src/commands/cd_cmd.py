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

    path = Path(path)
    const_path = Path.cwd()

    if str(path) == '~':
        os.chdir(os.path.expanduser('~'))
        logger.info(f"Сменили: '{const_path}' на: '{Path.cwd()}'")
        return

    if not path.exists():
        logger.error(f"Файл не существует: {path}")
        raise FileNotFoundError(f"Файл не существует: {path}")

    if not path.is_dir():
        logger.error(f"Не директория: {path}")
        raise NotADirectoryError(f"Не директория: {path}")

    os.chdir(path)
    logger.info(f"Сменили директорию с: '{const_path}' на: '{Path.cwd()}'")
    return
