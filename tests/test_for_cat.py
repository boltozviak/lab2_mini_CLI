import pytest

from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.cat_cmd import cat_command
from src.constants.file_mode import FileReadMode


def test_cat_string_mode(fs: FakeFilesystem):
    fs.create_file("/test.txt", contents="Hello, World!")
    result = cat_command("/test.txt")
    assert result == "Hello, World!"
    assert isinstance(result, str)

def test_cat_bytes_mode(fs: FakeFilesystem):
    content = b"Binary content \x00\x01\x02"
    fs.create_file("/binary.bin", contents=content)
    result = cat_command("/binary.bin", mode=FileReadMode.bytes)
    assert result == content
    assert isinstance(result, bytes)

def test_cat_validation_errors(fs: FakeFilesystem):
    with pytest.raises(FileNotFoundError) as exc_info:
        cat_command("/nonexistent.txt")
    assert "Entered path is not exists" in str(exc_info.value)

def test_cat_directory_raises_error(fs: FakeFilesystem):
    fs.create_dir("/test_dir")
    with pytest.raises(IsADirectoryError) as exc_info:
        cat_command("/test_dir")
    assert "Entered path is not a file" in str(exc_info.value)
