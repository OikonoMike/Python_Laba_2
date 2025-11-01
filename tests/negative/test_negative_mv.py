import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.command_mv import function_mv


def test_mv_nonexistent_source():
    """Тест: ошибка при несуществующем источнике"""
    result = function_mv("mv несуществующий.txt новый.txt")
    assert "ERROR: Источник несуществующий.txt не найден" in result


def test_mv_self_move():
    """Тест: ошибка при перемещении в самого себя"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test")
        temp_file = f.name

    try:
        result = function_mv(f"mv {temp_file} {temp_file}")
        assert "ERROR: Невозможно переместить файл в самого себя" in result
    finally:
        os.unlink(temp_file)


def test_mv_insufficient_arguments():
    """Тест: ошибка при недостаточном количестве аргументов"""
    result = function_mv("mv файл.txt")
    assert "ERROR: Неправильный формат ввода" in result


def test_mv_no_arguments():
    """Тест: ошибка при отсутствии аргументов"""
    result = function_mv("mv")
    assert "ERROR: Неправильный формат ввода" in result


def test_mv_permission_error():
    """Тест: ошибка при отсутствии прав доступа"""
    # Создаем файл без прав на чтение (на Linux/Mac)
    if os.name != "nt":  # Не для Windows
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("test")
            temp_file = f.name

        try:
            os.chmod(temp_file, 0o000)  # Убираем все права
            result = function_mv(f"mv {temp_file} новый.txt")
            assert "ERROR: Нет прав доступа" in result
        finally:
            os.chmod(temp_file, 0o644)  # Восстанавливаем права
            os.unlink(temp_file)


def test_mv_destination_is_subdirectory_of_source():
    """Тест: перемещение директории в её же поддиректорию"""
    with tempfile.TemporaryDirectory() as temp_dir:
        subdir = os.path.join(temp_dir, "subdir")
        os.makedirs(subdir)

        result = function_mv(f'mv "{temp_dir}" "{subdir}"')
        assert "ERROR" in result


def test_mv_circular_move():
    """Тест: циклическое перемещение"""
    with tempfile.TemporaryDirectory() as temp_dir:
        dir_a = os.path.join(temp_dir, "A")
        dir_b = os.path.join(temp_dir, "B")
        os.makedirs(dir_a)
        os.makedirs(dir_b)

        # Пытаемся переместить B в A (цикл)
        result = function_mv(f'mv "{dir_b}" "{os.path.join(dir_b, "A")}"')
        assert "ERROR" in result


def test_mv_to_readonly_destination():
    """Тест: перемещение в директорию только для чтения"""
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
                result = function_mv(f'mv "{source_file}" "{readonly_dir}"')
                assert "ERROR: Нет прав доступа" in result
            finally:
                os.chmod(readonly_dir, 0o755)
                if os.path.exists(source_file):
                    os.unlink(source_file)


def test_mv_across_filesystems():
    """Тест: перемещение между разными файловыми системами"""
    # Создаем временный файл и пытаемся переместить в /tmp (если это другая FS)
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test")
        source_file = f.name

    try:
        if os.name != "nt":  # Linux/Mac
            result = function_mv(f'mv "{source_file}" "/tmp/moved_file.txt"')
            # Может сработать, а может быть ошибка прав
            assert result is None or "ERROR" in result
        else:  # Windows
            result = function_mv(
                f'mv "{source_file}" "C:\\Windows\\Temp\\moved_file.txt"'
            )
            assert result is None or "ERROR" in result
    finally:
        # Удаляем если остался исходный файл
        if os.path.exists(source_file):
            os.unlink(source_file)
        # Удаляем если создался целевой файл
        if os.name != "nt" and os.path.exists("/tmp/moved_file.txt"):
            os.unlink("/tmp/moved_file.txt")
        elif os.name == "nt" and os.path.exists("C:\\Windows\\Temp\\moved_file.txt"):
            os.unlink("C:\\Windows\\Temp\\moved_file.txt")
