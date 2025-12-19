import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import Shell

def test_mv_and_rm(fs):
    fs.create_dir('/work')
    fs.create_file('/work/file1.txt')
    os.chdir('/work')
    shell = Shell()
    shell.run('rm file2.txt')
    assert not os.path.exists('file2.txt')

def test_rm_dir_recursive_accepted(fs, mocker, capsys):
    fs.create_dir('/work/dir1')
    fs.create_file('/work/dir1/file.txt', contents="test")
    os.chdir('/work')
    shell = Shell()
    mocker.patch("builtins.input", return_value='y')
    shell.run("rm -r dir1")
    out = capsys.readouterr().out
    assert not os.path.exists("dir1")
    assert 'Directory was deleted' in out

def test_rm_dir_recursive_cancelled(fs, mocker, capsys):
    fs.create_dir('/work/dir2')
    fs.create_file('/work/dir2/file.txt', contents="test")
    os.chdir('/work')
    shell = Shell()
    mocker.patch("builtins.input", return_value='n')
    shell.run("rm -r dir2")
    out = capsys.readouterr().out
    assert os.path.exists("dir2")
    assert 'Delete was canceled' in out