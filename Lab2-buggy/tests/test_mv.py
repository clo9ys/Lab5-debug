import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import Shell

def test_mv_rename_file(fs):
    fs.create_dir('/work')
    fs.create_file('/work/file1.txt')
    os.chdir('/work')
    shell = Shell()
    shell.run('mv file1.txt file2.txt')
    assert not os.path.exists('file1.txt')
    assert os.path.exists('file2.txt')

def test_mv_file_to_dir(fs):
    fs.create_dir('/work/dst')
    fs.create_file('/work/file1.txt')
    os.chdir('/work')
    shell = Shell()
    shell.run('mv file1.txt dst')
    assert os.path.exists('dst/file1.txt')

def test_mv_many_files_to_dir(fs):
    fs.create_dir('/work/dst')
    fs.create_file('/work/file1.txt')
    fs.create_file('/work/file2.txt')
    os.chdir('/work')
    shell = Shell()
    shell.run('mv file1.txt file2.txt dst')
    assert os.path.exists('dst/file1.txt')
    assert os.path.exists('dst/file2.txt')

def test_mv_many_files_to_file(fs, capsys):
    fs.create_dir('/work')
    fs.create_file('/work/file1.txt')
    fs.create_file('/work/file2.txt')
    fs.create_file('/work/dst.txt')
    os.chdir('/work')
    shell = Shell()
    shell.run('mv file1.txt file2.txt dst.txt')
    out = capsys.readouterr().out
    assert 'is not a directory' in out