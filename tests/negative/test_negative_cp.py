import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.command_cp import function_cp


def test_cp_nonexistent_source():
    """Тест: ошибка при несуществующем источнике"""
    result = function_cp("cp несуществующий.txt копия.txt")
    assert "ERROR: Файла несуществующий.txt не найдено" in result


def test_cp_insufficient_arguments():
    """Тест: ошибка при недостаточном количестве аргументов"""
    result = function_cp("cp файл.txt")
    assert "ERROR: Неправильный формат ввода" in result


def test_cp_r_with_file():
    """Тест: ошибка при использовании -r с файлом"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test")
        temp_file = f.name

    try:
        result = function_cp(f"cp -r {temp_file} копия.txt")
        assert (
            "ERROR: Опция -r поддерживается только для копирования каталогов" in result
        )
    finally:
        os.unlink(temp_file)


def test_cp_not_a_file():
    """Тест: ошибка когда источник не является файлом (но и не директория)"""
    # Создаем что-то что не является ни файлом ни директорией
    # В данном случае просто тестируем на несуществующем пути
    result = function_cp("cp invalid_path dest.txt")
    assert "ERROR: Файла invalid_path не найдено" in result


def test_cp_source_and_destination_same():
    """Тест: источник и назначение одинаковые"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test")
        temp_file = f.name

    try:
        result = function_cp(f'cp "{temp_file}" "{temp_file}"')
        assert "ERROR: Невозможно скопировать файл в самого себя" in result
    finally:
        os.unlink(temp_file)


def test_cp_to_readonly_directory():
    """Тест: копирование в директорию только для чтения"""
    if os.name != "nt":  # Не для Windows
        with tempfile.TemporaryDirectory() as temp_dir:
            readonly_dir = os.path.join(temp_dir, "readonly")
            os.makedirs(readonly_dir)
            os.chmod(readonly_dir, 0o444)  # Только чтение

            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".txt"
            ) as f:
                f.write("test")
                source_file = f.name

            try:
                result = function_cp(f'cp "{source_file}" "{readonly_dir}"')
                assert "ERROR: Нет прав доступа" in result
            finally:
                os.chmod(readonly_dir, 0o755)
                os.unlink(source_file)


def test_cp_invalid_flag():
    """Тест: неверный флаг"""
    result = function_cp("cp -x file.txt dest.txt")
    assert "ERROR" in result


def test_cp_multiple_invalid_sources():
    """Тест: несколько неверных источников"""
    result = function_cp("cp file1.txt file2.txt file3.txt dest/")
    assert "ERROR" in result
