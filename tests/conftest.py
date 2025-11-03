import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

@pytest.fixture(scope='function')
def test_dir_with_files(fs: FakeFilesystem):
    fs.create_dir("/test_dir")
    fs.create_dir("/test_dir/test_dir2")
    fs.create_file("/test_dir/test_file.txt")
    fs.create_file("/test_dir/test_file2.txt")
    fs.create_file("/test_dir/.hidden_file.txt")
    fs.create_dir("/test_dir/test_dir3")
    fs.create_file("/test_dir/test_dir3/test_file3.txt")
    return "/test_dir"
