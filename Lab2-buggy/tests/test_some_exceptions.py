import os, pytest, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import Shell

def test_unknown_command(fs, capsys):
    fs.create_dir('/work')
    os.chdir('/work')
    shell = Shell()
    shell.run("top-it")
    out = capsys.readouterr().out
    assert "Unknown command" in out

@pytest.mark.parametrize("cmd", ["cat", "rm", "mv", "cp", "rm -r", "zip", "tar", "unzip", "untar"])
def test_not_enough_args(fs, capsys, cmd):
    fs.create_dir('/work')
    os.chdir('/work')
    shell = Shell()
    shell.run(cmd)
    out = capsys.readouterr().out
    assert 'Not enough arguments' in out
