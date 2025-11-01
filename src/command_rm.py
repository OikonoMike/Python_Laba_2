import os
import os.path
import shutil
import shlex
from .DateTime import date_time
from .logging_in_shell import log


def function_rm(command):
    """Обработка функции rm (удаление файла/каталога)"""
    try:
        commands = shlex.split(command, posix=False)
        # Достаточно ли аргументов во введённой команде
        if len(commands) < 2:
            log(command, no_mistake=False, name_error='ERROR: Не указан файл или каталог для удаления')
            return f'{date_time()} ERROR: Не указан файл или каталог для удаления'
        if commands[1] == '-r':
            # обрабатываем запрос rm -r [path]
            if len(commands) < 3:
                log(command, no_mistake=False, name_error='ERROR: Не указан каталог для рекурсивного удаления')
                return f'{date_time()} ERROR: Не указан каталог для рекурсивного удаления'

            path = ' '.join(commands[2:]) # объединяем оставшиеся части для имени файла
            norm_path = os.path.normpath(os.path.expanduser(path))

            # проверка защищенных путей и для обычного удаления
            limit_path = limited_paths(command, norm_path)
            if limit_path is None:
                if os.path.exists(norm_path) and os.path.isdir(norm_path):
                    return remove_directory(command, norm_path)
                elif os.path.exists(norm_path) and os.path.isfile(norm_path):
                    log(command, no_mistake=False, name_error='ERROR: Рекурсивное удаление доступно только для каталогов')
                    return f'{date_time()} ERROR: Рекурсивное удаление доступно только для каталогов'
                else:
                    log(command, no_mistake=False, name_error=f'ERROR: Нет каталога с названием {path}')
                    return f'{date_time()} ERROR: Нет каталога с названием {path}'
            else:
                return limit_path
        else:
            path = ' '.join(commands[1:]) # объединяем оставшиеся части для имени файла
            norm_path = os.path.normpath(os.path.expanduser(path))
            # проверка защищенных путей и для обычного удаления
            limit_path = limited_paths(command, norm_path)
            if limit_path is not None:
                return limit_path

            if os.path.exists(norm_path) and os.path.isfile(norm_path):
                    log(command, no_mistake=True, name_error='')
                    os.remove(norm_path)
                    return None
            elif os.path.exists(norm_path) and os.path.isdir(norm_path):
                    log(command, no_mistake=False, name_error=f'ERROR: {path} является каталогом. Для удаления каталога используйте -r')
                    return f'{date_time()} ERROR: {path} является каталогом. Для удаления каталога используйте -r'
            else:
                log(command, no_mistake=False, name_error=f'ERROR: В каталоге нет файла {path}')
                return f'{date_time()} ERROR: В каталоге нет файла {path}'

    except Exception as error:
        log(command, no_mistake=False, name_error=f'ERROR: {str(error)}')
        return f'{date_time()} ERROR: {str(error)}'


def limited_paths(command, path):
    """Проверяет, является ли путь защищенным от удаления"""
    abs_path = os.path.abspath(path)

    # Текущий каталог
    if abs_path == os.path.abspath('.') or path == '.':
        log(command, no_mistake=False, name_error='ERROR: Нельзя удалять текущий каталог')
        return f'{date_time()} ERROR: Нельзя удалять текущий каталог'

    # Родительский каталог
    elif abs_path == os.path.abspath('..') or path == '..':
        log(command, no_mistake=False, name_error='ERROR: Нельзя удалять родительский каталог')
        return f'{date_time()} ERROR: Нельзя удалять родительский каталог'

    # Корневой каталог
    elif abs_path == os.path.abspath(os.path.expanduser('~')) or path == '~':
        log(command, no_mistake=False, name_error='ERROR: Нельзя удалять домашнюю директорию')
        return f'{date_time()} ERROR: Нельзя удалять домашнюю директорию'

    # Корневой каталог (проверка для всех ОС)
    elif (abs_path == os.path.abspath(os.sep) or path in ['/', '\\'] # проверка корневых каталогов (кроме Windows)
    or (os.name == 'nt' and len(abs_path) == 3 and abs_path.endswith(':\\'))): # проверка для Windows
        log(command, no_mistake=False, name_error='ERROR: Нельзя удалять корневой каталог')
        return f'{date_time()} ERROR: Нельзя удалять корневой каталог'

    return None # Путь не защищен => его можно удалять


def remove_directory(command, name_file):
    """Рекурсивно удаляет каталог с подтверждением"""
    print('Подтверждение')
    print(f'Элемент в "{name_file}" имеет дочерние объекты.'
          f' При продолжении все дочерние объекты будут удалены вместе с элементом.'
          f' Вы действительно хотите продолжить?')

    permission = input('[Y] Да - Y [N] Нет - N [?] Справка (значением по умолчанию является "Y"): ').strip()

    # пользователь даёт согласие на удаление каталога
    if permission == 'Y' or permission == 'y' or permission == '':
        try:
            log(command, no_mistake=True, name_error='')
            shutil.rmtree(name_file)
            return None
        except Exception as error:
            log(command, no_mistake=False, name_error=f'ERROR: {str(error)}')
            return f'{date_time()} ERROR: {str(error)}'

    # пользователь не дал согласия на удаление каталога
    elif permission == 'N' or permission == 'n':
        log(command, no_mistake=True, name_error='Операция отменена пользователем')
        return None

    # Справка с рекурсивным вызовом
    else:
        print('Справка:')
        print('Y - Да, удалить каталог и все содержимое в нём')
        print('N - Нет, отменить удаление')
        print('Enter - использовать значение по умолчанию (Y)')
        return remove_directory(command, name_file)