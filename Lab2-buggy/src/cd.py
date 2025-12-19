from pathlib import Path
import os
from src.resolve import Resolve

class Cd:
    def __init__(self, cwd=Path):
        self.cwd = cwd # текущая рабочая директория

    def change_dir(self, args: list[str]):
        """
        Меняет рабочую директорию в зависимости от аргумента.

        Аргументы:
            args: list[str] - список аргументов. Если пустой символ или "~" — переход в домашнюю директорию.

        Возвращает новую рабочую директорию (Path).
        """
        if len(args) < 2:
            if not args or args[0] == "~":
                new_cwd = Path.home()  # домашняя директория пользователя
            else:
                new_cwd = Resolve().resolv(pth=args[0])  # переход в указанную директорию

            if new_cwd.is_dir():
                os.chdir(new_cwd)  # меняем рабочую директорию на новую
                self.cwd = new_cwd
                return self.cwd  # передаем новую директорию обратно в main
            else:
                raise NotADirectoryError(f"{args[0]} is not a directory")
        else:
            raise IndexError("Too much arguments")