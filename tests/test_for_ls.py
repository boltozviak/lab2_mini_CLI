import pytest

from pyfakefs.fake_filesystem import FakeFilesystem
from src.commands.ls_cmd import ls_command


def test_ls_empty_returns_empty_string(fs: FakeFilesystem):
    fs.create_dir("/empty")
    result = ls_command("/empty")
    assert result == ""

def test_ls_default_shows_file1(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file1.txt")
    fs.create_file("/dir/file2.txt")
    fs.create_file("/dir/.hidden")
    result_default = ls_command("/dir")
    assert "file1.txt" in result_default

def test_ls_default_shows_file2(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file1.txt")
    fs.create_file("/dir/file2.txt")
    fs.create_file("/dir/.hidden")
    result_default = ls_command("/dir")
    assert "file2.txt" in result_default

def test_ls_default_hides_hidden(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file1.txt")
    fs.create_file("/dir/file2.txt")
    fs.create_file("/dir/.hidden")
    result_default = ls_command("/dir")
    assert ".hidden" not in result_default

def test_ls_advanced_shows_file1(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file1.txt")
    fs.create_file("/dir/file2.txt")
    fs.create_file("/dir/.hidden")
    result_advanced = ls_command("/dir", advanced=True)
    assert "file1.txt" in result_advanced

def test_ls_advanced_shows_file2(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file1.txt")
    fs.create_file("/dir/file2.txt")
    fs.create_file("/dir/.hidden")
    result_advanced = ls_command("/dir", advanced=True)
    assert "file2.txt" in result_advanced

def test_ls_advanced_shows_hidden(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file1.txt")
    fs.create_file("/dir/file2.txt")
    fs.create_file("/dir/.hidden")
    result_advanced = ls_command("/dir", advanced=True)
    assert ".hidden" in result_advanced


def test_ls_errors(fs: FakeFilesystem):
    with pytest.raises(FileNotFoundError) as exc_info:
        ls_command("/nonexistent")
    assert "Файл не существует" in str(exc_info.value)

    fs.create_file("/file.txt")
    with pytest.raises(NotADirectoryError) as exc_info:
        ls_command("/file.txt")
    assert "Не директория" in str(exc_info.value)


def test_ls_long_format_lists_file_txt(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt", contents="Hello World")
    fs.create_file("/dir/empty.txt", contents="")
    fs.create_dir("/dir/subdir")
    result = ls_command("/dir", long_format=True)
    assert "file.txt" in result

def test_ls_long_format_lists_empty_txt(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt", contents="Hello World")
    fs.create_file("/dir/empty.txt", contents="")
    fs.create_dir("/dir/subdir")
    result = ls_command("/dir", long_format=True)
    assert "empty.txt" in result

def test_ls_long_format_lists_subdir(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt", contents="Hello World")
    fs.create_file("/dir/empty.txt", contents="")
    fs.create_dir("/dir/subdir")
    result = ls_command("/dir", long_format=True)
    assert "subdir" in result

def test_ls_long_format_has_three_lines(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt", contents="Hello World")
    fs.create_file("/dir/empty.txt", contents="")
    fs.create_dir("/dir/subdir")
    result = ls_command("/dir", long_format=True)
    lines = result.split("\n")
    assert len(lines) == 3

def test_ls_long_format_line_has_min_columns(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt", contents="Hello World")
    fs.create_file("/dir/empty.txt", contents="")
    fs.create_dir("/dir/subdir")
    result = ls_command("/dir", long_format=True)
    first_line = result.split("\n")[0]
    parts = first_line.split()
    assert len(parts) >= 7

def test_ls_long_format_contains_type_marker(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt", contents="Hello World")
    fs.create_file("/dir/empty.txt", contents="")
    fs.create_dir("/dir/subdir")
    result = ls_command("/dir", long_format=True)
    assert "-" in result or "d" in result

def test_ls_long_format_contains_size_11(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt", contents="Hello World")
    fs.create_file("/dir/empty.txt", contents="")
    fs.create_dir("/dir/subdir")
    result = ls_command("/dir", long_format=True)
    assert "11" in result

def test_ls_long_format_contains_size_0(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt", contents="Hello World")
    fs.create_file("/dir/empty.txt", contents="")
    fs.create_dir("/dir/subdir")
    result = ls_command("/dir", long_format=True)
    assert "0" in result

def test_ls_long_format_has_digits(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt", contents="Hello World")
    fs.create_file("/dir/empty.txt", contents="")
    fs.create_dir("/dir/subdir")
    result = ls_command("/dir", long_format=True)
    assert any(char.isdigit() for char in result)


def test_ls_long_format_without_advanced_hides_hidden(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/visible.txt")
    fs.create_file("/dir/.hidden")
    result_no_advanced = ls_command("/dir", long_format=True)
    assert ".hidden" not in result_no_advanced

def test_ls_long_format_with_advanced_shows_visible(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/visible.txt")
    fs.create_file("/dir/.hidden")
    result_advanced = ls_command("/dir", long_format=True, advanced=True)
    assert "visible.txt" in result_advanced

def test_ls_long_format_with_advanced_shows_hidden(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/visible.txt")
    fs.create_file("/dir/.hidden")
    result_advanced = ls_command("/dir", long_format=True, advanced=True)
    assert ".hidden" in result_advanced
