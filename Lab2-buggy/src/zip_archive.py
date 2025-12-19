import zipfile
from pathlib import Path
from zipfile import BadZipfile


def make_zip(args: list[str]):
    """
    Архивирует указанные папки в zip-архив, имя которого задается последним аргументом.

    Аргументы:
        args: list[str] - список каталогов и имя создаваемого архива.

    Исключения:
    - IndexError, если аргументов меньше двух (нет каталогов или имени архива).
    """
    if len(args) >= 2:
        zip_name = args.pop(-1)  # имя создаваемого архива
        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf: # создаем архив
            for arg in args:
                for file in Path(arg).rglob("*"):  # Ищем файлы рекурсивно в директории
                    zipf.write(file, arcname=Path(arg).name / file.relative_to(arg))  # добавляем файл в архив
    else:
        raise IndexError("Not enough arguments")  # нет файлов или имени архива

def make_unzip(args: list[str]):
    """
    Разархивирует указанные zip-архивы в текущую рабочую директорию.

    Аргументы:
        args: list[str] - список путей к zip-архивам.

    Каждый архив из списка полностью распаковывается в текущую рабочую директорию.

    Исключения:
    - IndexError, если не передан ни один архив
    """
    if args:
        for arg in args:
            if '.zip' in arg:
                with zipfile.ZipFile(arg, "r") as zipf:
                    zipf.extractall(Path.cwd())  # извлекаем всё содержимое в текущую директорию
            else:
                raise BadZipfile(f"{args[-1]} is not a zip file")
    else:
        raise IndexError("Not enough arguments")

