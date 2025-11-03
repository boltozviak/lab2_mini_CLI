import pytest

from pathlib import Path

from pyfakefs.fake_filesystem import FakeFilesystem
from src.commands.mv_cmd import mv_command


def test_mv_file_successfully(fs: FakeFilesystem):
    fs.create_file("/source.txt", contents="test data")
    mv_command("/source.txt", "/dest.txt")
    assert not Path("/source.txt").exists()
    assert Path("/dest.txt").exists()
    assert Path("/dest.txt").read_text() == "test data"

def test_mv_nonexistent_source(fs: FakeFilesystem):
    with pytest.raises(FileNotFoundError) as exc_info:
        mv_command("/nonexistent.txt", "/dest.txt")
    assert "Entered source file is not exists" in str(exc_info.value)
