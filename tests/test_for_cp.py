import pytest

from pathlib import Path

from pyfakefs.fake_filesystem import FakeFilesystem
from src.commands.cp_cmd import cp_command


def test_cp_file_to_file(fs: FakeFilesystem):
    fs.create_file("/source.txt", contents="test")
    cp_command("/source.txt", "/dest.txt")
    assert Path("/dest.txt").exists()
    assert Path("/dest.txt").read_text() == "test"

def test_cp_nonexistent_source(fs: FakeFilesystem):
    with pytest.raises(FileNotFoundError):
        cp_command("/nonexistent.txt", "/dest.txt")

def test_cp_directory_without_recursive(fs: FakeFilesystem):
    fs.create_dir("/source_dir")
    with pytest.raises(IsADirectoryError) as exc_info:
        cp_command("/source_dir", "/dest_dir")
    assert "use -r" in str(exc_info.value)

def test_cp_directory_recursive_to_new_location(fs: FakeFilesystem):
    fs.create_dir("/source_dir")
    fs.create_file("/source_dir/file.txt", contents="data")
    cp_command("/source_dir", "/dest_dir", recursive=True)
    assert Path("/dest_dir").exists()
    assert Path("/dest_dir/file.txt").exists()

def test_cp_directory_recursive_into_existing_dir(fs: FakeFilesystem):
    fs.create_dir("/source_dir")
    fs.create_file("/source_dir/file.txt")
    fs.create_dir("/existing_dest")
    cp_command("/source_dir", "/existing_dest", recursive=True)
    assert Path("/existing_dest/source_dir").exists()
    assert Path("/existing_dest/source_dir/file.txt").exists()

def test_cp_directory_recursive_dest_is_file(fs: FakeFilesystem):
    fs.create_dir("/source_dir")
    fs.create_file("/dest_file.txt")
    with pytest.raises(IsADirectoryError) as exc_info:
        cp_command("/source_dir", "/dest_file.txt", recursive=True)
    assert "Destination is a file" in str(exc_info.value)
