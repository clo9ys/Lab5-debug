import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import Shell

def test_ls_without_args(fs, capsys):
    fs.create_dir('/work')
    fs.create_file('/work/file1.txt')
    os.chdir('/work')
    shell = Shell()
    shell.run('ls')
    out = capsys.readouterr().out
    assert 'file1.txt' in out

def test_ls_with_dir(fs, capsys):
    fs.create_dir('/work')
    fs.create_file('/work/file1.txt')
    os.chdir('/')
    shell = Shell()
    shell.run('ls work')
    out = capsys.readouterr().out
    assert 'file1.txt' in out

def test_ls_with_l_flag(fs, capsys):
    fs.create_dir('/work')
    fs.create_file('/work/file1.txt', contents="top-it")
    os.chdir('/work')
    shell = Shell()
    shell.run('ls -l')
    out = capsys.readouterr().out
    assert "file1.txt" in out
    assert "rw" in out or "--" in out
    assert "file1.txt" in out
    assert "6" in out
    lines = out.strip().split("\n")
    for line in lines:
        assert len(line.split()) >= 4

def test_ls_with_dir_l_flag(fs, capsys):
    fs.create_dir('/work')
    fs.create_file('/work/file1.txt', contents="top-it")
    os.chdir('/')
    shell = Shell()
    shell.run('ls -l work')
    out = capsys.readouterr().out
    assert "file1.txt" in out
    assert "rw" in out or "--" in out
    assert "file1.txt" in out
    assert "6" in out
    lines = out.strip().split("\n")
    for line in lines:
        assert len(line.split()) >= 1