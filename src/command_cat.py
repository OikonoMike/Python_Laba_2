import os
import os.path
import shlex

from .DateTime import date_time
from .logging_in_shell import log


def function_cat(command):
    """Функция для обработки команды cat [path] (просмотр файла)"""
    list_command = shlex.split(command, posix=False)  # разбиваем команду на подкоманды

    try:
        if len(list_command) == 2:
            """обрабатываем правильный ввод формата cat [path]"""
            path = list_command[1].rstrip()
            norm_path = os.path.normpath(
                os.path.expanduser(path)
            )  # нормализуем путь, учитывая, что может быть тильда(~)

            if os.path.exists(norm_path) and os.path.isfile(
                norm_path
            ):  # открываем файл по полному пути
                # Пробуем прочитать как текстовый файл
                try:
                    with open(norm_path, "r", encoding="utf-8") as file:
                        log(command, no_mistake=True, name_error="")
                        return file.read()
                except UnicodeDecodeError:
                    # Если не получилось прочитать, значит файл скорее всего бинарный
                    log(
                        command,
                        no_mistake=False,
                        name_error="ERROR: Невозможно прочитать файл. Файл является бинарным",
                    )
                    return f"{date_time()} ERROR: Невозможно прочитать файл. Файл является бинарным"

            # Дальше идёт обработка всевозможных ошибок
            elif os.path.exists(norm_path) and os.path.isdir(norm_path):
                log(
                    command,
                    no_mistake=False,
                    name_error="ERROR: Невозможно открыть файл, так как он является каталогом",
                )
                return f"{date_time()} ERROR: Невозможно открыть файл, так как он является каталогом"

            else:
                log(
                    command,
                    no_mistake=False,
                    name_error="ERROR: Данного файла нет в этом каталоге",
                )
                return f"{date_time()} ERROR: Данного файла нет в этом каталоге"

        elif len(list_command) < 2:
            """если введена только команда cat"""
            log(
                command,
                no_mistake=False,
                name_error="ERROR: ERROR: Имя файла не указано",
            )
            return f"{date_time()} ERROR: Имя файла не указано"

        else:
            log(
                command, no_mistake=False, name_error="ERROR: Неправильный формат ввода"
            )
            return f"{date_time()} ERROR: Неправильный формат ввода"

    except Exception as error:
        # Общий обработчик всех оставшихся исключений
        log(command, no_mistake=False, name_error=f"ERROR: {str(error)}")
        return f"{date_time()} ERROR: {str(error)}"
