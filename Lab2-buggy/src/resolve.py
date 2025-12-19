from pathlib import Path
import os

class Resolve:
    def __init__(self):
        self.cwd = Path.cwd()

    def resolv(self, pth: str) -> Path:
        #Функция возврата абсолютного пути
        if not os.path.isabs(pth):
            return (self.cwd / pth).expanduser().resolve()

        return Path(pth).expanduser().resolve()