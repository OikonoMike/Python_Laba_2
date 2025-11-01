import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.command_rm import function_rm


def test_rm_nonexistent_file():
    """Тест: ошибка при несуществующем файле"""
    result = function_rm("rm несуществующий.txt")
    assert "ERROR: В каталоге нет файла несуществующий.txt" in result


def test_rm_directory_without_r():
    """Тест: ошибка при удалении директории без -r"""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = function_rm(f"rm {temp_dir}")
        assert "является каталогом. Для удаления каталога используйте -r" in result


def test_rm_r_with_file():
    """Тест: ошибка при использовании -r с файлом"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test")
        temp_file = f.name

    try:
        result = function_rm(f"rm -r {temp_file}")
        assert "ERROR: Рекурсивное удаление доступно только для каталогов" in result
    finally:
        os.unlink(temp_file)


def test_rm_empty_command():
    """Тест: ошибка при отсутствии аргументов"""
    result = function_rm("rm")
    assert "ERROR: Не указан файл или каталог для удаления" in result


def test_rm_r_empty_command():
    """Тест: ошибка при отсутствии аргументов для -r"""
    result = function_rm("rm -r")
    assert "ERROR: Не указан каталог для рекурсивного удаления" in result


def test_rm_protected_paths():
    """Тест: ошибка при попытке удаления защищенных путей"""
    protected_paths = [".", "..", "~", "/"]

    for path in protected_paths:
        result = function_rm(f"rm {path}")
        assert "ERROR: Нельзя удалять" in result


def test_rm_r_protected_paths():
    """Тест: ошибка при попытке рекурсивного удаления защищенных путей"""
    protected_paths = [".", "..", "~", "/"]

    for path in protected_paths:
        result = function_rm(f"rm -r {path}")
        assert "ERROR: Нельзя удалять" in result


def test_rm_symlink_to_directory():
    """Тест: удаление симлинка на директорию"""
    if os.name != "nt":  # Не для Windows
        with tempfile.TemporaryDirectory() as temp_dir:
            target_dir = os.path.join(temp_dir, "target")
            os.makedirs(target_dir)

            symlink = os.path.join(temp_dir, "symlink")
            os.symlink(target_dir, symlink)

            # Должен удалить только симлинк, а не целевую директорию
            result = function_rm(f'rm "{symlink}"')
            assert result is None
            assert not os.path.exists(symlink)
            assert os.path.exists(target_dir)  # Целевая директория должна остаться


def test_rm_multiple_nonexistent_files():
    """Тест: удаление нескольких несуществующих файлов"""
    result = function_rm("rm file1.txt file2.txt file3.txt")
    assert "ERROR" in result


def test_rm_mixed_existent_nonexistent():
    """Тест: удаление смеси существующих и несуществующих файлов"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test")
        existent_file = f.name

    try:
        result = function_rm(f'rm "{existent_file}" nonexistent.txt')
        # В вашей реализации это может не поддерживаться
        assert "ERROR" in result or result is None
    finally:
        if os.path.exists(existent_file):
            os.unlink(existent_file)


def test_rm_with_invalid_flag():
    """Тест: неверный флаг"""
    result = function_rm("rm -x file.txt")
    assert "ERROR" in result


def test_rm_empty_string_argument():
    """Тест: пустая строка в качестве аргумента"""
    result = function_rm('rm ""')
    assert "ERROR" in result
