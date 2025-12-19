import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import Shell

def test_cat_normal(fs, capsys):
    fs.create_dir('/work')
    fs.create_file('/work/test.txt', contents='goose')
    os.chdir('/work')
    shell = Shell()
    shell.run('cat test.txt')
    out = capsys.readouterr().out
    assert 'goose' in out

def test_cat_not_a_file(fs, capsys):
    fs.create_dir('work')
    shell = Shell()
    shell.run('cat work')
    out = capsys.readouterr().out
    assert 'is not a file' in out

def test_cat_not_found(capsys):
    shell = Shell()
    shell.run("cat unknown_file.txt")
    out = capsys.readouterr().out
    assert 'No such file' in out