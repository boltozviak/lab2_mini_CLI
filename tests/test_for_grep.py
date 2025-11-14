import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.grep_cmd import grep_command


def test_grep_find_pattern_in_file(fs: FakeFilesystem):
    fs.create_file("/test.txt", contents="tralal\nazaza zaza\nla-la-la-la")
    result = grep_command("azaza", "/test.txt")
    assert len(result) == 1
    assert "/test.txt : 2 : azaza zaza" in result


def test_grep_pattern_not_found_returns_empty(fs: FakeFilesystem):
    fs.create_file("/test.txt", contents="tralal\nazaza zaza\nla-la-la-la")
    result = grep_command("sas", "/test.txt")
    assert len(result) == 0
    assert result == []


def test_grep_case_insensitive_with_ignore_flag(fs: FakeFilesystem):
    fs.create_file("/test.txt", contents="tralal\nAzAzA zaza\nla-la-la-la\nTRALAZAZA")
    result = grep_command("azaza", "/test.txt", ignore=True)
    assert len(result) == 2
    assert "/test.txt : 2 : AzAzA zaza" in result
    assert "/test.txt : 4 : TRALAZAZA" in result


def test_grep_case_sensitive_without_ignore_flag(fs: FakeFilesystem):
    fs.create_file("/test.txt", contents="tralal\nAzAzA zaza\nla-la-la-la\ntralazaza")
    result = grep_command("azaza", "/test.txt", ignore=False)
    assert len(result) == 1
    assert "/test.txt : 4 : tralazaza" in result

def test_grep_recursive_in_directory(fs: FakeFilesystem):
    fs.create_dir("/tralala_dir1")
    fs.create_file("/tralala_dir1/file1.txt", contents="tralal\nazaza zaza\nla-la-la-la")
    fs.create_file("/tralala_dir1/file2.txt", contents="tralal\nazaza zaza\nla-la-la-la")
    fs.create_dir("/tralala_dir1/tralala_dir2")
    fs.create_file("/tralala_dir1/tralala_dir2/file3.txt", contents="tralal\nazaza zaza\nla-la-la-la")
    result = grep_command("azaza", "/tralala_dir1", recursive=True)
    assert len(result) == 3
    assert "/tralala_dir1/file1.txt : 2 : azaza zaza" in result
    assert "/tralala_dir1/file2.txt : 2 : azaza zaza" in result
    assert "/tralala_dir1/tralala_dir2/file3.txt : 2 : azaza zaza" in result


def test_grep_directory_without_recursive_raises_error(fs: FakeFilesystem):
    fs.create_dir("/tralala_dir1")
    fs.create_dir("/tralala_dir1/tralala_dir2")
    fs.create_file("/tralala_dir1/tralala_dir2/azaza.txt")
    with pytest.raises(IsADirectoryError) as exc_info:
        grep_command("azaza", "/tralala_dir1", recursive=False)
    assert "Директория требует рекурсивного поиска" in str(exc_info.value)


def test_grep_file_not_found_raises_error(fs: FakeFilesystem):
    with pytest.raises(FileNotFoundError) as exc_info:
        grep_command("azaza", "/tralala.txt")
    assert "Файл не найден/не существует" in str(exc_info.value)


def test_grep_invalid_regex_raises_error(fs: FakeFilesystem):
    fs.create_file("/test.txt", contents="tralal\nazaza zaza\nla-la-la-la")
    with pytest.raises(ValueError) as exc_info:
        grep_command("[invalid", "/test.txt")
    assert "Регулярочка с ошибкой" in str(exc_info.value)
