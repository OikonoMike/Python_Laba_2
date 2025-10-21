import os
import os.path


def function_cd(command):
    command_list = command.split()
    return os.getcwd()