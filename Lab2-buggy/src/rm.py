from src.mv import mv
from pathlib import Path
from src.logger import make_logger

def rm(args: list[str]):
    """
    Перемещает файлы или директории в корзину.
    Аргументы:
        args (list[str]): пути файлов или каталога, опционально -r для рекурсии.
    Исключения:
        IndexError: если аргументов нет.
        IsADirectoryError, NotADirectoryError, PermissionError: если ошибки при удалении.
    """
    # создание папки .trash при ее отсутствии
    trash = Path(".trash")
    trash.mkdir(exist_ok=True)
    # проверка наличия аргументов
    if len(args) < 1:
        raise IndexError("Not enough arguments")
    # удаление файла
    if args[0] != "-r":
        # для нескольких файлов
        for src in args:
            src1 = Path(src)
            if src1.is_file():
                mv([src1, ".trash"])  # перенос файла в корзину
            else:
                raise IsADirectoryError(f"{src} is not a file, if you want remove a directory use -r")
    else:
        # удаление каталога
        args.remove("-r")
        if args:
            r_flag(args[0])
        else:
            raise IndexError("Not enough arguments")

def r_flag(src):
    """
    Перемещает директорию в корзину с подтверждением.
    Аргументы:
        src (str): путь каталога.
    Исключения:
        NotADirectoryError, PermissionError, если удалить нельзя.
    """
    src1 = Path(src)
    # проверка корня
    if not is_root(src1):
        if src1.is_dir():
            while True:
                answ = input(f"Delete directory {src}? [y/n]: ").lower() # запрос подтверждения удаления пользователем
                if answ == "y":
                    # если удаление подтверждено
                    mv([src1, ".trash"])
                    print("Directory was deleted")
                    make_logger().info("Directory was deleted") # записываем в лог
                    break
                elif answ == "n":
                    # удаление отклонено
                    print("Delete was canceled")
                    make_logger().info("Delete was canceled") # записываем в лог
                    break
                else:
                    print("Wrong answer print 'y' or 'n'")
        else:
            raise NotADirectoryError(f"{src} is not a directory, if you want remove a file dont use -r")
    else:
        raise PermissionError(f"You cant remove this directory: {src1}")

def is_root(path: Path) -> bool:
    """
    Проверяет, является ли путь корнем либо текущим рабочим каталогом.
    Аргументы:
        path (Path): путь.
    Возвращает:
        bool: True — если путь корневой, иначе False.
    """
    # проверка корня
    path = path.resolve()
    if (str(path) == "/" or (path.parent == path and path.drive) or
        (path == Path.cwd().parent.resolve()) or (path == Path.cwd().resolve())):
        return True
    return False
