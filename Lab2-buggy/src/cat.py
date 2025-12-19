from src.resolve import Resolve

def cat(args: list[str]):
    """
    Функция для вывода содержимого файлов.

    Аргументы:
        args (list[str]): список имён файлов (str), которые нужно открыть и вывести на экран.

    Исключения:
    - IndexError: если список аргументов пуст.
    - FileNotFoundError: если файл не найден или не является файлом.
    """
    # проверяем, что аргументы переданы
    if not args:
        raise IndexError("Not enough arguments")

    # для каждого переданного файла
    for arg in args:
        file1 = Resolve().resolv(pth=arg)
        # проверка существования файла и является ли он файлом
        if not file1.exists():
            raise FileNotFoundError("No such file")
        if not file1.is_file():
            raise IsADirectoryError(f"{arg} is not a file")
        # открываем файл и выводим его содержимое
        with open(file1, "r", encoding="UTF-8") as f:
            print(f"{arg}:\n\n", f.read())
    return 0
