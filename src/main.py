import os, os.path
from .DateTime import date_time
from .command_ls import function_ls
from .command_cd import function_cd
from .command_cat import function_cat
from .command_rm import function_rm
from .command_mv import function_mv
from .command_cp import function_cp

def main():
    """Главная функция выполнения"""
    try:
        command = input(f'{os.getcwd()}> ').rstrip()
        list_commands = ['ls', 'cd', 'cat', 'mv', 'cp', 'rm'] # список из команд, поддерживаемых этой программой
        while command != 'exit': # для выхода из программы нужно будет вписать exit
            try:
                if command.strip() == '': # проверка на пустой ввод
                    command = input(f'{os.getcwd()}> ').rstrip()
                    continue
                first_command = command.split()[0] # смотрим по первому слову, который ввёл пользователь
                if first_command in list_commands:
                    if first_command == 'ls':
                        original_directory = os.getcwd() # сохраняем исходную директорию
                        print(function_ls(command))
                        os.chdir(original_directory) # после выполнения ls возвращаемся в исходную директорию
                    elif first_command == 'cd':
                        cd = function_cd(command)
                        if cd is not None: # если не ошибка, то продолжаем вводить команды
                            print(cd) # если ошибка, то выводим ошибку
                    elif first_command == 'cat':
                        cat = function_cat(command)
                        print(cat) # выводим содержимое, либо ошибку
                    elif first_command == 'mv':
                        print(function_mv(command))
                    elif first_command == 'rm':
                        rm = function_rm(command)
                        if rm is not None: # если не ошибка, то продолжаем вводить команды
                            print(rm) # если ошибка, то выводим ошибку
                    elif first_command =='cp':
                        cp = function_cp(command)
                        if cp is not None: # если не ошибка, то продолжаем вводить команды
                            print(cp) # если ошибка, то выводим ошибку
                else:
                    print(date_time(), 'ERROR: Неизвестная команда')
                command = input(f'{os.getcwd()}> ').rstrip()
            except KeyboardInterrupt:
                break
            except Exception as error:
                print(f'{date_time()} ERROR: {str(error)}')
    except Exception as error:
        print(f'{date_time()} ERROR: {str(error)}')


if __name__ == "__main__":
    main()