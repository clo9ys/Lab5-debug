import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import Shell

def test_zip_unzip_archive(fs):
    fs.create_dir('/src')
    fs.create_file('/src/file1.txt', contents='Samir')
    fs.create_file('/src/file2.txt', contents='Legend')
    os.chdir('/')
    shell = Shell()
    shell.run("zip src src.zip")
    fs.remove_object('/src/file1.txt')
    fs.remove_object('/src/file2.txt')
    shell.run('unzip src.zip')
    assert os.path.exists('/src/file1.txt')
    assert os.path.exists('/src/file2.txt')
    with open('/src/file1.txt') as f:
        assert f.read() == 'Samir'
    with open('/src/file2.txt') as f:
        assert f.read() == 'Legend'
