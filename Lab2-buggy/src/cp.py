from pathlib import Path
import shutil

def cp(args: list[str]):
    """
    Копирует файлы или каталоги по указанным аргументам.
    Аргументы:
        args (list[str]): исходные и целевой путь, опционально -r для рекурсии.
    Исключения:
        IndexError: если аргументов меньше двух.
        NotADirectoryError: если целевой не каталог.
    """

    # проверка наличия аргументов
    if len(args) < 2:
        raise IndexError("Not enough arguments")
    dst = Path(args.pop(-1))
    # копирование без -r
    if args[0] != "-r":
        if len(args) == 1:
            shutil.copy2(Path(args[0]), dst)
        else:
            # проверка директории
            if dst.is_dir():
                # копирование каждого файла/каталога
                for src in args:
                    shutil.copy2(Path(src), dst)
            else:
                raise NotADirectoryError(f"{dst} is not a directory")
    else:
        # удаление -r и рекурсивное копирование
        args.remove("-r")
        r_flag(args, dst)

def r_flag(args: list[str], dst):
    """
    Копирует каталоги рекурсивно.
    Аргументы:
        args (list[str]): исходные пути.
        dst: целевой каталог.
    Исключения:
        NotADirectoryError: если один из аргументов не каталог.
    """
    # проверка директории
    if dst.is_dir():
        for src in args:
            src1 = Path(src)
            # проверка каталога
            if src1.is_dir():
                shutil.copytree(src1, dst / src1.name, dirs_exist_ok=True) # копирование каталога
            else:
                raise NotADirectoryError(f"{src1} is not a directory. If you want copy file dont use -r")
    else:
        raise NotADirectoryError(f"{dst} is not a directory")
