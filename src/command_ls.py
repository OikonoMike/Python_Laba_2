import os
import os.path
import stat
import shlex
from .logging_in_shell import log
from datetime import datetime
from .DateTime import date_time
from .command_cd import function_cd


def function_ls(command):
    """Обработка функции ls"""
    try:
        command_list = shlex.split(command, posix=False)
    except Exception as error:
        log(command, no_mistake=False, name_error=f'ERROR: Неправильный формат ввода команды: {str(error)}')
        return f'{date_time()} ERROR: Неправильный формат ввода команды: {str(error)}'

    original_directory = os.getcwd() # сохраняем оригинальный катало, чтобы потом в него возвращаться
    try:
        # запрос вида ls
        if len(command_list) == 1:
            log(command, no_mistake=True, name_error='')
            list_files = os.listdir()

            # Если каталог, в котором мы находимся, пустой
            if len(list_files) == 0:
                log(command, no_mistake=True, name_error='')
                return 'Пустой каталог'
            else:
                log(command, no_mistake=True, name_error='')
                return '\n'.join(list_files)

        # запрос вида ls [path] или ls -l
        elif len(command_list) == 2:
            # если вида ls -l
            if command_list[1] == '-l':
                log(command, no_mistake=True, name_error='')
                return function_minus_l(command)
            # если вида ls [path]
            elif command_list[1] != '-l':
                result_cd = function_cd(f'cd {command_list[1]}') # переходим по пути, который указал пользователь
                if result_cd is None:
                    result = '\n'.join(os.listdir())
                    log(command, no_mistake=True, name_error='')
                    os.chdir(original_directory)
                    return result
                else:
                    return result_cd # возвращаем ошибку

            else:
                log(command, no_mistake=False, name_error='ERROR: Неправильный формат ввода')
                return f'{date_time()} ERROR: Неправильный формат ввода'

        elif len(command_list) == 3:
            if command_list[2] == '-l':
                result_cd = function_cd(f'cd {command_list[1]}')  # переходим по пути, который указал пользователь

                if result_cd is None:
                    # если cd не выдал ошибки
                    result_l = function_minus_l(command) # сохраняем файлы из каталога, в который мы перешли
                    os.chdir(original_directory) # возвращаемся в исходный каталог
                    log(command, no_mistake=True, name_error='')
                    return result_l # выводим результат

                else:
                    # Если есть ошибка при переходе
                    return result_cd # возвращаем ошибку

            else:
                log(command, no_mistake=False, name_error='ERROR: Неправильный формат ввода')
                return f'{date_time()} ERROR: Неправильный формат ввода'

        else:
            log(command, no_mistake=False, name_error='ERROR: Неправильный формат ввода')
            return f'{date_time()} ERROR: Неправильный формат ввода'

    except Exception as error:
        os.chdir(original_directory)
        log(command, no_mistake=False, name_error=f'ERROR: {str(error)}')
        return f'{date_time()} ERROR: {str(error)}'


def function_minus_l(command):
    """Выводит подробный список файлов и каталогов"""
    files = os.listdir()
    if not files:
        return 'Пустой каталог'

    result = [f'\n Каталог:  {os.getcwd()}\n',
              '   Mode            LastWriteTime                Length       Name',
              '  ------           -------------                ------     --------']

    for file in os.listdir():
        full_path = os.path.join(os.getcwd(), file)
        os_stat = os.stat(full_path)

        size_file = os_stat.st_size
        if os.path.isdir(full_path):
            size_file = '    '
        write_time = datetime.fromtimestamp(os_stat.st_mtime)

        mode = stat.filemode(os_stat.st_mode)
        result.append(f'{mode}     {write_time: %d.%m.%Y %H:%M:%S}              {size_file}    {file}')
    log(command, no_mistake=True, name_error='')
    return '\n'.join(result)