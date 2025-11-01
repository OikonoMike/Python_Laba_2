import os
import sys
import tempfile

from src.command_cat import function_cat

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def test_cat_file_not_found():
    """Тест: ошибка при несуществующем файле"""
    result = function_cat("cat несуществующий_файл.txt")
    assert "ERROR: Данного файла нет в этом каталоге" in result


def test_cat_nonexistent_file_with_spaces():
    """Тест: ошибка при несуществующем файле с пробелами"""
    result = function_cat('cat "файл с пробелами.txt"')
    assert "ERROR: Данного файла нет в этом каталоге" in result


def test_cat_directory():
    """Тест: ошибка при попытке чтения директории"""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = function_cat(f"cat {temp_dir}")
        assert "ERROR: Невозможно открыть файл, так как он является каталогом" in result


def test_cat_empty_command():
    """Тест: ошибка при пустой команде после cat (отсутствие имени файла)"""
    result = function_cat("cat")
    assert "ERROR: Имя файла не указано" in result


def test_cat_incorrect_format_input():
    """Тест: ошибка при вводе команды (неправильный формат ввода)"""
    result = function_cat("cat файл_1.txt файл_2.txt")
    assert "ERROR: Неправильный формат ввода" in result


def test_cat_binary_file():
    """Тест: ошибка при чтении бинарного файла"""
    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".exe") as f:
        # Создаем бинарный файл, чтобы убедиться, что вылетит ошибка
        f.write(b"\xff\x00\x01\x02\x03\x04\x05")
        temp_file = f.name
    try:
        result = function_cat(f"cat {temp_file}")
        assert "ERROR: Невозможно прочитать файл. Файл является бинарным" in result
    finally:
        os.unlink(temp_file)


def test_cat_file_with_special_chars_in_name():
    """Тест: ошибка при файле со специальными символами в имени (если не существует)"""
    result = function_cat('cat "file@with#special$chars.txt"')
    assert "ERROR: Данного файла нет в этом каталоге" in result


def test_cat_path_traversal_attempt():
    """Тест: попытка path traversal атаки"""
    result = function_cat("cat ../../../etc/passwd")
    assert "ERROR" in result


def test_cat_empty_filename():
    """Тест: пустое имя файла"""
    result = function_cat('cat ""')
    assert "ERROR" in result


def test_cat_only_spaces_in_filename():
    """Тест: имя файла состоит только из пробелов"""
    result = function_cat('cat "   "')
    assert "ERROR" in result


def test_cat_multiple_nonexistent_files():
    """Тест: несколько несуществующих файлов (неправильный формат)"""
    result = function_cat("cat file1.txt file2.txt file3.txt")
    assert "ERROR: Неправильный формат ввода" in result


def test_cat_very_long_filename():
    """Тест: очень длинное имя файла"""
    long_name = "a" * 255 + ".txt"
    result = function_cat(f"cat {long_name}")
    assert "ERROR" in result


def test_cat_filename_with_newline():
    """Тест: имя файла с символом новой строки"""
    result = function_cat('cat "file\nwithnewline.txt"')
    assert "ERROR" in result
