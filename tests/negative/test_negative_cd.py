import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.command_cd import function_cd


def test_cd_nonexistent_directory():
    """Тест: ошибка при переходе в несуществующую директорию"""
    result = function_cd("cd несуществующая_папка")
    assert "ERROR: Каталог несуществующая_папка не найден" in result


def test_cd_to_file():
    """Тест: ошибка при попытке перехода в файл"""
    # Создаём тестовый текстовый файл
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test")
        temp_file = f.name

    try:
        result = function_cd(f"cd {temp_file}")
        assert "ERROR: Каталог" in result and "не найден" in result
    finally:
        os.unlink(temp_file)


def test_cd_empty_command():
    """Тест: ошибка при отсутствии пути"""
    result = function_cd("cd")
    assert "ERROR: Путь не указан" in result


def test_cd_multiple_dots():
    """Тест: ошибка при множественных точках"""
    result = function_cd("cd .....")
    assert "ERROR: Каталог ..... не найден" in result


def test_cd_protected_directory():
    """Тест: ошибка при переходе в системную директорию (если нет прав)"""
    result = function_cd("cd /root")  # На Linux/Mac
    # result = function_cd('cd C:\\Windows\\System32\\config') # Windows
    assert "ERROR" in result


def test_cd_path_with_null_character():
    """Тест: путь с null-символом"""
    result = function_cd("cd path\0with_null")
    assert "ERROR" in result


def test_cd_to_system_protected_directory():
    """Тест: переход в системную защищенную директорию"""
    if os.name == "nt":  # Windows
        result = function_cd("cd C:\\Windows\\System32\\Config")
    else:  # Linux/Mac
        result = function_cd("cd /root")
    assert "ERROR" in result


def test_cd_path_with_wildcards():
    """Тест: путь с wildcard символами"""
    result = function_cd("cd some*path")
    assert "ERROR" in result


def test_cd_empty_path_after_quotes():
    """Тест: пустой путь в кавычках"""
    result = function_cd('cd ""')
    assert "ERROR" in result


def test_cd_path_with_only_slashes():
    """Тест: путь состоящий только из слешей"""
    result = function_cd("cd ////")
    assert "ERROR" in result


def test_cd_to_broken_symlink():
    """Тест: переход по битой симлинк-ссылке"""
    if os.name != "nt":  # Не для Windows
        with tempfile.TemporaryDirectory() as temp_dir:
            broken_symlink = os.path.join(temp_dir, "broken_link")
            os.symlink("/non/existent/path", broken_symlink)
            result = function_cd(f"cd {broken_symlink}")
            assert "ERROR" in result
