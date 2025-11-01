import os

from .DateTime import date_time

# Определяем абсолютный путь к shell.log в текущей директории src
current_dir = os.path.dirname(os.path.abspath(__file__))
shell_path = os.path.join(current_dir, "shell.log")


def log(command, no_mistake=True, name_error=""):
    """Записывает команды и ошибки в файл shell.log (который всегда находится в src)"""

    try:
        # Пробуем записать лог-файл в текущий каталог
        with open(shell_path, "a", encoding="utf-8") as shell:
            write_in_log(shell, command, no_mistake, name_error)

    except Exception as error:
        print(f"{date_time()} ERROR: {str(error)}")


def write_in_log(shell, command, no_mistake=True, name_error=""):
    time = date_time()  # запоминаем время
    shell.write(f"{time} {command}\n")  # в schell.log записываем последнюю команду

    """Проверяем на наличие/отсутствие ошибки"""
    if no_mistake is True:
        if name_error == "":
            shell.write(f"{time} INFO: The request was executed correctly\n")
        else:
            shell.write(f"{time} {name_error}\n")
    else:
        shell.write(
            f"{time} {name_error}\n"
        )  # в schell.log записываем ошибку для последней команды
