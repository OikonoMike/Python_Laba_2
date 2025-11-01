import os
import os.path
import shlex
import shutil

from .DateTime import date_time
from .logging_in_shell import log


def function_mv(command):
    """Обработка команды mv (перемещение/переименовывание)"""
    list_command = shlex.split(command, posix=False)
    try:
        # Проверка минимального количества аргументов
        if len(list_command) < 3:
            log(
                command, no_mistake=False, name_error='ERROR: Неправильный формат ввода'
            )
            return f'{date_time()} ERROR: Неправильный формат ввода'

        # Нормализация путей источника и назначения
        normpath_for_source = os.path.normpath(os.path.expanduser(list_command[1]))
        normpath_for_destination = os.path.normpath(os.path.expanduser(list_command[2]))

        # Проверяем существование источника
        if not os.path.exists(normpath_for_source):
            log(
                command,
                no_mistake=False,
                name_error=f'ERROR: Источник {list_command[1]} не найден',
            )
            return f'{date_time()} ERROR: Источник {list_command[1]} не найден'

        # Проверка на права доступа к файлу/каталогу
        try:
            # Проверка, можем ли мы прочитать этот файл
            if os.path.isfile(normpath_for_source):
                with open(normpath_for_source, 'rb') as f:
                    f.read(1)  # для проверки достаточно прочитать первый байт файла
            elif os.path.isdir(normpath_for_source):
                # Пробуем получить список файлов директории
                os.listdir(normpath_for_source)
        except PermissionError:
            log(
                command,
                no_mistake=False,
                name_error='ERROR: Нет прав доступа для чтения источника',
            )
            return f'{date_time()} ERROR: Нет прав доступа для чтения источника'

        # Определяем конечный путь назначения
        if os.path.isdir(normpath_for_destination):
            # Если назначение - существующая директория, сохраняем исходное имя
            final_path_to_destination = os.path.join(
                normpath_for_destination, os.path.basename(normpath_for_source)
            )
        else:
            # Если назначение - путь к файлу, используем его как есть
            final_path_to_destination = normpath_for_destination

        # Защита от перемещения файла/каталога в самого себя
        if os.path.abspath(normpath_for_source) == os.path.abspath(
            final_path_to_destination
        ):
            log(
                command,
                no_mistake=False,
                name_error='ERROR: Невозможно переместить файл в самого себя',
            )
            return f'{date_time()} ERROR: Невозможно переместить файл в самого себя'

        try:
            # Перемещение файла или каталога
            shutil.move(normpath_for_source, final_path_to_destination)
            log(command, no_mistake=True, name_error="")
            return None

        except PermissionError:
            log(
                command,
                no_mistake=False,
                name_error='ERROR: Нет прав доступа для перемещения',
            )
            return f'{date_time()} ERROR: Нет прав доступа для перемещения'
        except Exception as error:
            log(command, no_mistake=False, name_error=f'ERROR: {str(error)}')
            return f'{date_time()} ERROR: {str(error)}'
    except Exception as error:
        log(command, no_mistake=False, name_error=f'ERROR: {str(error)}')
        return f'{date_time()} ERROR: {str(error)}'
