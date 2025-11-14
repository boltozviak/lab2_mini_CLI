import pytest
import shutil

from pathlib import Path

from pyfakefs.fake_filesystem import FakeFilesystem
from src.commands.arch_cmd import zip_command, unzip_command, tar_command, untar_command


def test_zip_command_success(fs: FakeFilesystem):
    fs.create_dir("/test_dir")
    fs.create_file("/test_dir/file.txt")
    zip_command("/test_dir", "/archive.zip")
    assert Path("/archive.zip").exists()

def test_zip_command_wrong_ext_raises(fs: FakeFilesystem):
    fs.create_dir("/test_dir")
    with pytest.raises(ValueError) as exc_info:
        zip_command("/test_dir", "/archive.tar")
    assert "Попытка создания zip архива без .zip" in str(exc_info.value)

def test_creating_zip_without_suffix_raises(fs: FakeFilesystem):
    fs.create_dir("/test_dir")
    with pytest.raises(ValueError) as exc_info:
        zip_command("/test_dir", "/archive")
    assert "Попытка создания zip архива без .zip" in str(exc_info.value)

def test_zip_command_existing_archive_raises(fs: FakeFilesystem):
    fs.create_dir("/test_dir")
    fs.create_file("/existing.zip")
    with pytest.raises(FileExistsError) as exc_info:
        zip_command("/test_dir", "/existing.zip")
    assert "Архив уже существует" in str(exc_info.value)

def test_zip_command_nonexistent_src_raises(fs: FakeFilesystem):
    with pytest.raises(FileNotFoundError) as exc_info:
        zip_command("/nonexistent", "/archive.zip")
    assert "Директория не существует" in str(exc_info.value)

def test_zip_command_src_not_dir_raises(fs: FakeFilesystem):
    fs.create_file("/file.txt")
    with pytest.raises(NotADirectoryError) as exc_info:
        zip_command("/file.txt", "/archive.zip")
    assert "Не директория" in str(exc_info.value)


def test_unzip_creates_dir(fs: FakeFilesystem):
    fs.create_dir("/test_dir")
    fs.create_file("/test_dir/file.txt")
    zip_command("/test_dir", "/archive.zip")
    shutil.rmtree("/test_dir")
    unzip_command("/archive.zip")
    assert Path("/test_dir").exists()

def test_unzip_creates_file(fs: FakeFilesystem):
    fs.create_dir("/test_dir")
    fs.create_file("/test_dir/file.txt")
    zip_command("/test_dir", "/archive.zip")
    shutil.rmtree("/test_dir")
    unzip_command("/archive.zip")
    assert Path("/test_dir/file.txt").exists()

def test_unzip_nonexistent_raises(fs: FakeFilesystem):
    with pytest.raises(FileNotFoundError) as exc_info:
        unzip_command("/nonexistent.zip")
    assert "Архив не существует" in str(exc_info.value)

def test_unzip_not_zip_raises(fs: FakeFilesystem):
    fs.create_file("/not_zip.zip")
    with pytest.raises(ValueError) as exc_info:
        unzip_command("/not_zip.zip")
    assert "Попытка распаковки не zip архива" in str(exc_info.value)


def test_tar_command_success(fs: FakeFilesystem):
    fs.create_dir("/test_dir")
    fs.create_file("/test_dir/file.txt")
    tar_command("/test_dir", "/archive.tar.gz")
    assert Path("/archive.tar.gz").exists()

def test_tar_wrong_ext_zip_raises(fs: FakeFilesystem):
    fs.create_dir("/test_dir")
    with pytest.raises(ValueError) as exc_info:
        tar_command("/test_dir", "/archive.zip")
    assert "Попытка создания tar.gz архива без .tar.gz" in str(exc_info.value)

def test_tar_wrong_ext_tar_raises(fs: FakeFilesystem):
    fs.create_dir("/test_dir")
    with pytest.raises(ValueError) as exc_info:
        tar_command("/test_dir", "/archive.tar")
    assert "Попытка создания tar.gz архива без .tar.gz" in str(exc_info.value)

def test_tar_existing_archive_raises(fs: FakeFilesystem):
    fs.create_dir("/test_dir")
    fs.create_file("/existing.tar.gz")
    with pytest.raises(FileExistsError) as exc_info:
        tar_command("/test_dir", "/existing.tar.gz")
    assert "Архив уже существует" in str(exc_info.value)

def test_tar_nonexistent_src_raises(fs: FakeFilesystem):
    with pytest.raises(FileNotFoundError) as exc_info:
        tar_command("/nonexistent", "/archive.tar.gz")
    assert "Директория не существует" in str(exc_info.value)

def test_tar_src_not_dir_raises(fs: FakeFilesystem):
    fs.create_file("/file.txt")
    with pytest.raises(NotADirectoryError) as exc_info:
        tar_command("/file.txt", "/archive.tar.gz")
    assert "Не директория" in str(exc_info.value)

def test_untar_creates_file(fs: FakeFilesystem):
    fs.create_dir("/test_dir")
    fs.create_file("/test_dir/file.txt")
    tar_command("/test_dir", "/archive.tar.gz")
    shutil.rmtree("/test_dir")
    untar_command("/archive.tar.gz")
    assert Path("/test_dir/file.txt").exists()

def test_untar_nonexistent_raises(fs: FakeFilesystem):
    with pytest.raises(FileNotFoundError) as exc_info:
        untar_command("/nonexistent.tar.gz")
    assert "Архив не существует" in str(exc_info.value)

def test_untar_not_targz_raises(fs: FakeFilesystem):
    fs.create_file("/not_tar.tar.gz")
    with pytest.raises(ValueError) as exc_info:
        untar_command("/not_tar.tar.gz")
    assert "Попытка распаковки не tar.gz архива" in str(exc_info.value)
