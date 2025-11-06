import logging
import shutil
from os import PathLike
from pathlib import Path


logger = logging.getLogger(__name__)

def mv_command(
    filename_source: PathLike[str] | str,
    filename_destination: PathLike[str] | str,
) -> None:

    src = Path(filename_source)
    dst = Path(filename_destination)

    if not src.exists():
        logger.error(f"Файл не существует: {src}")
        raise FileNotFoundError(f"Файл не существует: {src}")

    try:
        shutil.move(src, dst)
        logger.info(f"Успешно перемещено: {src} в {dst}")
    except OSError as e:
        logger.error(f"Ошибка при перемещении {src} в {dst}: {e}")
        raise
