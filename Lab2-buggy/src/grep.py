import os
import re
from src.logger import make_logger

def grep(args: list[str]):
    """
    Поиск строк по регулярному выражению во всех указанных файлах и директориях
    Поддержка -r (рекурсия), -i (игнор регистра)

    Аргументы:
        args: list[str] - шаблон строки и папка, в которой нужно искать

    Исключения:
    - IndexError - если недостаточно аргументов
    """
    # обработка флагов
    recursive = False
    lower_case = False
    for arg in args:
        if arg == '-r':
            recursive = True
            args.remove(arg)
        elif arg == '-i':
            lower_case = True
            args.remove(arg)

    if len(args) < 2:
        raise IndexError("Not enough arguments. ")

    pattern = args[0]
    items = args[1:]

    # компиляция регулярного выражения
    if lower_case:
        flags = re.IGNORECASE
    else:
        flags = 0

    try:
        regexp = re.compile(pattern, flags)
    except re.error as e:
        print(f"Wrong expression: {e}")
        make_logger().error(" - wrong expression")
        return

    files = []
    for item in items:
        if os.path.isfile(item):
            files.append(item)
        elif os.path.isdir(item) and recursive:
            for root, _, filenames in os.walk(item):
                for fname in filenames:
                    files.append(os.path.join(root, fname))
        elif os.path.isdir(item) and not recursive:
            print(f"{item} is a directory, use -r")
            make_logger().error(" - directory without -r")
        elif recursive and not os.path.isdir(item):
            print(f'{item} is file, dont use -r')
            make_logger().error(" - file with -r")

    matches = False
    for file in files:
        try:
            with open(file, encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    match = regexp.search(line)
                    if match:
                        # выводим имя файла, номер строки и найденный фрагмент
                        print(f"{file}:{i}:{match.group(0).rstrip()}")
                        matches = True
        except Exception as e:
            print(f"Error with file {file}: {e}")
            make_logger().error(" - error with file")
    if not matches:
        print("No matches found")