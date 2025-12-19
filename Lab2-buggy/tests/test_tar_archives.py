import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import Shell

def test_tar_archive(fs):
    fs.create_dir('/src')
    fs.create_file('/src/file1.txt', contents='goose')
    fs.create_file('/src/file2.txt', contents='top-it')
    os.chdir('/')
    shell = Shell()
    shell.run('tar src src.tar.gz')
    fs.remove_object('/src/file1.txt')
    fs.remove_object('/src/file2.txt')
    shell.run('untar src.tar.gz')
    assert os.path.exists('/src/file1.txt')
    assert os.path.exists('/src/file2.txt')
    with open('/src/file1.txt') as f:
        assert f.read() == 'goose'
    with open('/src/file2.txt') as f:
        assert f.read() == 'top-it'
