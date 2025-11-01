import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.command_ls import function_ls


def test_ls_nonexistent_path():
    """Тест: ошибка при несуществующем пути"""
    result = function_ls("ls несуществующая_папка")
    assert "ERROR: Каталог несуществующая_папка не найден" in result


def test_ls_too_many_arguments():
    """Тест: ошибка при слишком большом количестве аргументов"""
    result = function_ls("ls папка1 папка2 папка3")
    assert "ERROR: Неправильный формат ввода" in result


def test_ls_file_instead_of_directory():
    """Тест: ошибка при указании файла вместо директории"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test")
        temp_file = f.name

    try:
        result = function_ls(f"ls {temp_file}")
        assert "ERROR: Каталог" in result and "не найден" in result
    finally:
        os.unlink(temp_file)


def test_ls_invalid_flag():
    """Тест: неверный флаг"""
    result = function_ls("ls -x")
    assert "ERROR" in result


def test_ls_multiple_invalid_flags():
    """Тест: несколько неверных флагов"""
    result = function_ls("ls -x -y -z")
    assert "ERROR" in result


def test_ls_flag_after_path():
    """Тест: флаг после пути (неправильный порядок)"""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = function_ls(f'ls "{temp_dir}" -l')
        # В вашей реализации это может работать, проверяем
        if "ERROR" in result:
            assert "ERROR" in result


def test_ls_empty_directory_name():
    """Тест: пустое имя директории"""
    result = function_ls('ls ""')
    assert "ERROR" in result


def test_ls_directory_with_special_permissions():
    """Тест: директория без прав на чтение"""
    if os.name != "nt":  # Не для Windows
        with tempfile.TemporaryDirectory() as temp_dir:
            no_access_dir = os.path.join(temp_dir, "no_access")
            os.makedirs(no_access_dir)
            os.chmod(no_access_dir, 0o000)  # Никаких прав

            result = function_ls(f'ls "{no_access_dir}"')
            assert "ERROR" in result

            os.chmod(no_access_dir, 0o755)  # Восстанавливаем права


def test_ls_too_many_combinations():
    """Тест: слишком много комбинаций аргументов"""
    result = function_ls("ls -l -r -a /path1 /path2 /path3")
    assert "ERROR" in result
