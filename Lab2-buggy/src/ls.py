from pathlib import Path
from src.resolve import Resolve
import os
import datetime as dt
from stat import filemode

class Ls:
    def __init__(self, cwd=Path.cwd()):
        """
        Аргументы:
            cwd: текущий путь.
        """
        # установка текущего каталога
        self.cwd = cwd

    def list_dir(self, args: list[str]):
        """
        Выводит содержимое каталога.
        Аргументы:
            args (list[str]): флаг -l (опционально); каталоги, о которых требуется вывести информацию
        """
        # вывод файлов текущего каталога
        if len(args) == 0:
            print(*os.listdir(path=self.cwd), sep=" ")
            return None
        else:
            # режим подробного вывода
            if args[0] == '-l':
                args.remove("-l")
                # вывод подробной информации о текущем каталоге
                if len(args) == 0:
                    for pth in sorted(self.cwd.iterdir()):
                        Ls().l_flag(pth)
                    return None
                else:
                    # вывод подробной информации о нескольких каталогах
                    for arg in args:
                        pth = Resolve().resolv(arg)
                        # вывод для файлов
                        if pth.is_file():
                            print(f"{arg}:")
                            Ls().l_flag(pth)
                        else:
                            # вывод для каталогов
                            print(f"{arg}:")
                            for p in sorted(pth.iterdir()):
                                Ls().l_flag(p)
                    return None
            else:
                Ls().arg_flag(args)
                return None

    @staticmethod
    def arg_flag(args: list[str]):
        """
        Выводит содержимое для списка каталогов.
        Аргументы:
            args (list[str]): список каталогов.
        """
        # вывод по каждому каталогу
        if len(args) > 1:
            # для нескольких каталогов
            for arg in args:
                print(f"{arg}:\n", *os.listdir(path=arg), sep=" ")
            return 1
        else:
            # для одного каталога
            print(*os.listdir(path=args[0]), sep=" ")
            return 1

    @staticmethod
    def l_flag(pth: Path):
        """
        Выводит подробную информацию о файле или каталоге.
        Аргументы:
            pth (Path): путь к объекту.
        """
        st = pth.stat()
        time_change = dt.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S") # время изменения
        name = pth.name # имя
        size = st.st_size # размер
        perms = filemode(st.st_mode) # права доступа
        print(f"{perms:13} {time_change:10} {size:8} {name}")
