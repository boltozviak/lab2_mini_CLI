import pytest

from pathlib import Path

from pyfakefs.fake_filesystem import FakeFilesystem
from src.commands.cp_cmd import cp_command


def test_cp_creates_dest(fs: FakeFilesystem):
    fs.create_file("/source.txt")
    cp_command("/source.txt", "/dest.txt")
    assert Path("/dest.txt").exists()

def test_cp_source_not_found(fs: FakeFilesystem):
    with pytest.raises(FileNotFoundError):
        cp_command("/test_file.txt", "/dest.txt")

def test_cp_dir_without_recursive(fs: FakeFilesystem):
    fs.create_dir("/source_dir")
    with pytest.raises(IsADirectoryError) as exc_info:
        cp_command("/source_dir", "/dest_dir")
    assert "Директория копируется не рекурсивно" in str(exc_info.value)

def test_cp_dir_recursive_copies_file(fs: FakeFilesystem):
    fs.create_dir("/source_dir")
    fs.create_file("/source_dir/file.txt")
    cp_command("/source_dir", "/dest_dir", recursive=True)
    assert Path("/dest_dir/file.txt").exists()

def test_cp_dir_recursive_into_existing_copies_file(fs: FakeFilesystem):
    fs.create_dir("/source_dir")
    fs.create_file("/source_dir/file.txt")
    fs.create_dir("/existing_dest")
    cp_command("/source_dir", "/existing_dest", recursive=True)
    assert Path("/existing_dest/source_dir/file.txt").exists()

def test_cp_dir_recursive_dest_is_file(fs: FakeFilesystem):
    fs.create_dir("/source_dir")
    fs.create_file("/dest_file.txt")
    with pytest.raises(NotADirectoryError) as exc_info:
        cp_command("/source_dir", "/dest_file.txt", recursive=True)
    assert "Пункт назначения - файл" in str(exc_info.value)
