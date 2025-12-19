from pathlib import Path
import shutil

def mv(args: list[str]):
    """
    Перемещает файлы или каталоги по указанным аргументам.
    Аргументы:
        args (list[str]): исходные и целевой путь.
    Исключения:
        IndexError: если аргументов меньше двух.
        NotADirectoryError: если целевой не каталог.
    """
    # проверка наличия аргументов
    if len(args) < 2:
        raise IndexError("Not enough arguments")
    dst = Path(args.pop(-1))
    # перемещение или переименовывание одиночного файла
    if len(args) == 1:
        shutil.move(Path(args[0]), dst)
        return None
    else:
        # перемещение списка
        if dst.is_dir():
            for src in args:
                shutil.move(Path(src), dst)
            return None
        else:
            raise NotADirectoryError(f"{dst} is not a directory")
