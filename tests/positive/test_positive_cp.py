import os
import sys
import tempfile

from src.command_cp import function_cp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def test_cp_single_file():
    """Тест: копирование одиночного файла"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as source:
        source.write("test content")
        source_path = source.name

    dest_path = source_path + ".copy"

    try:
        result = function_cp(f'cp "{source_path}" "{dest_path}"')
        assert result is None  # Успешное выполнение возвращает None
        assert os.path.exists(dest_path)
        with open(dest_path, "r") as f:
            assert f.read() == "test content"
    finally:
        for path in [source_path, dest_path]:
            if os.path.exists(path):
                os.unlink(path)


def test_cp_file_to_directory():
    """Тест: копирование файла в директорию"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as source:
        source.write("test content")
        source_path = source.name

    with tempfile.TemporaryDirectory() as temp_dir:
        result = function_cp(f'cp "{source_path}" "{temp_dir}"')
        assert result is None

        dest_file = os.path.join(temp_dir, os.path.basename(source_path))
        assert os.path.exists(dest_file)
        with open(dest_file, "r") as f:
            assert f.read() == "test content"

    os.unlink(source_path)
