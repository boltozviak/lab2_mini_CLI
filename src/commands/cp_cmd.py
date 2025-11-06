import logging
import shutil
from os import PathLike
from pathlib import Path


logger = logging.getLogger(__name__)

def cp_command(
    filename_source: PathLike[str] | str,
    filename_destination: PathLike[str] | str,
    recursive: bool = False,
) -> None:

    src = Path(filename_source)
    dst = Path(filename_destination)

    if not src.exists():
        logger.error(f"Файл не существует: {src}")
        raise FileNotFoundError(f"Файл не существует: {src}")


    try:
        if src.is_file():
            shutil.copy(src, dst)
            logger.info(f"Успешно скопировано: {src} в {dst}")
        elif src.is_dir():
            if not recursive:
                logger.error(f"Не директория: {src}")
                raise IsADirectoryError(f"Не директория: {src}")
            else:
                if dst.exists() and dst.is_file():
                    logger.error(f"Пункт назначения - файл: {dst}")
                    raise IsADirectoryError(f"Пункт назначения - файл: {dst}")
                elif dst.exists() and dst.is_dir():
                    destination_path = dst / src.name
                    shutil.copytree(src, destination_path)
                    logger.info(f"Успешно скопировано: {src} в {dst}")
                else:
                    shutil.copytree(src, dst)
                    logger.info(f"Успешно скопировано: {src} в {dst}")
    except shutil.Error as e:
        logger.error(f"Ошибка при копировании {src} в {dst}: {e}")
        raise
    except OSError as e:
        logger.error(f"Ошибка при копировании {src} в {dst}: {e}")
        raise
