import pytest
import os

from pathlib import Path

from pyfakefs.fake_filesystem import FakeFilesystem
from src.commands.rm_cmd import rm_command


def test_rm_file_successfully(fs: FakeFilesystem):
    fs.create_file("/tralala.txt")
    rm_command("/tralala.txt")
    assert not Path("/tralala.txt").exists()

def test_rm_nonexistent_file(fs: FakeFilesystem):
    with pytest.raises(FileNotFoundError) as exc_info:
        rm_command("/tralala.txt")
    assert "Файл не существует" in str(exc_info.value)

def test_rm_important_path_home(fs: FakeFilesystem):
    home = Path.home()
    fs.create_dir(home)
    with pytest.raises(PermissionError) as exc_info:
        rm_command(home)
    assert "Вы не можете удалить этот файл" in str(exc_info.value)

def test_rm_parent_directory_of_cwd(fs: FakeFilesystem):
    fs.create_dir("/parent/tralala_child")
    os.chdir("/parent/tralala_child")
    with pytest.raises(PermissionError):
        rm_command("/parent/tralala_child")

def test_rm_directory_without_recursive(fs: FakeFilesystem):
    fs.create_dir("/tralala_dir")
    with pytest.raises(IsADirectoryError) as exc_info:
        rm_command("/tralala_dir")
    assert "Директория не пуста" in str(exc_info.value)

def test_rm_directory_with_recursive(fs: FakeFilesystem):
    fs.create_dir("/tralala_dir")
    fs.create_file("/tralala_dir/file.txt")
    rm_command("/tralala_dir", recursive=True)
    assert not Path("/tralala_dir").exists()
