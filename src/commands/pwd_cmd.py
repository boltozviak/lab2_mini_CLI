import os
import logging

logger = logging.getLogger(__name__)

def pwd_command() -> str:
    '''
    Выводит путь к директории, где находимся
    '''
    logger.info(f"Текущая директория: {os.getcwd()}")
    return os.getcwd()
