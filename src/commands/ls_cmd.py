# import logging
import os
import stat
import pwd
import grp
# from logging import Logger
from os import PathLike
from pathlib import Path
from datetime import datetime

# logger = Logger(__name__)

def ls_command(
    path: PathLike[str] | str,
    long_format: bool = False,
    advanced: bool = False) -> str:

    path = Path(path)
    if advanced:
        files = os.listdir(path)
    else:
        files = [f for f in os.listdir(path) if not f.startswith('.')]



    if long_format:
        dir_files = []

        for file in files:
            file_path = os.path.join(path, file)

            file_mode = str(stat.filemode(os.stat(file_path).st_mode))
            file_nlinks = str(os.stat(file_path).st_nlink)
            file_gid = str(grp.getgrgid(os.stat(file_path).st_gid).gr_name)
            file_uid = str(pwd.getpwuid(os.stat(file_path).st_uid).pw_name)
            file_size = str(os.stat(file_path).st_size)
            file_time = str(datetime.fromtimestamp(os.stat(file_path).st_mtime)).split(".")[0]

            file_str = f"{file_mode:5} {file_nlinks:2} {file_uid:5} {file_gid:5} {file_size:5} {file_time:20} {file}"

            dir_files.append(file_str)

        return "\n".join(dir_files)

    return "\n".join(files)
