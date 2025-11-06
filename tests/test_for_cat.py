import pytest

from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.cat_cmd import cat_command
from src.constants.file_mode import FileReadMode


def test_cat_string_content(fs: FakeFilesystem):
    fs.create_file("/azaza.txt", contents="azaza")
    result = cat_command("/azaza.txt")
    assert result == "azaza"

def test_cat_string_type(fs: FakeFilesystem):
    fs.create_file("/azaza.txt", contents="azaza")
    result = cat_command("/azaza.txt")
    assert isinstance(result, str)

def test_cat_bytes_content(fs: FakeFilesystem):
    fs.create_file("/azaza.bin", contents=b"azaza")
    result = cat_command("/azaza.bin", mode=FileReadMode.bytes)
    assert result == b"azaza"

def test_cat_bytes_type(fs: FakeFilesystem):
    fs.create_file("/azaza.bin", contents=b"azaza")
    result = cat_command("/azaza.bin", mode=FileReadMode.bytes)
    assert isinstance(result, bytes)

def test_cat_validation_errors(fs: FakeFilesystem):
    with pytest.raises(FileNotFoundError) as exc_info:
        cat_command("/tralala.txt")
    assert "Файл не существует" in str(exc_info.value)

def test_cat_directory_raises_error(fs: FakeFilesystem):
    fs.create_dir("/tralala_dir")
    with pytest.raises(IsADirectoryError) as exc_info:
        cat_command("/tralala_dir")
    assert "Не файл" in str(exc_info.value)
