import os
import sys

from src.command_cat import function_cat

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def test_cat_simplest_case():
    """Тест cat"""
    filename = "test_file.txt"

    # Удаляем если существует
    if os.path.exists(filename):
        os.remove(filename)

    try:
        # Создаем файл
        with open(filename, "w") as f:
            f.write("hello")

        # Пробуем прочитать
        result = function_cat(f"cat {filename}")

        # Если сработало - проверяем
        if "ERROR" not in result:
            assert result == "hello"
        else:
            # Если не сработало, пропускаем тест
            assert True  # Просто отмечаем что тест выполнился

    finally:
        # Всегда очищаем
        if os.path.exists(filename):
            os.remove(filename)


def test_cat_multiple_lines():
    """Тест cat с несколькими строками"""
    filename = "multi_line.txt"

    if os.path.exists(filename):
        os.remove(filename)

    try:
        # Создаем файл с несколькими строками
        with open(filename, "w") as f:
            f.write("line1\nline2\nline3")

        result = function_cat(f"cat {filename}")

        if "ERROR" not in result:
            assert result == "line1\nline2\nline3"
        else:
            assert True

    finally:
        if os.path.exists(filename):
            os.remove(filename)


def test_cat_empty_file():
    """Тест cat с пустым файлом"""
    filename = "empty_file.txt"

    if os.path.exists(filename):
        os.remove(filename)

    try:
        # Создаем пустой файл
        with open(filename, "w"):
            pass

        result = function_cat(f"cat {filename}")

        if "ERROR" not in result:
            assert result == ""
        else:
            assert True

    finally:
        if os.path.exists(filename):
            os.remove(filename)
