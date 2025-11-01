# import logging
# from logging import Logger
from os import PathLike
from pathlib import Path
import os
# logger = Logger(__name__)

def cd_command(
    path: PathLike[str] | str) -> None:
    path = Path(path)
    os.chdir(path)
