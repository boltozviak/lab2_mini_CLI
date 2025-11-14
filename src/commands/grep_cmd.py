import os
from os import PathLike
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

def find_in_file(file_path: Path, user_regexp: re.Pattern) -> list[str]:
    '''
    что в файле есть
    '''
    result = []
    with open(file_path, 'r') as f:
        for num, line in enumerate(f, 1):
            if user_regexp.search(line):
                result.append(f"{file_path} : {num} : {line.rstrip('\n')}")
    return result

def find_in_directory(directory: Path, user_regexp: re.Pattern) -> list[str]:
    '''
    файлики в директориях
    '''
    result= []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = Path(root) / filename
            result.extend(find_in_file(file_path, user_regexp))
    return result

def grep_command(
    pattern: str,
    src: PathLike[str] | str,
    recursive: bool = False,
    ignore: bool = False,
) -> list[str]:

    src = Path(src)
    result = []

    if not src.exists():
        logger.error(f"Файл не найден: {src}")
        raise FileNotFoundError(f"Файл не найден/не существует: {src}")

    try:
        if ignore:
            user_regexp = re.compile(pattern, re.IGNORECASE)
        else:
            user_regexp = re.compile(pattern)
    except re.error as e:
        logger.error(f"Регулярочка с ошибкой: {e}")
        raise ValueError(f"Регулярочка с ошибкой: {e}")

    if src.is_file():
        result.extend(find_in_file(src, user_regexp))
    elif src.is_dir():
        if recursive:
            result.extend(find_in_directory(src, user_regexp))
        else:
            logger.error(f"Директория требует рекурсивного поиска: {src}")
            raise IsADirectoryError(f"Директория требует рекурсивного поиска: {src}")

    logger.info(f"grep: найдено {len(result)} подстрок")

    return result
