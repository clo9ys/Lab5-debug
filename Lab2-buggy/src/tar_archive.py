import tarfile
from gzip import BadGzipFile
from pathlib import Path

def make_tar(args: list[str]):
    """
    Архивирует указанные папки в архив формата tar.gz, имя которого задается последним аргументом.

    Аргументы:
        args: list[str] - список каталогов и имя создаваемого архива.

    Исключения:
    - IndexError, если аргументов меньше двух (нет каталогов или имени архива).
    """
    if len(args) >= 2:
        tar_name = args.pop(-1)  # имя создаваемого архива
        with tarfile.open(tar_name, "w:gz") as tarf: # создаем архив
            for arg in args:
                for file in Path(arg).rglob("*"):  # ищем файлы рекурсивно в директории
                    tarf.add(file, arcname=Path(arg).name / file.relative_to(arg))  # добавляем файл в архив
    else:
        raise IndexError("Not enough arguments")  # не указаны файлы или имя архива

def make_untar(args: list[str]):
    """
    Разархивирует указанные tar-архивы в текущую рабочую директорию.

    Аргументы:
        args: list[str] - список путей к tar-архивам.

    Каждый архив из списка полностью распаковывается в текущую рабочую директорию.
    """
    if args:
        for arg in args:
            if '.tar.gz' in arg:
                with tarfile.open(arg, "r:gz") as tarf:
                    tarf.extractall(Path.cwd())  # извлекаем всё содержимое в текущую директорию
            else:
                raise BadGzipFile(f"{args[-1]} is not a gzip file")
    else:
        raise IndexError("Not enough arguments")