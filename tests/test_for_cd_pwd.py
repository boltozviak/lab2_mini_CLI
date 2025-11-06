import pytest
import os

from pathlib import Path
from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.cd_cmd import cd_command
from src.commands.pwd_cmd import pwd_command


def test_cd_basic_paths(fs: FakeFilesystem):
    fs.create_dir("/parent/child")
    cd_command("/parent/child")
    assert Path.cwd() == Path("/parent/child")

def test_cd_go_to_parent(fs: FakeFilesystem):
    fs.create_dir("/parent/child")
    cd_command("/parent")
    assert Path.cwd() == Path("/parent")

def test_cd_go_to_child(fs: FakeFilesystem):
    fs.create_dir("/parent/child")
    cd_command("/parent")
    cd_command("child")
    assert Path.cwd() == Path("/parent/child")

def test_cd_parent_directory(fs: FakeFilesystem):
    fs.create_dir("/parent/child")
    os.chdir("/parent/child")
    cd_command("..")
    assert Path.cwd() == Path("/parent")

def test_cd_current_directory(fs: FakeFilesystem):
    fs.create_dir("/parent")
    os.chdir("/parent")
    cd_command(".")
    assert Path.cwd() == Path("/parent")

def test_cd_home_directory(fs: FakeFilesystem):
    home = os.path.expanduser("~")
    fs.create_dir(home)
    fs.create_dir("/some_dir")
    os.chdir("/some_dir")
    cd_command("~")
    assert Path.cwd() == Path(home)

def test_cd_errors(fs: FakeFilesystem):
    fs.create_dir("/existing")
    os.chdir("/existing")
    with pytest.raises(FileNotFoundError) as exc_info:
        cd_command("/nonexistent")
    assert "Файл не существует" in str(exc_info.value)

def test_cd_nonexistent_subdir_raises_error(fs: FakeFilesystem):
    fs.create_dir("/existing")
    with pytest.raises(FileNotFoundError) as exc_info:
        cd_command("/existing/nonexistent_subdir")
    assert "Файл не существует" in str(exc_info.value)

def test_cd_file_raises_error(fs: FakeFilesystem):
    fs.create_file("/test_file.txt")
    with pytest.raises(NotADirectoryError) as exc_info:
        cd_command("/test_file.txt")
    assert "Не директория" in str(exc_info.value)

def test_pwd_command(fs: FakeFilesystem):
    fs.create_dir("/test_pwd")
    os.chdir("/test_pwd")
    result = pwd_command()
    assert result == "/test_pwd"
