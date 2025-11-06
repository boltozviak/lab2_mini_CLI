import pytest
import os
import pwd
import grp
from datetime import datetime

from pyfakefs.fake_filesystem import FakeFilesystem
from src.commands.ls_cmd import ls_command


def test_ls_empty_returns_empty_string(fs: FakeFilesystem):
    fs.create_dir("/empty")
    result = ls_command("/empty")
    assert result == ""

def test_ls_default_shows_file1(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file1.txt")
    result_default = ls_command("/dir")
    assert "file1.txt" in result_default

def test_ls_default_hides_hidden(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/.hidden")
    result_default = ls_command("/dir")
    assert ".hidden" not in result_default

def test_ls_advanced_shows_hidden(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/.hidden")
    result_advanced = ls_command("/dir", advanced=True)
    assert ".hidden" in result_advanced

def test_ls_errors_file_not_found(fs: FakeFilesystem):
    with pytest.raises(FileNotFoundError) as exc_info:
        ls_command("/nonexistent")
    assert "Файл не существует" in str(exc_info.value)

def test_ls_errors_not_a_directory(fs: FakeFilesystem):
    fs.create_file("/file.txt")
    with pytest.raises(NotADirectoryError) as exc_info:
        ls_command("/file.txt")
    assert "Не директория" in str(exc_info.value)

def test_ls_file_mode(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt")
    result = ls_command("/dir", long_format=True)
    assert result.split()[0].startswith("-")

def test_ls_dir_mode(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_dir("/dir/subdir")
    result = ls_command("/dir", long_format=True)
    assert result.split()[0].startswith("d")

def test_ls_nlinks(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt")
    result = ls_command("/dir", long_format=True)
    assert result.split()[1].isdigit()

def test_ls_uid(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt")
    result = ls_command("/dir", long_format=True)
    uid_field = result.split()[2]
    stat_uid_name = pwd.getpwuid(os.stat("/dir/file.txt").st_uid).pw_name
    assert uid_field == stat_uid_name

def test_ls_gid(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt")
    result = ls_command("/dir", long_format=True)
    gid_field = result.split()[3]
    stat_gid_name = grp.getgrgid(os.stat("/dir/file.txt").st_gid).gr_name
    assert gid_field == stat_gid_name

def test_ls_size(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt", contents="azaza")
    result = ls_command("/dir", long_format=True)
    size_field = int(result.split()[4])
    stat_size = os.stat("/dir/file.txt").st_size
    assert size_field == stat_size

def test_ls_mtime(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt")
    result = ls_command("/dir", long_format=True)
    time_field = f"{result.split()[5]} {result.split()[6]}"
    stat_time = str(datetime.fromtimestamp(os.stat("/dir/file.txt").st_mtime)).split(".")[0]
    assert time_field == stat_time

def test_ls_name(fs: FakeFilesystem):
    fs.create_dir("/dir")
    fs.create_file("/dir/file.txt")
    result = ls_command("/dir", long_format=True)
    assert result.split()[-1] == "file.txt"
