import os
import os.path
import shlex
import shutil

from .DateTime import date_time
from .logging_in_shell import log


def function_cp(command):
    """Обрабатывает команду cp (копирование)"""
    command_list = shlex.split(command)

    try:
        if len(command_list) < 3:
            log(
                command, no_mistake=False, name_error="ERROR: Неправильный формат ввода"
            )
            return f"{date_time()} ERROR: Неправильный формат ввода"

        # команда формата cp -r <directory1> <directory2> (рекурсивное копирование каталога)
        if command_list[1] == "-r":
            if len(command_list) < 4:
                log(
                    command,
                    no_mistake=False,
                    name_error="ERROR: Не указан источник и/или каталог для рекурсивного копирования",
                )
                return f"{date_time()} ERROR: Не указан источник и/или каталог для рекурсивного копирования"

            normpath_for_source = os.path.normpath(os.path.expanduser(command_list[2]))
            if os.path.isdir(normpath_for_source):
                normpath_for_destination = os.path.normpath(
                    os.path.expanduser(command_list[3])
                )

                if not os.path.exists(normpath_for_source):
                    log(
                        command,
                        no_mistake=False,
                        name_error=f"ERROR: ERROR: Каталога {command_list[2]} не найдено",
                    )
                    return f"{date_time()} ERROR: Каталога {command_list[2]} не найдено"
                try:
                    # Если назначение уже существует, то мы его удаляем и записываем заново
                    if os.path.exists(normpath_for_destination):
                        # Удаляем существующую директорию перед копированием
                        shutil.rmtree(normpath_for_destination)

                    shutil.copytree(normpath_for_source, normpath_for_destination)
                    log(command, no_mistake=True, name_error="")
                    return None

                except PermissionError:
                    log(
                        command,
                        no_mistake=False,
                        name_error="ERROR: Нет прав доступа для копирования",
                    )
                    return f"{date_time()} ERROR: Нет прав доступа для копирования"

                except Exception as error:
                    log(command, no_mistake=False, name_error=f"ERROR: {str(error)}")
                    return f"{date_time()} ERROR: {str(error)}"
            else:
                log(
                    command,
                    no_mistake=False,
                    name_error="ERROR: Опция -r поддерживается только для копирования каталогов",
                )
                return f"{date_time()} ERROR: Опция -r поддерживается только для копирования каталогов"

        # Обработка копирования файлов (без опции -r)
        else:
            normpath_for_source = os.path.normpath(os.path.expanduser(command_list[1]))
            normpath_for_destination = os.path.normpath(
                os.path.expanduser(command_list[2])
            )

            if not os.path.exists(normpath_for_source):
                log(
                    command,
                    no_mistake=False,
                    name_error=f"ERROR: Файла {command_list[1]} не найдено",
                )
                return f"{date_time()} ERROR: Файла {command_list[1]} не найдено"

            if os.path.isdir(normpath_for_source):
                log(
                    command,
                    no_mistake=False,
                    name_error="ERROR: Для копирования каталога нужно использовать опцию -r",
                )
                return f"{date_time()} ERROR: Для копирования каталога нужно использовать опцию -r"

            if not os.path.isfile(normpath_for_source):
                log(
                    command,
                    no_mistake=False,
                    name_error=f"ERROR: {command_list[1]} не является файлом",
                )
                return f"{date_time()} ERROR: {command_list[1]} не является файлом"

            # Определяем путь назначения
            if os.path.isdir(
                normpath_for_destination
            ):  # Если назначение - каталог, то сохраняем исходное имя файла
                final_path_to_destination = os.path.join(
                    normpath_for_destination, os.path.basename(normpath_for_source)
                )
            else:  # Если назначение - путь к файлу, используем его как есть
                final_path_to_destination = normpath_for_destination

            # Проверяем, что источник не является назначением (не копируется сама в себя)
            if os.path.abspath(normpath_for_source) == os.path.abspath(
                final_path_to_destination
            ):
                log(
                    command,
                    no_mistake=False,
                    name_error="ERROR: Невозможно скопировать файл в самого себя",
                )
                return f"{date_time()} ERROR: Невозможно скопировать файл в самого себя"

            # Копирование файла
            try:
                shutil.copy2(
                    normpath_for_source, final_path_to_destination
                )  # Копирование файла с сохранением метаданных
                log(command, no_mistake=True, name_error="")
                return None
            except PermissionError:
                log(
                    command,
                    no_mistake=False,
                    name_error="ERROR: Нет прав доступа для копирования",
                )
                return f"{date_time()} ERROR: Нет прав доступа для копирования"
            except Exception as error:
                log(command, no_mistake=False, name_error=f"ERROR: {str(error)}")
                return f"{date_time()} ERROR: {str(error)}"

    except Exception as error:
        log(command, no_mistake=False, name_error=f"ERROR: {str(error)}")
        return f"{date_time()} ERROR: {str(error)}"
