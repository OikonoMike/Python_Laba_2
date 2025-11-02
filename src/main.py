import os
import os.path

from .command_cat import function_cat
from .command_cd import function_cd
from .command_cp import function_cp
from .command_ls import function_ls
from .command_mv import function_mv
from .command_rm import function_rm
from .command_grep import function_grep
from .logging_in_shell import log
from .DateTime import date_time


def main():
    """Главная функция выполнения"""
    try:
        command = input(f"{os.getcwd()}> ").rstrip()
        list_commands = [
            "ls",
            "cd",
            "cat",
            "mv",
            "cp",
            "rm",
            "grep",
        ]  # список из команд, поддерживаемых этой программой
        while command != "exit":  # для выхода из программы нужно будет вписать exit
            try:
                if command.strip() == "":  # проверка на пустой ввод
                    command = input(f"{os.getcwd()}> ").rstrip()
                    continue
                first_command = command.split()[
                    0
                ]  # смотрим по первому слову, который ввёл пользователь
                if first_command in list_commands:
                    if first_command == "ls":
                        original_directory = (
                            os.getcwd()
                        )  # сохраняем исходную директорию
                        print(function_ls(command))
                        os.chdir(
                            original_directory
                        )  # после выполнения ls возвращаемся в исходную директорию
                    elif first_command == "cd":
                        cd = function_cd(command)
                        if (
                            cd is not None
                        ):  # если не ошибка, то продолжаем вводить команды
                            print(cd)  # если ошибка, то выводим ошибку
                    elif first_command == "cat":
                        cat = function_cat(command)
                        print(cat)  # выводим содержимое, либо ошибку
                    elif first_command == "mv":
                        mv = function_mv(command)
                        if (
                            mv is not None
                        ): # если не ошибка, то продолжаем вводить команды
                            print(mv) # если ошибка, то выводим ошибку
                    elif first_command == "rm":
                        rm = function_rm(command)
                        if (
                            rm is not None
                        ):  # если не ошибка, то продолжаем вводить команды
                            print(rm)  # если ошибка, то выводим ошибку
                    elif first_command == "cp":
                        cp = function_cp(command)
                        if (
                            cp is not None
                        ):  # если не ошибка, то продолжаем вводить команды
                            print(cp)  # если ошибка, то выводим ошибку
                    elif first_command == "grep":
                        grep = function_grep(command)
                        if (
                            grep is not None
                        ): # если не ошибка, то продолжаем вводить команды
                            print(grep) # если ошибка, то выводим ошибку
                else:
                    print(date_time(), "ERROR: Неизвестная команда")
                    # Логируем неизвестную команду
                    log(command, no_mistake=False, name_error='ERROR: Неизвестная команда')
                command = input(f"{os.getcwd()}> ").rstrip()
            except KeyboardInterrupt:
                break
            except Exception as error:
                print(f"{date_time()} ERROR: {str(error)}")
                log(command, no_mistake=False, name_error=f"ERROR: {str(error)}")
    except Exception as error:
        print(f"{date_time()} ERROR: {str(error)}")
        log("main", no_mistake=False, name_error=f"ERROR: {str(error)}")


if __name__ == "__main__":
    main()
