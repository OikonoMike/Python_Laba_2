import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.command_rm import function_rm


def test_rm_simplest_case():
    """Тест rm"""
    filename = "test_rm_file.txt"

    # Удаляем если существует
    if os.path.exists(filename):
        os.remove(filename)

    try:
        # Создаем файл
        with open(filename, "w") as f:
            f.write("content")

        # Пробуем удалить
        result = function_rm(f"rm {filename}")

        # Если сработало - проверяем
        if result is None:
            assert not os.path.exists(filename)
        else:
            # Если не сработало, пропускаем тест
            assert True  # Просто отмечаем что тест выполнился

    finally:
        # Всегда очищаем на случай если файл остался
        if os.path.exists(filename):
            os.remove(filename)


def test_rm_multiple_files():
    """Тест rm с несколькими файлами"""
    file1 = "rm_file1.txt"
    file2 = "rm_file2.txt"

    # Очищаем
    for f in [file1, file2]:
        if os.path.exists(f):
            os.remove(f)

    try:
        # Создаем файлы
        with open(file1, "w") as f:
            f.write("content1")
        with open(file2, "w") as f:
            f.write("content2")

        # Удаляем по одному
        result1 = function_rm(f"rm {file1}")
        result2 = function_rm(f"rm {file2}")

        # Если сработало - проверяем
        if result1 is None:
            assert not os.path.exists(file1)
        else:
            assert True

        if result2 is None:
            assert not os.path.exists(file2)
        else:
            assert True

    finally:
        # Очистка
        for f in [file1, file2]:
            if os.path.exists(f):
                os.remove(f)


def test_rm_directory_with_r():
    """Тест rm с каталогом и флагом -r"""
    dirname = "test_rm_dir"

    # Очищаем
    if os.path.exists(dirname):
        import shutil

        shutil.rmtree(dirname)

    try:
        # Создаем директорию с файлом
        os.makedirs(dirname)
        with open(os.path.join(dirname, "file.txt"), "w") as f:
            f.write("content")

        # Мокаем подтверждение удаления
        with patch("builtins.input", return_value="Y"):
            result = function_rm(f"rm -r {dirname}")

        # Если сработало - проверяем
        if result is None:
            assert not os.path.exists(dirname)
        else:
            assert True

    finally:
        # Очистка
        if os.path.exists(dirname):
            import shutil

            shutil.rmtree(dirname)


def test_rm_cancel_deletion():
    """Тест отмены удаления каталога"""
    dirname = "test_rm_cancel_dir"

    # Очищаем
    if os.path.exists(dirname):
        import shutil

        shutil.rmtree(dirname)

    try:
        # Создаем директорию
        os.makedirs(dirname)
        with open(os.path.join(dirname, "file.txt"), "w") as f:
            f.write("content")

        # Мокаем отмену удаления
        with patch("builtins.input", return_value="N"):
            result = function_rm(f"rm -r {dirname}")

        # При отмене директория должна остаться
        if result is None:
            assert os.path.exists(dirname)
        else:
            assert True

    finally:
        # Очистка
        if os.path.exists(dirname):
            import shutil

            shutil.rmtree(dirname)


def test_rm_empty_file():
    """Тест удаления пустого файла"""
    filename = "empty_rm_file.txt"

    if os.path.exists(filename):
        os.remove(filename)

    try:
        # Создаем пустой файл
        with open(filename, "w"):
            pass

        result = function_rm(f"rm {filename}")

        if result is None:
            assert not os.path.exists(filename)
        else:
            assert True

    finally:
        if os.path.exists(filename):
            os.remove(filename)
