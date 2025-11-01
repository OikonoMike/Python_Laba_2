import os
import sys
import tempfile

from src.command_ls import function_ls

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def test_ls_current_directory():
    """Тест: список файлов текущей директории"""
    result = function_ls("ls")
    assert result is not None
    assert "ERROR" not in result
    # Должен вернуть список файлов или 'Пустой каталог'
    assert isinstance(result, str)


def test_ls_specific_directory():
    """Тест: список файлов указанной директории"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Создаем несколько файлов
        with open(os.path.join(temp_dir, "test_file.txt"), "w") as f:
            f.write("content")

        result = function_ls(f'ls "{temp_dir}"')
        assert result is not None
        assert "ERROR" not in result
        assert "test_file.txt" in result


def test_ls_detailed():
    """Тест: детализированный список с флагом -l"""
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(os.path.join(temp_dir, "test.txt"), "w") as f:
            f.write("test")

        result = function_ls(f'ls "{temp_dir}" -l')
        assert result is not None
        assert "ERROR" not in result
        # В детализированном выводе должна быть информация
        assert "test.txt" in result
        assert "Каталог:" in result
