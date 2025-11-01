import os
import logging

logger = logging.getLogger(__name__)

def pwd_command() -> str:
    logger.info(f"Pwd command: {os.getcwd()}")
    return os.getcwd()
