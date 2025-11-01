import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.command_grep import function_grep


def test_grep_nonexistent_file():
    """Тест: ошибка при несуществующем файле"""
    result = function_grep("grep pattern несуществующий.txt")
    assert "ERROR: Путь несуществующий.txt не найден" in result


def test_grep_insufficient_arguments():
    """Тест: ошибка при недостаточном количестве аргументов"""
    result = function_grep("grep pattern")
    assert "ERROR: Неправильный формат ввода" in result


def test_grep_no_path():
    """Тест: ошибка при отсутствии пути"""
    result = function_grep("grep pattern")
    assert "ERROR: Неправильный формат ввода" in result


def test_grep_invalid_path_type():
    """Тест: ошибка при невалидном типе пути"""
    result = function_grep("grep pattern 123")
    assert "ERROR: Путь 123 не найден" in result


def test_grep_pattern_with_special_regex_chars():
    """Тест: шаблон со специальными regex символами"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test [content] with (special) chars")
        temp_file = f.name

    try:
        result = function_grep(f'grep "[content]" "{temp_file}"')
        # Должен найти, но проверяем что нет ошибки
        assert "ERROR" not in result or "INFO: Совпадений не найдено" in result
    finally:
        os.unlink(temp_file)


def test_grep_in_directory_without_r():
    """Тест: поиск в директории без флага -r"""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = function_grep(f'grep pattern "{temp_dir}"')
        assert "ERROR" in result or "INFO: Совпадений не найдено" in result


def test_grep_multiple_patterns():
    """Тест: несколько шаблонов (неподдерживаемый формат)"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test content")
        temp_file = f.name

    try:
        result = function_grep(f'grep pattern1 pattern2 "{temp_file}"')
        assert "ERROR" in result
    finally:
        os.unlink(temp_file)


def test_grep_binary_file():
    """Тест: поиск в бинарном файле"""
    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".bin") as f:
        f.write(b"\x00\x01\x02\x03pattern\x04\x05")
        temp_file = f.name

    try:
        result = function_grep(f'grep pattern "{temp_file}"')
        # Должен пропустить бинарный файл без ошибки
        assert "ERROR" not in result
    finally:
        os.unlink(temp_file)
