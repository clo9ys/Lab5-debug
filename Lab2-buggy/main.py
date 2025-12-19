from gzip import BadGzipFile
from pathlib import Path
import datetime as dt, shlex
from zipfile import BadZipfile

from src.ls import Ls
from src.cat import cat
from src.cd import Cd
from src.mv import mv
from src.rm import rm
from src.cp import cp
from src.logger import make_logger
from src.help import _help
from src.zip_archive import make_zip, make_unzip
from src.tar_archive import make_tar, make_untar
from src.grep import grep

class Shell:
    """
    Основной класс командной оболочки. Отвечает за инициализацию окружения, обработку пользовательского ввода и вызов команд.
    """

    def __init__(self):
        self.cwd = Path.cwd()  # текущая рабочая директория
        self.logger = make_logger() # логгирующая функция

    def parser(self):
        """
        Основной цикл ввода и вывода. Принимает команды пользователя и передаёт их в обработку.
        """
        while True:
            try:
                line = input(f"{self.cwd}> ")  # выводим текущую папку и запрашиваем команду
            except (EOFError, KeyboardInterrupt):
                print()
                break
            self.run(line) # вызываем run() для последующей обработки введенной команды

    @staticmethod
    def add_history(line: str):
        """
        Сохраняет команду и время ее ввода в файл .history.
        Аргументы:
            line - введенная команда и аргументы (флаг, файлы, каталоги)
        """
        with open(".history", "a", encoding="utf-8") as f:
            time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{time}] {line}\n")

    def run(self, line: str):
        """
        Вызывает парсер, ведет запись лога, вызывает соответствующую функцию.

        Аргументы:
             line - введенная команда и аргументы (флаг, файлы, каталоги)
        """
        Shell().add_history(line)
        self.logger.info(f" - {line}") # запись в лог о вызове команды

        # разбиваем строку на команду и аргументы
        cmd, *args = shlex.split(line.strip())

        try:
            match cmd:
                case "ls":
                    Ls(self.cwd).list_dir(args)
                case "cd":
                    self.cwd = Cd(self.cwd).change_dir(args)
                case "cat":
                    cat(args)
                case "mv":
                    mv(args)
                case "rm":
                    rm(args)
                case "cp":
                    cp(args)
                case "--help":
                    _help(args)
                case "zip":
                    make_zip(args)
                case "unzip":
                    make_unzip(args)
                case "tar":
                    make_tar(args)
                case "untar":
                    make_untar(args)
                case "grep":
                    grep(args)
                case "exit":
                    raise SystemExit(0)  # завершение работы
                case _:
                    print(f"Unknown command: {cmd}. Use --help")
                    self.logger.error(f" - unknown command")

        # обработка ошибок и запись их в лог
        except (FileNotFoundError, FileExistsError):
            print(f"No such file or directory")
            self.logger.error(f" - wrong argument")
        except NotADirectoryError as err:
            print(err)
            self.logger.error(" - wrong argument")
        except PermissionError as err:
            print(err)
            self.logger.error(f" - user don't have enough permissions")
        except IndexError as err:
            print(err)
            self.logger.error(f" - {err}")
        except IsADirectoryError as err:
            print(err)
            self.logger.error(f" - {err}")
        except BadZipfile as err:
            print(err)
            self.logger.error(f" - {err}")
        except BadGzipFile as err:
            print(err)
            self.logger.error(f" - {err}")

if __name__ == "__main__":
    Shell().parser()
