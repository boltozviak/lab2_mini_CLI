import pytest

from pathlib import Path

from pyfakefs.fake_filesystem import FakeFilesystem
from src.commands.mv_cmd import mv_command


def test_mv_removes_source(fs: FakeFilesystem):
    fs.create_file("/source.txt", contents="azaza")
    mv_command("/source.txt", "/azaza.txt")
    assert not Path("/source.txt").exists()

def test_mv_creates_destination(fs: FakeFilesystem):
    fs.create_file("/source.txt", contents="azaza")
    mv_command("/source.txt", "/azaza.txt")
    assert Path("/azaza.txt").exists()

def test_mv_preserves_content(fs: FakeFilesystem):
    fs.create_file("/source.txt", contents="azaza")
    mv_command("/source.txt", "/azaza.txt")
    assert Path("/azaza.txt").read_text() == "azaza"

def test_mv_nonexistent_source(fs: FakeFilesystem):
    with pytest.raises(FileNotFoundError) as exc_info:
        mv_command("/tralala.txt", "/azaza.txt")
    assert "Файл не существует" in str(exc_info.value)
