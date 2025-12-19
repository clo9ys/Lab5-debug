import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import Shell

def test_cd_dirs(fs):
    fs.create_dir('/work/new_dir')
    os.chdir('/work')
    shell = Shell()
    shell.run('cd new_dir')
    assert shell.cwd.name == 'new_dir'

@pytest.mark.parametrize("home_dir", ["~", ""])
def test_cd_home(fs, home_dir):
    fs.create_dir('/home/userhome')
    os.environ["HOME"] = "/home/userhome"
    os.chdir('/home/userhome')
    shell = Shell()
    shell.run(f'cd {home_dir}')
    assert str(shell.cwd) == '/home/userhome'

@pytest.mark.parametrize("is_file", ["file1.txt", "file2.py"])
def test_cd_not_a_directory_error(is_file, capsys):
    shell = Shell()
    shell.run(f'cd {is_file}')
    out = capsys.readouterr().out
    assert "is not a directory" in out

def test_cd_too_much_args(capsys):
    shell = Shell()
    shell.run(f'cd src tests')
    out = capsys.readouterr().out
    assert "Too much arguments" in out