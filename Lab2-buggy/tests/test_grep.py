from src.grep import grep

def test_grep_basic(fs, capsys):
    fs.create_file('/file.txt', contents='top-it\nsamir\ngoose\n')
    grep(['samir', '/file.txt'])
    out = capsys.readouterr().out
    assert '/file.txt:2:samir' in out

def test_grep_regex(fs, capsys):
    fs.create_file('/file.txt', contents='peter123\nzhabin45\ngoose\n987fiit\n')
    grep([r'\d+[a-z]+', '/file.txt'])
    out = capsys.readouterr().out
    assert '/file.txt:1:123' not in out
    assert '/file.txt:4:987fiit' in out

def test_grep_ignore_case(fs, capsys):
    fs.create_file('/file.txt', contents='Hello\nhello\nHELLO\nhi\n')
    grep(['-i', 'hello', '/file.txt'])
    out = capsys.readouterr().out
    assert '/file.txt:1:Hello' in out
    assert '/file.txt:2:hello' in out
    assert '/file.txt:3:HELLO' in out

def test_grep_recursive(fs, capsys):
    fs.create_dir('/dir')
    fs.create_file('/dir/file1.txt', contents='num42\nnum67\n')
    fs.create_file('/dir/file2.txt', contents='num52\n')
    grep(['-r', r'num\d+', '/dir'])
    out = capsys.readouterr().out
    assert '/dir/file1.txt:1:num42' in out
    assert '/dir/file1.txt:2:num67' in out
    assert '/dir/file2.txt:1:num52' in out

def test_grep_regex_group(fs, capsys):
    fs.create_file('/goose.txt', contents='id-001\nid-002\nnone\n')
    grep([r'id-(\d+)', '/goose.txt'])
    out = capsys.readouterr().out
    assert '/goose.txt:1:id-001' in out
    assert '/goose.txt:2:id-002' in out

def test_grep_no_match(fs, capsys):
    fs.create_file('/z.txt', contents='aaa\nbbb\nccc\n')
    grep(['notfound', '/z.txt'])
    out = capsys.readouterr().out.strip()
    assert out == 'No matches found'

