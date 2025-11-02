import logging
import os
import stat
import pwd
import grp
from os import PathLike
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

def ls_command(
    path: PathLike[str] | str,
    long_format: bool = False,
    advanced: bool = False) -> str:

    path = Path(path)

    if not path.exists():
        logger.error(f"Path is not exists: {path}")
        raise FileNotFoundError(f"Path is not exists: {path}")

    if not path.is_dir():
        logger.error(f"Path is not a directory: {path}")
        raise NotADirectoryError(f"Path is not a directory: {path}")

    if advanced:
        files = os.listdir(path)
    else:
        files = [f for f in os.listdir(path) if not f.startswith('.')]

    if long_format:
        dir_files = []

        for file in files:
            file_path = os.path.join(path, file)
            stat_info = os.stat(file_path)

            file_mode = str(stat.filemode(stat_info.st_mode))
            file_nlinks = str(stat_info.st_nlink)
            file_gid = str(grp.getgrgid(stat_info.st_gid).gr_name)
            file_uid = str(pwd.getpwuid(stat_info.st_uid).pw_name)
            file_size = str(stat_info.st_size)
            file_time = str(datetime.fromtimestamp(stat_info.st_mtime)).split(".")[0]

            file_str = f"{file_mode:5} {file_nlinks:5} {file_uid:5} {file_gid:5} {file_size:10} {file_time:20} {file}"

            dir_files.append(file_str)

        logger.info(path)
        return "\n".join(dir_files)

    logger.info(path)
    return "\n".join(files)
