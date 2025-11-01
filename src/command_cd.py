import os
import os.path
import shlex

from .DateTime import date_time
from .logging_in_shell import log


def function_cd(command):
    """Обработка команды cd"""
    try:
        if os.name == "nt":  # Заменяем слеши для обработки путей Windows
            command = command.replace("\\", "/")
        command_list = shlex.split(command)

        # Проверка, что указан путь для перехода
        if len(command_list) >= 2:
            path = command_list[1]

            """Обработка специальных случаев"""

            # Текущая директория (остаемся на месте)
            if len(path) == 1 and path == ".":
                log(command, no_mistake=True, name_error="")
                return None
            # Родительский каталог
            elif path == ".." and len(path) == 2:
                log(command, no_mistake=True, name_error="")
                os.chdir("..")
                return None
            # Домашний каталог
            elif path == "~":
                log(command, no_mistake=True, name_error="")
                os.chdir(os.path.expanduser("~"))
                return None
            # Проверяем, что пользователь не ввёл, например, .......
            elif len(path) > 2 and all(point == "." for point in path):
                log(
                    command,
                    no_mistake=False,
                    name_error=f"ERROR: Каталог {path} не найден",
                )
                return f"{date_time()} ERROR: Каталог {path} не найден"

            # Обычный путь к директории
            else:
                # Проверка существования и типа (должна быть директорией)
                if os.path.exists(path) and os.path.isdir(path):
                    log(command, no_mistake=True, name_error="")
                    os.chdir(path)
                    return None
                else:
                    log(
                        command,
                        no_mistake=False,
                        name_error=f"ERROR: Каталог {path} не найден",
                    )
                    return f"{date_time()} ERROR: Каталог {path} не найден"
        else:
            log(command, no_mistake=False, name_error="ERROR: Путь не указан")
            return f"{date_time()} ERROR: Путь не указан"

    except Exception as error:
        log(command, no_mistake=False, name_error=f"ERROR: {str(error)}")
        return f"{date_time()} ERROR: {str(error)}"
