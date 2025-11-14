import logging
import shutil
from os import PathLike
from pathlib import Path
from src.constants.denied_files import get_denied_paths

logger = logging.getLogger(__name__)

def cp_command(
    filename_source: PathLike[str] | str,
    filename_destination: PathLike[str] | str,
    recursive: bool = False,
) -> None:
    '''
    Копирует файл или директорию

    Параметры:
    - filename_source - путь к файлу или директории, которые копируем
    - filename_destination - путь к файлу или директории, в которую копируем
    - recursive - копируем ли директорию рекурсивно

    Исключения:
    - FileNotFoundError - не найдено/не существует исходный файл
    - IsADirectoryError - копированеи директоирии происходит не рекурсивно
    - NotADirectoryError - попытка копирвать директорию в файл
    - PermissionError - попытка копировать важный файл/директорию
    '''

    src = Path(filename_source)
    dst = Path(filename_destination)
    current_path = Path.cwd().resolve()
    denied_paths = get_denied_paths(current_path)

    if not src.exists():
        logger.error(f"Файл не существует: {src}")
        raise FileNotFoundError(f"Файл не существует: {src}")

    src = src.resolve()

    if src in denied_paths:
        logger.error(f"Попытка копировать важный файл: {src}")
        raise PermissionError(f"Нельзя копировать данный файл: {src}")

    try:
        if src.is_file():
            shutil.copy(src, dst)
            logger.info(f"Успешно скопировано: {src} в {dst}")
        elif src.is_dir():
            if not recursive:
                logger.error(f"Директория копируется не рекурсивно: {src}")
                raise IsADirectoryError(f"Директория копируется не рекурсивно: {src}")
            else:
                if dst.exists() and dst.is_file():
                    logger.error(f"Пункт назначения - файл: {dst}")
                    raise NotADirectoryError(f"Пункт назначения - файл: {dst}")
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
