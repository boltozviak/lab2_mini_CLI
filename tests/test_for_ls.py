import pytest

from pyfakefs.fake_filesystem import FakeFilesystem
from src.commands.ls_cmd import ls_command


def test_ls_basic_functionality(fs: FakeFilesystem):
    fs.create_dir("/empty")
    result = ls_command("/empty")
    assert result == ""

    fs.create_dir("/dir")
    fs.create_file("/dir/file1.txt")
    fs.create_file("/dir/file2.txt")
    fs.create_file("/dir/.hidden")

    result_default = ls_command("/dir")
    assert "file1.txt" in result_default
    assert "file2.txt" in result_default
    assert ".hidden" not in result_default

    result_advanced = ls_command("/dir", advanced=True)
    assert "file1.txt" in result_advanced
    assert "file2.txt" in result_advanced
    assert ".hidden" in result_advanced


def test_ls_errors(fs: FakeFilesystem):
    with pytest.raises(FileNotFoundError) as exc_info:
        ls_command("/nonexistent")
    assert "Файл не существует" in str(exc_info.value)

    fs.create_file("/file.txt")
    with pytest.raises(NotADirectoryError) as exc_info:
        ls_command("/file.txt")
    assert "Не директория" in str(exc_info.value)


def test_ls_long_format(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt", contents="Hello World")
    fs.create_file("/dir/empty.txt", contents="")
    fs.create_dir("/dir/subdir")

    result = ls_command("/dir", long_format=True)

    assert "file.txt" in result
    assert "empty.txt" in result
    assert "subdir" in result

    lines = result.split("\n")
    assert len(lines) == 3

    first_line = lines[0]
    parts = first_line.split()
    assert len(parts) >= 7

    assert "-" in result or "d" in result

    assert "11" in result
    assert "0" in result

    assert any(char.isdigit() for char in result)


def test_ls_long_format_with_advanced(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/visible.txt")
    fs.create_file("/dir/.hidden")

    result_no_advanced = ls_command("/dir", long_format=True)
    assert "visible.txt" in result_no_advanced
    assert ".hidden" not in result_no_advanced

    result_advanced = ls_command("/dir", long_format=True, advanced=True)
    assert "visible.txt" in result_advanced
    assert ".hidden" in result_advanced
