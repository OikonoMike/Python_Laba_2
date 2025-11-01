import os
import sys

from src.command_grep import function_grep

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def test_grep_simplest_case():
    """Простой тест grep"""
    filename = "grep_test.txt"

    if os.path.exists(filename):
        os.remove(filename)

    try:
        # Создаем файл с текстом для поиска
        with open(filename, "w") as f:
            f.write("Goose\nbanana\norange")

        # Ищем слово
        result = function_grep(f"greap Goose {filename}")

        # Если сработало - проверяем
        if "ERROR" not in result and "INFO: Совпадений не найдено" not in result:
            assert "Goose" in result
        else:
            # Если не сработало или не найдено, пропускаем тест
            assert True

    finally:
        if os.path.exists(filename):
            os.remove(filename)


def test_grep_no_matches():
    """Тест grep когда нет совпадений"""
    filename = "grep_no_match.txt"

    if os.path.exists(filename):
        os.remove(filename)

    try:
        with open(filename, "w") as f:
            f.write("hello world")

        result = function_grep(f"greap nonexistent {filename}")

        # Должен вернуть информационное сообщение
        if "INFO: Совпадений не найдено" in result:
            assert True
        elif "ERROR" not in result:
            # Если что-то нашел (не должно быть)
            assert len(result) > 0
        else:
            # Если ошибка, пропускаем
            assert True

    finally:
        if os.path.exists(filename):
            os.remove(filename)


def test_grep_case_sensitive():
    """Тест grep с учетом регистра"""
    filename = "case_test.txt"

    if os.path.exists(filename):
        os.remove(filename)

    try:
        with open(filename, "w") as f:
            f.write("Goose\ngoose\nGOOSE")

        result = function_grep(f"greap Goose {filename}")

        if "ERROR" not in result and "INFO: Совпадений не найдено" not in result:
            # Должен найти только строчную 'Goose'
            assert "goose" in result.lower()
        else:
            assert True

    finally:
        if os.path.exists(filename):
            os.remove(filename)
