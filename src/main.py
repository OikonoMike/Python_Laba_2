import os, os.path
from DateTime import date_time
from command_ls import function_ls
from command_cd import function_cd
from command_cat import function_cat

def main():
    command = input(f'{date_time()} ')
    list_commands = ['ls', 'cd', 'cat', 'mv', 'cp', 'rm']
    while command != 'exit':
        if command.split()[0] in list_commands:
            if 'ls' in command:
                print(date_time(), function_ls(command))
                print(os.system(command))
            elif 'cd' in command:
                print(date_time(), function_cd(command))
            elif 'cat' in command:
                print(date_time(), function_cat(command))
            elif 'mv' in command:
                print(date_time(), )
        else:
            print(date_time(), 'ERROR: Неизвестная команда')
        command = input(f'{date_time()} ')


main()