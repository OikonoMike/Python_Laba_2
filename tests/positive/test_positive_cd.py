import os
import sys

from src.command_cd import function_cd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def test_cd_to_home():
    """Тест: переход в домашний каталог"""
    original_dir = os.getcwd()
    home_dir = os.path.expanduser("~")

    try:
        result = function_cd("cd ~")
        assert result is None

        current_dir = os.getcwd()
        expected_dir = os.path.normpath(home_dir)
        actual_dir = os.path.normpath(current_dir)
        assert actual_dir == expected_dir

    finally:
        os.chdir(original_dir)


def test_cd_current_directory():
    """Тест: переход в текущий каталог (остаемся на месте)"""
    original_dir = os.getcwd()

    try:
        result = function_cd("cd .")
        assert result is None
        assert os.getcwd() == original_dir

    finally:
        os.chdir(original_dir)
