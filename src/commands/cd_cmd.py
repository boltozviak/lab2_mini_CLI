import logging
from os import PathLike
from pathlib import Path
import os

logger = logging.getLogger(__name__)

def cd_command(
    path: PathLike[str] | str
) -> None:
    path = Path(path)
    const_path = Path.cwd()

    if str(path) == '~':
        os.chdir(os.path.expanduser('~'))
        logger.info(f"Сменили: '{const_path}' на: '{Path.cwd()}'")
        return

    if not path.exists():
        logger.error(f"Файл не существует: {Path.cwd()}")
        raise FileNotFoundError(f"Файл не существует: {Path.cwd()}")

    if not path.is_dir():
        logger.error(f"Не директория: {Path.cwd()}")
        raise NotADirectoryError(f"Не директория: {Path.cwd()}")

    os.chdir(path)
    logger.info(f"Сменили директорию с: '{const_path}' на: '{Path.cwd()}'")
    return
