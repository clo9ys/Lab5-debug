import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import Shell

def test_cp_files(fs):
    fs.create_dir('/work')
    fs.create_file('/work/file1.txt', contents='something')
    os.chdir('/work')
    shell = Shell()
    shell.run('cp file1.txt file2.txt')
    assert os.path.exists('file2.txt')
    with open('file2.txt') as f:
        assert f.read() == 'something'

def test_cp_files_to_dir(fs):
    fs.create_file('/file1.txt', contents='something1')
    fs.create_file('/file2.txt', contents='something2')
    fs.create_dir('/dst')
    os.chdir('/')
    shell = Shell()
    shell.run('cp file1.txt file2.txt dst')
    assert os.path.exists('/dst/file1.txt')
    assert os.path.exists('/dst/file2.txt')
    with open('/dst/file1.txt') as f:
        assert f.read() == 'something1'
    with open('/dst/file2.txt') as f:
        assert f.read() == 'something2'

def test_cp_r_flag(fs):
    fs.create_dir('/src/subdir')
    fs.create_file('/src/file1.txt', contents='something1')
    fs.create_file('/src/subdir/file2.txt', contents='something2')
    fs.create_dir('/dst')
    os.chdir('/')
    shell = Shell()
    shell.run('cp -r src dst')
    assert os.path.exists('/dst/src/file1.txt')
    assert os.path.exists('/dst/src/subdir/file2.txt')
    with open('/dst/src/file1.txt') as f:
        assert f.read() == 'something1'
    with open('/dst/src/subdir/file2.txt') as f:
        assert f.read() == 'something2'

def test_cp_not_a_dir(fs, capsys):
    fs.create_file('/file1.txt', contents='something1')
    fs.create_file('/file2.txt', contents='something2')
    fs.create_file('/file3.txt')
    os.chdir("/")
    shell = Shell()
    shell.run(f'cp file1.txt file2.txt file3.txt')
    out = capsys.readouterr().out
    assert 'is not a directory' in out

def test_cp_r_flag_not_a_dir1(fs, capsys):
    fs.create_dir('/src/subdir')
    fs.create_file('/src/file1.txt', contents='something1')
    fs.create_dir('/dst.txt')
    os.chdir('/')
    shell = Shell()
    shell.run('cp -r src dst')
    out = capsys.readouterr().out
    assert 'is not a directory' in out

def test_cp_r_flag_not_a_dir2(fs, capsys):
    fs.create_file('/file1.txt', contents='something1')
    fs.create_dir('/dst')
    os.chdir('/')
    shell = Shell()
    shell.run('cp -r file1.txt dst')
    out = capsys.readouterr().out
    assert 'is not a directory' in out