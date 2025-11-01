import os
import os.path
import shlex

from .DateTime import date_time
from .logging_in_shell import log


def function_grep(command):
    """Обработка команды grep (поиск по содержимому файлов)"""
    try:
        # Разбиваем команду на части
        command_list = shlex.split(command)

        # Проверяем, что команда имеет достаточно частей
        if len(command_list) < 3:
            log(
                command, no_mistake=False, name_error="ERROR: Неправильный формат ввода"
            )
            return f"{date_time()} ERROR: Неправильный формат ввода"

        # Флаги для опций
        recurs = False
        without_registr = False
        pattern = None
        path_to_search = None

        # Обрабатываем опции и аргументы
        i = 1  # начинаем с первого аргумента после 'grep'
        while i < len(command_list):
            current_part = command_list[i]

            # Проверяем опции
            if current_part == "-r":
                recurs = True
                i += 1
            elif current_part == "-i":
                without_registr = True
                i += 1
            elif current_part == "-ri" or current_part == "-ir":
                recurs = True
                without_registr = True
                i += 1
            else:
                # Если это не опция, то это должен быть шаблон или путь
                if pattern is None:
                    pattern = current_part
                    i += 1
                elif path_to_search is None:
                    path_to_search = current_part
                    i += 1
                else:
                    # Если есть лишние аргументы
                    log(
                        command,
                        no_mistake=False,
                        name_error="ERROR: Слишком много аргументов",
                    )
                    return f"{date_time()} ERROR: Слишком много аргументов"

        # Проверяем, чтобы были и шаблон и путь
        if pattern is None:
            log(
                command,
                no_mistake=False,
                name_error="ERROR: Не указан шаблон для поиска",
            )
            return f"{date_time()} ERROR: Не указан шаблон для поиска"

        if path_to_search is None:
            log(
                command, no_mistake=False, name_error="ERROR: Не указан путь для поиска"
            )
            return f"{date_time()} ERROR: Не указан путь для поиска"

        # Нормализуем путь
        normal_path = os.path.normpath(os.path.expanduser(path_to_search))

        # Проверяем, что путь существует
        if not os.path.exists(normal_path):
            log(
                command,
                no_mistake=False,
                name_error=f"ERROR: Путь {path_to_search} не найден",
            )
            return f"{date_time()} ERROR: Путь {path_to_search} не найден"

        # Список для хранения результатов
        search_results = []

        # Если путь - это файл
        if os.path.isfile(normal_path):
            file_results = search_in_a_single_file(
                normal_path, pattern, without_registr
            )
            if file_results:
                search_results.extend(file_results)

        # Если путь - это папка
        elif os.path.isdir(normal_path):
            if recurs:
                # Рекурсивный поиск во всех подпапках
                all_files = find_all_files(normal_path)

                # Ищем в каждом файле
                for file_path in all_files:
                    file_results = search_in_a_single_file(
                        file_path, pattern, without_registr
                    )
                    if file_results:
                        search_results.extend(file_results)
            else:
                # Поиск только в текущей папке
                for item in os.listdir(normal_path):
                    full_item_path = os.path.join(normal_path, item)
                    if os.path.isfile(full_item_path):
                        file_results = search_in_a_single_file(
                            full_item_path, pattern, without_registr
                        )
                        if file_results:
                            search_results.extend(file_results)
        else:
            log(
                command,
                no_mistake=False,
                name_error=f"ERROR: {path_to_search} не является файлом или каталогом",
            )
            return f"{date_time()} ERROR: {path_to_search} не является файлом или каталогом"

        # Формируем результат
        if search_results:
            output_lines = []
            current_file_path = None

            for result in search_results:
                file_path = result[0]  # Это полный путь к файлу
                line_number = result[1]
                line_text = result[2].rstrip()

                # Для красоты делаем путь относительным
                relative_path = os.path.relpath(file_path, os.getcwd())

                # Сравниваем полные пути, а не относительные
                if file_path != current_file_path:
                    output_lines.append(f"[{relative_path}]")
                    current_file_path = file_path

                # Добавляем номер строки и саму строку
                output_lines.append(f"{line_number} {line_text}")

            log(command, no_mistake=True, name_error="")
            return "\n".join(output_lines)
        else:
            log(command, no_mistake=True, name_error="INFO: Совпадений не найдено")
            return f"{date_time()} INFO: Совпадений не найдено"

    except PermissionError:
        log(
            command,
            no_mistake=False,
            name_error="ERROR: Нет прав доступа для чтения файлов",
        )
        return f"{date_time()} ERROR: Нет прав доступа для чтения файлов"
    except Exception as error:
        log(command, no_mistake=False, name_error=f"ERROR: {str(error)}")
        return f"{date_time()} ERROR: {str(error)}"


def find_all_files(directory_path):
    """Находит все файлы в папке и подпапках"""
    all_files = []

    try:
        # Сначала добавляем файлы из текущей папки
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)

            if os.path.isfile(item_path):
                # Если это файл - добавляем в список
                all_files.append(item_path)
            elif os.path.isdir(item_path):
                # Если это папка - ищем файлы в ней рекурсивно
                files_in_subfolder = find_all_files(item_path)
                all_files.extend(files_in_subfolder)
    except PermissionError:
        # Если нет прав доступа к папке, пропускаем её
        pass

    return all_files


def search_in_a_single_file(file_path, pattern, without_registr):
    """Поиск шаблона в одном файле"""
    search_results = []

    try:
        # Пытаемся открыть файл как текстовый
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Подготавливаем шаблон для поиска
        search_pattern = pattern
        if without_registr:
            search_pattern = pattern.lower()

        # Ищем в каждой строке
        line_number = 1
        for line in lines:
            search_line = line
            if without_registr:
                search_line = line.lower()

            # Проверяем, есть ли шаблон в строке
            if search_pattern in search_line:
                search_results.append((file_path, line_number, line))

            line_number += 1

    except UnicodeDecodeError:
        # Если файл бинарный, просто пропускаем его
        pass
    except PermissionError:
        # Если нет прав на чтение, пропускаем файл
        pass
    except Exception:
        # Любые другие ошибки - пропускаем файл
        pass

    return search_results
